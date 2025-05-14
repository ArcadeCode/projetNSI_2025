@echo off
setlocal enabledelayedexpansion

:: Initialisation des options
set SYNC=1
set FONT_REFRESH=1
set CLEAN_LOGS=1
:: Vérification des arguments
for %%A in (%*) do (
    if "%%A"=="--no-sync" set SYNC=0
    if "%%A"=="--no-font-refresh" set FONT_REFRESH=0
    if "%%A"=="--no-log-clean" set CLEAN_LOGS=0
)

:: Exécution des commandes en fonction des options
if %SYNC%==1 python -m uv sync
if %FONT_REFRESH%==1 python -m uv run python ./scripts/refresh_font.py
if %CLEAN_LOGS%==1 python -m uv run python ./scripts/clear_logs.py

@echo Starting the app, this can take some time...
python -m uv run python -m app.main


::python -m uv sync
::python -m uv run python ./refresh_font.py
::python -m uv run python -m app.main screen:phone_samsung_galaxy_s5