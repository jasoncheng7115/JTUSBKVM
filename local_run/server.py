# server.py
import http.server
import ssl
import os
import webbrowser
import socket
import subprocess
import datetime
import shutil
import sys
from pathlib import Path

def check_openssl():
    """檢查是否有安裝 OpenSSL"""
    if shutil.which('openssl') is None:
        print('錯誤：未安裝 OpenSSL')
        print('請安裝 OpenSSL:')
        print('Windows: https://slproweb.com/products/Win32OpenSSL.html')
        print('macOS: 使用 brew install openssl')
        print('Linux: sudo apt install openssl 或對應的包管理命令')
        return False
    return True

def is_cert_expired(cert_path):
    """檢查憑證是否過期"""
    try:
        # 使用 openssl 檢查憑證過期日期
        result = subprocess.run(
            ['openssl', 'x509', '-in', cert_path, '-noout', '-enddate'],
            capture_output=True,
            text=True
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
            print(f'錯誤：無法寫入 {cert_path}，請檢查檔案權限')
            return False
        if key_path.exists() and not os.access(key_path, os.W_OK):
            print(f'錯誤：無法寫入 {key_path}，請檢查檔案權限')
            return False
            
        try:
            # 建立新憑證
            result = subprocess.run([
                'openssl', 'req', '-new', '-x509', 
                '-keyout', 'key.pem', 
                '-out', 'cert.pem',
                '-days', '365',
                '-nodes',
                '-subj', '/CN=localhost'
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print('錯誤：建立憑證失敗')
                print(result.stderr)
                return False
                
        except Exception as e:
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
                    
        print('找不到支援的瀏覽器，請手動開啟以下網址：')
        print(url)
        print('請使用 Chrome 或 Edge 瀏覽器（89 版或更新）')
        return False
        
    except Exception as e:
        print(f'開啟瀏覽器時發生錯誤：{str(e)}')
        print(f'請手動使用 Chrome 或 Edge 開啟：{url}')
        return False

def main():
    # 確保在正確的目錄
    os.chdir(Path(__file__).parent)
    
    # 建立 SSL 憑證
    if not create_cert():
        input('按 Enter 鍵結束程式...')
        return
    
    # 尋找可用的 port
    port = find_available_port()
    if not port:
        print('錯誤：無法找到可用的 port（4443-4542）')
        input('按 Enter 鍵結束程式...')
        return
    
    # 設定伺服器
    server_address = ('localhost', port)
    try:
        httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    except Exception as e:
        print(f'錯誤：無法建立伺服器 - {str(e)}')
        input('按 Enter 鍵結束程式...')
        return
    
    # 設定 SSL
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    except Exception as e:
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
        print(f'\n錯誤：伺服器運行時發生錯誤 - {str(e)}')
    finally:
        input('按 Enter 鍵結束程式...')

if __name__ == '__main__':
    main()