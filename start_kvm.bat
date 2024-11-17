# Windows版本 (start.bat):
@echo off
chcp 65001 > nul
title JTUSBKVM Server

:: 檢查 Python 是否安裝
python --version > nul 2>&1
if errorlevel 1 (
    echo Python 未安裝！
    echo 請從以下位置下載並安裝 Python：
    echo https://www.python.org/downloads/
    echo.
    echo 安裝時請勾選 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

:: 檢查 Python 版本
for /f "tokens=2" %%I in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%I"
for /f "tokens=1 delims=." %%I in ("%PYTHON_VERSION%") do set "PYTHON_MAJOR=%%I"
for /f "tokens=2 delims=." %%I in ("%PYTHON_VERSION%") do set "PYTHON_MINOR=%%I"

if %PYTHON_MAJOR% LSS 3 (
    echo Python 版本過舊！
    echo 當前版本：%PYTHON_VERSION%
    echo 需要 Python 3.6 或更新版本
    echo.
    pause
    exit /b 1
)
if %PYTHON_MAJOR%==3 if %PYTHON_MINOR% LSS 6 (
    echo Python 版本過舊！
    echo 當前版本：%PYTHON_VERSION%
    echo 需要 Python 3.6 或更新版本
    echo.
    pause
    exit /b 1
)

:: 執行伺服器
python server.py
exit /b 0