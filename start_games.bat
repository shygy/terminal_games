@echo off
REM Batch script to start terminal games on Windows

REM Change directory to the script location
cd /d "%~dp0"

REM Attempt to run the launcher with python command
python launch_games.py
if %ERRORLEVEL% NEQ 0 (
    REM If python command fails, try python3
    python3 launch_games.py
    if %ERRORLEVEL% NEQ 0 (
        REM If both fail, show error message
        echo Error: Could not run the games with Python.
        echo Please ensure Python 3 is installed and in your PATH.
        pause
        exit /b 1
    )
)

pause