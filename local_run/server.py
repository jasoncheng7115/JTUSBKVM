"""
=========================================================================

JTUSBKVM - Web Console Loader

Version: 1.3.1
Last Update: 2025-05-12

Author: Jason Cheng
E-mail: jason@jason.tools
GitHub: https://github.com/jasoncheng7115

License: GNU Affero General Public License v3.0
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
any later version.

=========================================================================

Required Installations:

1. Python Packages (Required)

   Windows:
   pip install requests

   macOS:
   # 建立並使用虛擬環境（推薦）
   python3 -m venv jtusbkvm-env
   source jtusbkvm-env/bin/activate
   pip3 install requests
   
   # 或使用 Homebrew（替代方案）
   brew install python-requests

   Linux:
   # Debian/Ubuntu - 使用系統套件管理器
   sudo apt install python3-requests
   
   # 或使用虛擬環境（推薦）
   python3 -m venv jtusbkvm-env
   source jtusbkvm-env/bin/activate
   python3 -m pip install requests
   

2. OpenSSL (Required)

   Windows:
   Download and install from https://slproweb.com/products/Win32OpenSSL.html
   
   macOS:
   brew install openssl
   
   Linux (Ubuntu/Debian):
   sudo apt install openssl
   
   Linux (CentOS/RHEL):
   sudo yum install openssl

=========================================================================
"""

import http.server
import ssl
import os
import webbrowser
import socket
import subprocess
import datetime
import shutil
import sys
import re
import requests
from pathlib import Path

# 檔案的遠端位置
REMOTE_FILES = {
    'index.html': 'https://raw.githubusercontent.com/jasoncheng7115/JTUSBKVM/refs/heads/main/web/jtusbkvm.html',
    'logo-1.png': 'https://raw.githubusercontent.com/jasoncheng7115/JTUSBKVM/refs/heads/main/web/logo-1.png',
    'js/xterm.css': 'https://cdn.jsdelivr.net/npm/xterm/css/xterm.css',
    'js/xterm.js': 'https://cdn.jsdelivr.net/npm/xterm/lib/xterm.js',
    'js/xterm-addon-fit.js': 'https://cdn.jsdelivr.net/npm/xterm-addon-fit/lib/xterm-addon-fit.js'
}

OPENSSL_PATH = "C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe"

def get_version_from_html(content):
    """從 HTML 內容中取得版本號"""
    version_match = re.search(r'Version:\s*(\d+\.\d+\.\d+)', content)
    if version_match:
        return version_match.group(1)
    return "0.0.0"

def ensure_directory_exists(filepath):
    """確保目錄存在"""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def check_internet_connection():
    """檢查網路連線狀態"""
    try:
        # 嘗試連線到一個可靠的網站
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False

