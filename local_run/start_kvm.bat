@echo off
rem =========================================================================
rem
rem JTUSBKVM - Web Console Loader
rem
rem Version: 1.1.0
rem Last Update: 2024-05-11
rem
rem 原作者: Jason Cheng
rem 電子郵件: jason@jason.tools
rem GitHub: https://github.com/jasoncheng7115
rem
rem 授權: GNU Affero General Public License v3.0
rem
rem 注意: 本檔案須以 Big5 (cp950) 編碼，以及 CRLF 換行字元存檔
rem
rem
rem =========================================================================

rem 設定繁體中文代碼頁
chcp 950 >nul
title JTUSBKVM Server

echo JTUSBKVM 伺服器啟動工具
echo ====================================
echo.
echo 正在檢查 Python 安裝狀態...
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤: Python 未安裝或未加入系統路徑！
    echo.
    echo 請下載並安裝 Python:
    echo https://www.python.org/downloads/windows/
    echo.
    echo 重要: 安裝時請勾選 [v] Add Python.exe to PATH
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do set pyver=%%a
echo 已找到 Python %pyver%
echo.

echo 檢查必要的 Python 模組...
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安裝 requests 模組...
    python -m pip install requests
    if %errorlevel% neq 0 (
        echo 錯誤: 安裝 requests 模組失敗！
        echo 請手動執行以下命令:
        echo python -m pip install requests
        echo.
        pause
        exit /b 1
    )
    echo Requests 模組安裝成功。
    echo.
)

echo 檢查 server.py 檔案...
if not exist server.py (
    echo 錯誤: 找不到 server.py 檔案！
    echo 請確認 server.py 與此批次檔位於同一目錄。
    echo.
    pause
    exit /b 1
)

echo.
echo 所有檢查已通過，準備啟動伺服器...
echo ====================================
echo.
echo 正在啟動 JTUSBKVM 伺服器...
echo 請勿關閉此視窗，關閉視窗將會終止伺服器。
echo.

python server.py
if %errorlevel% neq 0 (
    echo.
    echo 錯誤: 伺服器啟動失敗！
    echo 請檢查錯誤訊息並修正問題。
    echo.
    pause
    exit /b 1
)

echo.
echo 伺服器已關閉。
echo.
pause
exit /b 0