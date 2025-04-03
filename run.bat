@echo off
setlocal enabledelayedexpansion

:: Initialisation des options
set SYNC=1
set FONT_REFRESH=1
set "KIVY_LOG_FOLDER=C:\Users\%USERNAME%\.kivy\logs"

:: Supprime les logs avant de démarrer l'application Kivy
@echo Deleting old logs...
if exist "%KIVY_LOG_FOLDER%" del /Q "%KIVY_LOG_FOLDER%\*"

:: Vérification des arguments
for %%A in (%*) do (
    if "%%A"=="--no-sync" set SYNC=0
    if "%%A"=="--no-font-refresh" set FONT_REFRESH=0
)

:: Exécution des commandes en fonction des options
if %SYNC%==1 python -m uv sync
if %FONT_REFRESH%==1 python -m uv run python ./refresh_font.py

@echo Starting the app, this can take some time...
python -m uv run python -m app.main screen:phone_samsung_galaxy_s5


::python -m uv sync
::python -m uv run python ./refresh_font.py
::python -m uv run python -m app.main screen:phone_samsung_galaxy_s5