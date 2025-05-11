@echo off
rem =========================================================================
rem
rem JTUSBKVM - Web Console Loader
rem
rem Version: 1.1.0
rem Last Update: 2024-05-11
rem
rem ��@��: Jason Cheng
rem �q�l�l��: jason@jason.tools
rem GitHub: https://github.com/jasoncheng7115
rem
rem ���v: GNU Affero General Public License v3.0
rem
rem �`�N: ���ɮ׶��H Big5 (cp950) �s�X�A�H�� CRLF ����r���s��
rem
rem
rem =========================================================================

rem �]�w�c�餤��N�X��
chcp 950 >nul
title JTUSBKVM Server

echo JTUSBKVM ���A���Ұʤu��
echo ====================================
echo.
echo ���b�ˬd Python �w�˪��A...
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ���~: Python ���w�˩Υ��[�J�t�θ��|�I
    echo.
    echo �ФU���æw�� Python:
    echo https://www.python.org/downloads/windows/
    echo.
    echo ���n: �w�ˮɽФĿ� [v] Add Python.exe to PATH
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do set pyver=%%a
echo �w��� Python %pyver%
echo.

echo �ˬd���n�� Python �Ҳ�...
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo ���b�w�� requests �Ҳ�...
    python -m pip install requests
    if %errorlevel% neq 0 (
        echo ���~: �w�� requests �Ҳե��ѡI
        echo �Ф�ʰ���H�U�R�O:
        echo python -m pip install requests
        echo.
        pause
        exit /b 1
    )
    echo Requests �Ҳզw�˦��\�C
    echo.
)

echo �ˬd server.py �ɮ�...
if not exist server.py (
    echo ���~: �䤣�� server.py �ɮסI
    echo �нT�{ server.py �P���妸�ɦ��P�@�ؿ��C
    echo.
    pause
    exit /b 1
)

echo.
echo �Ҧ��ˬd�w�q�L�A�ǳƱҰʦ��A��...
echo ====================================
echo.
echo ���b�Ұ� JTUSBKVM ���A��...
echo �Ф������������A���������N�|�פ���A���C
echo.

python server.py
if %errorlevel% neq 0 (
    echo.
    echo ���~: ���A���Ұʥ��ѡI
    echo ���ˬd���~�T���íץ����D�C
    echo.
    pause
    exit /b 1
)

echo.
echo ���A���w�����C
echo.
pause
exit /b 0