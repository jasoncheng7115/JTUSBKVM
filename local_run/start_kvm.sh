#!/bin/bash

# =========================================================================
#
# JTUSBKVM - Web Console Loader (for macOS/Linux)
#
# Version: 1.1.0
# Last Update: 2024-11-26
#
# Author: Jason Cheng
# E-mail: jason@jason.tools
# GitHub: https://github.com/jasoncheng7115
#
# License: GNU Affero General Public License v3.0
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# =========================================================================

# 設定正確的文字編碼
export LANG=en_US.UTF-8

# 檢查是否為 macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_NAME="macOS"
    PYTHON_CMD="python3"
    INSTALL_CMD="brew install python3"
    INSTALL_INFO="請先安裝 Homebrew（https://brew.sh），然後執行：\nbrew install python3"
else
    OS_NAME="Linux"
    PYTHON_CMD="python3"
    if command -v apt-get >/dev/null 2>&1; then
        INSTALL_CMD="sudo apt-get install python3"
        INSTALL_INFO="請執行：\nsudo apt-get update && sudo apt-get install python3"
    elif command -v dnf >/dev/null 2>&1; then
        INSTALL_CMD="sudo dnf install python3"
        INSTALL_INFO="請執行：\nsudo dnf install python3"
    elif command -v pacman >/dev/null 2>&1; then
        INSTALL_CMD="sudo pacman -S python"
        INSTALL_INFO="請執行：\nsudo pacman -S python"
    else
        INSTALL_CMD=""
        INSTALL_INFO="請使用您的套件管理器安裝 Python 3"
    fi
fi

# 檢查 Python 是否安裝
if ! command -v $PYTHON_CMD >/dev/null 2>&1; then
    echo "錯誤：Python 3 未安裝！"
    echo -e "在 $OS_NAME 上安裝 Python 3："
    echo -e "$INSTALL_INFO"
    echo ""
    read -p "按 Enter 鍵結束..."
    exit 1
fi

# 檢查 Python 版本
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ $PYTHON_MAJOR -lt 3 ] || ([ $PYTHON_MAJOR -eq 3 ] && [ $PYTHON_MINOR -lt 6 ]); then
    echo "Python 版本過舊！"
    echo "目前版本：$PYTHON_VERSION"
    echo "需要 Python 3.6 或更新版本"
    echo ""
    echo "請更新您的 Python 版本"
    echo ""
    read -p "按 Enter 鍵結束..."
    exit 1
fi

# 檢查並安裝 requests 模組
echo "檢查必要的 Python 模組..."
if ! $PYTHON_CMD -c "import requests" >/dev/null 2>&1; then
    echo "未安裝 requests 模組，正在安裝..."
    
    # 建立並使用虛擬環境
    if [ ! -d "venv" ]; then
        echo "建立虛擬環境..."
        $PYTHON_CMD -m venv venv
    fi
    
    # 啟動虛擬環境
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux"* ]]; then
        source venv/bin/activate
    else
        source venv/Scripts/activate
    fi
    
    # 安裝 requests
    pip install requests
    
    if [ $? -ne 0 ]; then
        echo "安裝 requests 模組失敗！"
        echo "請手動執行以下命令："
        echo "python3 -m pip install requests"
        read -p "按 Enter 鍵結束..."
        exit 1
    fi
    echo "requests 模組安裝完成"
fi

# 確保腳本有執行權限
chmod +x "$0"

# 如果存在虛擬環境就使用它
if [ -d "venv" ]; then
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux"* ]]; then
        source venv/bin/activate
    else
        source venv/Scripts/activate
    fi
fi

# 執行伺服器
$PYTHON_CMD server.py
exit 0
