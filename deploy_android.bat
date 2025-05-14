@echo off
setlocal enabledelayedexpansion

REM === CONFIGURATION ===
set USER=debian
set HOST=51.178.43.28
set LOCAL_APP=%CD%\app
set LOCAL_BIN=%CD%\bin
set REMOTE_APP=/home/%USER%/app
set REMOTE_BIN=/home/%USER%/app/bin
set KEY_PATH=C:\Users\estebandervaux\OneDrive\Documents\Cours\2024-2025\.secrets\.ssh\id_rsa
set BACKUP_SUFFIX=_backup_%random%

echo.
echo === Vérification des prérequis ===
if not exist "%LOCAL_APP%" (
    echo [ERREUR] Le dossier app local n'existe pas: %LOCAL_APP%
    goto :error
)

if not exist "%KEY_PATH%" (
    echo [ERREUR] La clé SSH n'existe pas: %KEY_PATH%
    goto :error
)

echo.
echo === Vérification de la connexion SSH ===
ssh -i "%KEY_PATH%" -o ConnectTimeout=5 -o BatchMode=yes %USER%@%HOST% "echo Connexion réussie" > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Impossible de se connecter au serveur %USER%@%HOST%
    echo Vérifiez votre connexion internet, l'état du serveur et les informations d'identification.
    goto :error
)

echo.
echo === Vérification de l'existence du dossier distant ===
ssh -i "%KEY_PATH%" %USER%@%HOST% "if [ -d '%REMOTE_APP%' ]; then echo 'exist'; else echo 'not_exist'; fi" > temp_result.txt
set /p REMOTE_DIR_STATUS=<temp_result.txt
del temp_result.txt

if "%REMOTE_DIR_STATUS%"=="exist" (
    echo [INFO] Le dossier distant %REMOTE_APP% existe déjà.
    
    echo.
    echo === Sauvegarde des fichiers importants sur le serveur ===
    ssh -i "%KEY_PATH%" %USER%@%HOST% "if [ -f '%REMOTE_APP%/buildozer.spec' ]; then cp '%REMOTE_APP%/buildozer.spec' '%REMOTE_APP%/buildozer.spec%BACKUP_SUFFIX%'; fi"
    if %ERRORLEVEL% NEQ 0 (
        echo [AVERTISSEMENT] Impossible de sauvegarder buildozer.spec. Continuation...
    ) else (
        echo [INFO] Fichier buildozer.spec sauvegardé.
    )
) else (
    echo [INFO] Création du dossier distant %REMOTE_APP%
    ssh -i "%KEY_PATH%" %USER%@%HOST% "mkdir -p '%REMOTE_APP%'"
    if %ERRORLEVEL% NEQ 0 (
        echo [ERREUR] Impossible de créer le dossier distant %REMOTE_APP%
        goto :error
    )
)

echo.
echo ======= ÉTAPE 1 : Transfert des fichiers individuels =======
for %%F in (%LOCAL_APP%\*) do (
    set "FILENAME=%%~nxF"
    echo Transfert de !FILENAME!...
    
    REM Éviter de transférer le dossier bin s'il existe localement
    if "!FILENAME!" NEQ "bin" (
        scp -i "%KEY_PATH%" "%%F" %USER%@%HOST%:%REMOTE_APP%/
        if !ERRORLEVEL! NEQ 0 (
            echo [ERREUR] Le transfert du fichier !FILENAME! a échoué.
            echo Tentative de continuer avec les autres fichiers...
        )
    )
)

REM Transfert récursif des sous-dossiers (sauf bin)
for /d %%D in (%LOCAL_APP%\*) do (
    set "DIRNAME=%%~nxD"
    if "!DIRNAME!" NEQ "bin" (
        echo Transfert du dossier !DIRNAME!...
        ssh -i "%KEY_PATH%" %USER%@%HOST% "mkdir -p '%REMOTE_APP%/!DIRNAME!'"
        scp -i "%KEY_PATH%" -r "%%D\*" %USER%@%HOST%:%REMOTE_APP%/!DIRNAME!/
        if !ERRORLEVEL! NEQ 0 (
            echo [AVERTISSEMENT] Problème lors du transfert du dossier !DIRNAME!. Continuation...
        )
    )
)

echo.
echo === Restauration du fichier buildozer.spec sauvegardé si nécessaire ===
ssh -i "%KEY_PATH%" %USER%@%HOST% "if [ -f '%REMOTE_APP%/buildozer.spec%BACKUP_SUFFIX%' ]; then mv '%REMOTE_APP%/buildozer.spec%BACKUP_SUFFIX%' '%REMOTE_APP%/buildozer.spec'; echo 'Fichier buildozer.spec restauré.'; fi"

echo.
echo === Vérification des permissions des scripts ===
ssh -i "%KEY_PATH%" %USER%@%HOST% "chmod +x '%REMOTE_APP%/buildozer.sh'"
if %ERRORLEVEL% NEQ 0 (
    echo [AVERTISSEMENT] Impossible de définir les permissions d'exécution pour buildozer.sh
)

echo.
echo ======= ÉTAPE 2 : Compilation Android avec Buildozer =======
echo Démarrage de la compilation...
ssh -i "%KEY_PATH%" %USER%@%HOST% "cd '%REMOTE_APP%' && bash buildozer.sh -v android debug"
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] L'exécution de buildozer.sh a échoué.
    goto :compilation_error
)

echo.
echo ======= ÉTAPE 3 : Récupération du dossier bin depuis le serveur =======
REM Vérifier si le dossier bin existe sur le serveur
ssh -i "%KEY_PATH%" %USER%@%HOST% "if [ -d '%REMOTE_BIN%' ]; then echo 'exist'; else echo 'not_exist'; fi" > temp_bin_status.txt
set /p REMOTE_BIN_STATUS=<temp_bin_status.txt
del temp_bin_status.txt

if "%REMOTE_BIN_STATUS%"=="not_exist" (
    echo [ERREUR] Le dossier bin n'existe pas sur le serveur.
    echo La compilation n'a probablement pas fonctionné correctement ou le chemin est incorrect.
    goto :error
)

REM Supprime et recrée le dossier local bin s'il existe
if exist %LOCAL_BIN% (
    echo Suppression du dossier bin local existant...
    rmdir /s /q %LOCAL_BIN%
    if %ERRORLEVEL% NEQ 0 (
        echo [ERREUR] Impossible de supprimer le dossier bin local existant.
        echo Vérifiez qu'aucun fichier n'est en cours d'utilisation.
        goto :error
    )
)

echo Création du dossier bin local...
mkdir %LOCAL_BIN%
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Impossible de créer le dossier bin local.
    goto :error
)

echo Téléchargement des fichiers compilés...
scp -i "%KEY_PATH%" -r %USER%@%HOST%:%REMOTE_BIN%/* %LOCAL_BIN%
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Le téléchargement du dossier bin a échoué.
    goto :error
)

echo.
echo ======= Déploiement terminé avec succès =======
echo Les fichiers APK devraient se trouver dans le dossier: %LOCAL_BIN%
goto :end

:compilation_error
echo.
echo [INFO] Malgré l'échec de la compilation, tentative de récupération des logs...
ssh -i "%KEY_PATH%" %USER%@%HOST% "if [ -f '%REMOTE_APP%/.buildozer/logs/buildozer.log' ]; then cat '%REMOTE_APP%/.buildozer/logs/buildozer.log' | tail -n 50; fi"
goto :error

:error
echo.
echo ======= Déploiement terminé avec des erreurs =======
endlocal
pause
exit /b 1

:end
endlocal
pause
exit /b 0