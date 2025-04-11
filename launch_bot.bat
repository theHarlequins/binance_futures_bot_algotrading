@echo off
echo Starting Binance Futures Trading Bot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking required packages...
pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install required packages
        pause
        exit /b 1
    )
)

REM Check if credentials.py exists
if not exist credentials.py (
    echo Error: credentials.py not found
    echo Please create credentials.py with your API keys
    pause
    exit /b 1
)

REM Launch the bot
echo Starting the bot...
python gui.py

REM If the bot crashes, pause to see the error message
pause 