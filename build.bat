@echo off
setlocal

REM === CONFIGURATION ===
set USER=debian
set HOST=51.178.43.28
set LOCAL_APP=%CD%\app
set LOCAL_BIN=%CD%\bin
set REMOTE_APP=/home/%USER%/app
set REMOTE_BIN=/home/%USER%/app/bin
set KEY_PATH=C:\Users\estebandervaux\OneDrive\Documents\Cours\2024-2025\.secrets\.ssh\id_rsa


echo.
echo ======= ÉTAPE 1 : Envoi de %LOCAL_APP% vers %USER%@%HOST%:%REMOTE_APP% =======
scp -i "%KEY_PATH%" -r %LOCAL_APP% %USER%@%HOST%:%REMOTE_APP%
IF %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Le transfert SCP a échoué.
    exit /b %ERRORLEVEL%
)

echo.
echo ======= ÉTAPE 2 : Compilation Android avec Buildozer =======
ssh -i "%KEY_PATH%" %USER%@%HOST% "cd %REMOTE_APP% && bash buildozer.sh -v android debug"
IF %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] L'exécution de buildozer.sh a échoué.
    exit /b %ERRORLEVEL%
)

echo.
echo ======= ÉTAPE 3 : Récupération du dossier bin depuis le serveur =======
REM Supprime et recrée le dossier local bin s’il existe
if exist %LOCAL_BIN% (
    rmdir /s /q %LOCAL_BIN%
)
mkdir %LOCAL_BIN%

scp -i "%KEY_PATH%" -r %USER%@%HOST%:%REMOTE_BIN% %LOCAL_BIN%
IF %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Le téléchargement du dossier bin a échoué.
    exit /b %ERRORLEVEL%
)

echo.
echo ======= Déploiement terminé avec succès =======
endlocal
pause