def download_file(url, local_path):
    """下載檔案"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        ensure_directory_exists(local_path)
        with open(local_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print()
        print()
        print(f'下載 {local_path} 時發生錯誤: {str(e)}')
        return False

def check_local_files():
    """檢查本機檔案是否存在，並顯示少的檔案清單"""
    missing_files = []
    for local_path in REMOTE_FILES.keys():
        if not os.path.exists(local_path):
            missing_files.append(local_path)
    return missing_files

def check_and_update_files():
    """檢查並更新所有需要的檔案"""
    # 檢查網路連線
    has_internet = check_internet_connection()
    
    # 檢查本機檔案
    missing_files = check_local_files()
    
    if not has_internet:
        if missing_files:
            print("目前沒有網路連線可使用，且本機缺少以下檔案：")
            for file in missing_files:
                print(f"- {file}")
            print("請連線網路後再次執行程式或手動加入缺少的檔案。")
            print("但程式仍將嘗試使用現有檔案啟動...")
            return len(missing_files) == 0
        else:
            print()
            print()
            print("目前沒有網路連線，將使用本機檔案運行...")
            return True
    
    # 如果有網路，則嘗試更新
    all_success = True
    
    for local_path, remote_url in REMOTE_FILES.items():
        local_file = Path(local_path)
        
        try:
            if not local_file.exists():
                print(f'下載 {local_path}...')
                if not download_file(remote_url, local_path):
                    all_success = False
                    print()
                    print()
                    print(f'錯誤：無法下載 {local_path}')
                else:
                    print(f'{local_path} 下載完成')
            else:
                # 檢查遠端檔案是否有更新
                try:
                    response = requests.get(remote_url, timeout=5)
                    response.raise_for_status()
                    remote_content = response.content
                    
                    # 對於 HTML 檔案，檢查版本號碼
                    if local_path == 'index.html':
                        remote_text = response.text
                        remote_version = get_version_from_html(remote_text)
                        
                        with open(local_file, 'r', encoding='utf-8') as f:
                            local_content = f.read()
                            local_version = get_version_from_html(local_content)
                            
                        if remote_version > local_version:
                            print(f'發現新版本 {remote_version}，更新中...')
                            with open(local_file, 'w', encoding='utf-8') as f:
                                f.write(remote_text)
                            print(f'{local_path} 更新完成')
                        else:
                            print(f'目前版本 {local_version} 已是最新')
                    else:
                        # 對於其他檔案，檢查檔案大小或修改時間
                        # 由於無法直接獲取遠端檔案的修改時間，這裡直接比較檔案大小
                        local_size = os.path.getsize(local_path)
                        remote_size = len(remote_content)
                        
                        if remote_size != local_size:
                            print(f'發現 {local_path} 有更新，下載中...')
                            with open(local_path, 'wb') as f:
                                f.write(remote_content)
                            print(f'{local_path} 更新完成')
                except Exception as e:
                    print()
                    print()
                    print(f'檢查 {local_path} 更新時發生錯誤: {str(e)}')
                    print('將使用本機檔案繼續...')
                    
        except Exception as e:
            print()
            print()
            print(f'處理 {local_path} 時發生錯誤: {str(e)}')
            print('將使用本機檔案繼續...')
            
    return True  # 即使有錯誤，也會嘗試使用已有的本機檔案

def check_openssl():
    """檢查是否有安裝 OpenSSL"""
    # 優先使用指定的 OpenSSL 路徑
    if os.path.exists(OPENSSL_PATH) and os.access(OPENSSL_PATH, os.X_OK):
        return True
    
    # 若指定路徑不存在或無法執行，則檢查系統 PATH
    if shutil.which('openssl') is None:
        print()
        print()
        print('錯誤：未安裝 OpenSSL')
        print('請安裝 OpenSSL:')
        print()
        print('Windows: https://slproweb.com/products/Win32OpenSSL.html')
        print('macOS: 使用 brew install openssl')
        print('Linux: sudo apt install openssl 或對應的包管理命令')
        return False
    return True

def is_cert_expired(cert_path):
    """檢查憑證是否過期"""
    try:
        # 使用設定的 OpenSSL 路徑
        openssl_command = OPENSSL_PATH if os.path.exists(OPENSSL_PATH) else 'openssl'
        
        # 使用 openssl 檢查憑證過期日期
        result = subprocess.run(
            [openssl_command, 'x509', '-in', cert_path, '-noout', '-enddate'],
            capture_output=True,
            text=True,
            timeout=30  # 增加 timeout 參數，避免命令卡住
        )
        if result.returncode != 0:
            return True

        # 解析過期日期
        end_date = result.stdout.split('=')[1].strip()
        end_date = datetime.datetime.strptime(end_date, '%b %d %H:%M:%S %Y %Z')
        
        # 如果憑證在30天內過期，也視為需要更新
        return end_date - datetime.datetime.now() < datetime.timedelta(days=30)
    except Exception:
        return True
    
def create_cert():
    """建立或更新 SSL 憑證"""
    cert_path = Path('cert.pem')
    key_path = Path('key.pem')
    
    # 檢查是否需要建立新憑證
    need_new_cert = (
        not cert_path.exists() or 
        not key_path.exists() or 
        is_cert_expired(cert_path)
    )
    
    if need_new_cert:
        if not check_openssl():
            return False
            
        print('建立新的 SSL 憑證...')
        
        # 先檢查檔案權限
        if cert_path.exists() and not os.access(cert_path, os.W_OK):
            print()
            print()
            print(f'錯誤：無法寫入 {cert_path}，請檢查檔案權限')
            return False
        if key_path.exists() and not os.access(key_path, os.W_OK):
            print()
            print()
            print(f'錯誤：無法寫入 {key_path}，請檢查檔案權限')
            return False
            
        try:
            # 使用設定的 OpenSSL 路徑
            openssl_command = OPENSSL_PATH if os.path.exists(OPENSSL_PATH) else 'openssl'
            
            # 建立新憑證
            result = subprocess.run([
                openssl_command, 'req', '-new', '-x509', 
                '-keyout', 'key.pem', 
                '-out', 'cert.pem',
                '-days', '365',
                '-nodes',
                '-subj', '/CN=localhost'
            ], capture_output=True, text=True, timeout=60)  # 增加 timeout 參數
            
            if result.returncode != 0:
                print()
                print()
                print('錯誤：建立憑證失敗')
                print(result.stderr)
                return False
                
        except Exception as e:
            print()
            print()
            print(f'錯誤：建立憑證時發生錯誤 - {str(e)}')
            return False
            
    return True

def is_port_available(port):
    """檢查 port 是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except:
            return False

def find_available_port(start_port=4443):
    """尋找可用的 port"""
    port = start_port
    while not is_port_available(port) and port < start_port + 100:
        port += 1
    return port if port < start_port + 100 else None

def open_supported_browser(url):
    """嘗試開啟 Chrome 或 Edge"""
    # Windows 的 Chrome 路徑
    win_chrome_paths = [
        os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
        os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
        os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe')
    ]
    
    # Windows 的 Edge 路徑
    win_edge_paths = [
        os.path.expandvars(r'%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe'),
        os.path.expandvars(r'%ProgramFiles%\Microsoft\Edge\Application\msedge.exe')
    ]
    
    try:
        # Windows
        if os.name == 'nt':
            # 先嘗試 Chrome
            for path in win_chrome_paths:
                if os.path.exists(path):
                    subprocess.Popen([path, url])
                    print('已使用 Chrome 開啟')
                    return True
                    
            # 再嘗試 Edge
            for path in win_edge_paths:
                if os.path.exists(path):
                    subprocess.Popen([path, url])
                    print('已使用 Edge 開啟')
                    return True
                    
        # macOS
        elif sys.platform == 'darwin':
            try:
                # 先嘗試 Chrome
                subprocess.Popen(['open', '-a', 'Google Chrome', url])
                print('已使用 Chrome 開啟')
                return True
            except:
                # 再嘗試 Edge
                try:
                    subprocess.Popen(['open', '-a', 'Microsoft Edge', url])
                    print('已使用 Edge 開啟')
                    return True
                except:
                    pass
                
        # Linux
        else:
            # 依序嘗試不同的瀏覽器命令
            browsers = [
                'google-chrome',
                'chrome',
                'chromium',
                'chromium-browser',
                'microsoft-edge'
            ]
            
            for browser in browsers:
                try:
                    subprocess.Popen([browser, url])
                    print(f'已使用 {browser} 開啟')
                    return True
                except FileNotFoundError:
                    continue
        print()
        print()            
        print('找不到支援的瀏覽器，請手動開啟以下網址：')
        print(url)
        print('請使用 Chrome 或 Edge 瀏覽器（89 版或更新）')
        return False
        
    except Exception as e:
        print()
        print()
        print(f'開啟瀏覽器時發生錯誤：{str(e)}')
        print(f'請手動使用 Chrome 或 Edge 開啟：{url}')
        return False

def main():
    # 確保在正確的目錄
    os.chdir(Path(__file__).parent)
    
    # 檢查並更新所有需要的檔案
    files_check_result = check_and_update_files()
    
    # 建立 SSL 憑證
    if not create_cert():
        input('按 Enter 鍵結束程式...')
        return
    
    # 尋找可用的 port
    port = find_available_port()
    if not port:
        print()
        print()
        print('錯誤：無法找到可用的 port（4443-4542）')
        input('按 Enter 鍵結束程式...')
        return
    
    # 設定伺服器
    server_address = ('localhost', port)
    try:
        httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    except Exception as e:
        print()
        print()
        print(f'錯誤：無法建立伺服器 - {str(e)}')
        input('按 Enter 鍵結束程式...')
        return
    
    # 設定 SSL
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    except Exception as e:
        print()
        print()
        print(f'錯誤：SSL 設定失敗 - {str(e)}')
        input('按 Enter 鍵結束程式...')
        return
    
    # 啟動伺服器
    url = f'https://localhost:{port}'
    print(f'伺服器啟動在：{url}')
    print('首次使用請在瀏覽器中允許不安全的憑證（因為是自簽憑證）')
    print('按 Ctrl+C 可停止伺服器')
    
    # 嘗試開啟支援的瀏覽器
    if not open_supported_browser(url):
        print('請確保已安裝 Chrome 或 Edge 瀏覽器')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n伺服器已停止')
        httpd.server_close()
    except Exception as e:
        print()
        print()
        print(f'\n錯誤：伺服器運行時發生錯誤 - {str(e)}')
    finally:
        input('按 Enter 鍵結束程式...')

if __name__ == '__main__':
    main()
