![JTUSBKVM-Logo](https://github.com/jasoncheng7115/JTUSBKVM/blob/main/JTUSBKVM.001.png?raw=true)

-----

# JTUSBKVM

> 本專案仍然在開發中。

-----

## 緣起

做為到處建置系統的 IT 人，有時難免會遇到在機房沒有機架式 KVM 或是搶不到 KVM 推車的窘境，或是在各種 LAB 環境要準備螢幕鍵盤滑鼠麻煩的場景。在幾年前我就在看 ATEN CV211 這款行動式 USB 帶線 KVM 產品，搭配筆電用非常方便，可惜它的價格接近一萬元，對我來說有點困難 😭😭😭

最近又常常有這樣的需求，有天忽然冒出「不如自己用 Arduino 自幹一組！」這樣的想法，於是........就搞出來了 ✌✌✌

當然這功能比不上大廠專業產品，例如 ISO 映像檔掛接的功能就沒有。要有當然也做得出來，可是要用更高階的開發板....失去初衷了，而且這款是 USBKVM，我人都走到伺服器前面了順手插個 USB 碟不就好了 (笑)


---

## 功能

### 硬體功能
* 一條 USB C 線接至控制端電腦 (若電腦無 Type C 可搭配 Type A 轉接頭)
* 一條 USB A 及 HDMI 線接至被控端電腦 (若控端為 VGA 可搭配轉接頭使用)
* 顯示訊號輸入 (BIOS 等級)，可輸入 1080P (4K 應該也可以收，沒測過)
* 傳遞鍵盤、滑鼠操作
* 一條 RJ45 終端機控制線，可連接至網路設備 RJ45 Console 連接埠

### 軟體功能
* 被控端畫面顯示，支援 16:9、16:10、4:3 等多種螢幕比例
* 送出鍵盤與滑鼠操作，包括滑鼠滾輪行為
* 支援功能鍵、特殊鍵與修飾鍵
* 支援貼上功能，可一次送出一批指令 (僅限英文、數字、符號，中日韓文等無法送出)
* 具擷圖、錄影功能
* 支援 Windows、Linux、macOS，搭配 Chrome、Chromium 或 Edge 瀏覽器
* 網路設備 Console 連線設定終端機，可快速切換鮑率與換行字元、下載歷程
  
---

## 組成

盒裝圖
![盒裝](https://raw.githubusercontent.com/jasoncheng7115/JTUSBKVM/refs/heads/main/screenshot/9_%E5%A4%96%E7%AE%B1.JPG)

零件圖
![零件](https://raw.githubusercontent.com/jasoncheng7115/JTUSBKVM/refs/heads/main/screenshot/9_%E9%9B%B6%E4%BB%B6.JPG)



### 硬體組成
* Arduino Pro Micro 開發板 x 2
* SP3232 RS232 轉接板 x 1
* HDMI 影像擷取器 x 1 
* VGA to HDMI 轉接頭 x 1
* Type C USB Hub 附轉接頭 x 1
* Type C 延長線 1M x 1
* HDMI 0.3M 線材 x 1
* DB9 to RJ45 轉接線 x 1
* MicroUSB to TypeA 0.3M 線材 x 2
* 杜邦端子母對母連接線 0.2M x 6
* 透明收納盒 x 1
* 全都在網路購入，成本合計大約 一千三

### 軟體組成
* 控制端與被控端免安裝任何軟體
* 純前端 HTML + CSS + JavaScript
* 完全無後端程式碼，均在使用者本機運作
* 視訊輸入採用瀏覽器標準 MediaStream API
* 控制器連接採用瀏覽器標準 Web Serial API
* Web 控制端頁面可使用我的 https://kvm.jason.tools
* Web 控制端頁面也可以使用我撰寫的離線應用程式，說明待撰寫 (local_run 下)

### 韌體組成
* Arduino 程式碼分為 A B 兩片開發板，均先釋出
 
  
> 有許多朋友提到為何不買零件重新 layout 板子，這樣可以體積更小、成本更低呢？
> 我的出發點是用容易買到的材料組裝，除了故障零件容易替換的好處之外，若日後這些零件全部拆開都有其各自原功能可以發揮，毫不浪費也不製造電子垃圾。 (這也算得上是沾點 ESG 吧 XD)


---

## 實例


從 macOS 連接控制 Windows 主機擷圖 (v1.3)

![從 macOS 連接控制 Windows 主機擷圖](https://raw.githubusercontent.com/jasoncheng7115/JTUSBKVM/refs/heads/main/screenshot/windows_1.png)

從 Windows 連接控制 Linux 主機擷圖 (v1.3)

![從 Windows 連接控制 Linux 主機擷圖](https://raw.githubusercontent.com/jasoncheng7115/JTUSBKVM/refs/heads/main/screenshot/linux_from_windows.png)

從 macOS 連接控制 Cisco 序列終端機 (v1.3)
![從 macOS 連接控制 Cisco 序列終端機 (](https://raw.githubusercontent.com/jasoncheng7115/JTUSBKVM/refs/heads/main/screenshot/console_cisco2.png)



連接控制 Linux 主機錄影 (v1.0)

![控制 Linux 主機錄影](https://github.com/jasoncheng7115/JTUSBKVM/blob/main/screenshot/6%20linux_ok_cut.gif?raw=true)


連接控制 Windows 主機錄影 (v1.0)

![控制 Windows 主機錄影](https://github.com/jasoncheng7115/JTUSBKVM/blob/main/screenshot/5%20windows_ok_cut.gif?raw=true)


---

## 接線說明

### 接線圖
> TODO

### 接線表

| **來源裝置** | **來源接腳** | **目的裝置** | **目的接腳** |
|:---|:---|:---|:---|
| Arduino Pro Micro A | USB 連接埠 | 控制端電腦 | USB 連接埠 |
| Arduino Pro Micro B | USB 連接埠 | 被控制端電腦 | USB 連接埠 |
| Arduino Pro Micro A | Pin8 接腳 | Arduino Pro Micro B | RX 接腳 |
| Arduino Pro Micro A | GND 接腳 | Arduino Pro Micro B | GND 接腳 |
| Arduino Pro Micro A | RX 接腳 | RS232 模組 (SP3232) | TX 接腳 |
| Arduino Pro Micro A | TX 接腳 | RS232 模組 (SP3232) | RX 接腳 |
| Arduino Pro Micro A | GND 接腳 | RS23 2模組 (SP3232) | GND 接腳 |
| Arduino Pro Micro A | VCC (5V) 接腳 | RS232 模組 (SP3232) | VCC 接腳 |


### 說明

* Arduino A 的 USB 連接埠：連接到控制端電腦（也就是你要操作的那台電腦）。
* Arduino B 的 USB 連接埠：連接到被控制端電腦（要被遠端控制的那台電腦）。
* Pin8 接腳：從 Arduino A 輸出訊號，送到 Arduino B 板 的 RX 接腳。
* GND（接地）：Arduino A、Arduino B、RS232 模組三者的 GND 接腳必須互相連接（共地）。
* RS232 模組 (SP3232)：作為 TTL 電平與標準 RS232 通訊規格之間的轉換橋樑，在此使用 TTL 側接腳。
* RX/TX 接法：
   * A 板的 RX 接 RS232 模組的 TX（交叉接法）
   * A 板的 TX 接 RS232 模組的 RX（交叉接法）
* 硬體流量控制 (CTS/RTS)：可不連接，懸空即可，不影響通訊功能。

---

## 韌體燒錄

建議採用二進位檔燒錄方式較方便。若使用原始碼燒錄方式需要先安裝 Arduino IDE 以及相關函式庫，較為麻煩。

### 原始程式碼燒錄方式
> TODO

### 二進位檔案燒錄方式
> TODO

---

## 執行方式

### 系統需求

* Windows 10/11 或 macOS 或 Linux
* Chrome/Chromium 或 Edge 瀏覽器


### 方式一：線上執行

本系統可以完全免安裝使用，只需要以 Chrome/Chromium 或 Edge 瀏覽器連接到 https://kvm.jason.tools 即可使用完整功能。

  
  
### 方式二：本機執行

除了線上使用之外，本專案也提供了可在本機運作的模式，以便應對沒有網路可以使用的環境。

> 注意事項
> 初次執行時會自動安裝必要的套件 (Windows 請事先手動安裝好 Python 3.6 以上及 OpenSSL)，並且自動產生自簽憑證，在瀏覽器自動開啟時記得允許此站台與憑證。


#### 安裝方式

Windows:
1. 至本專案的 local_run/ 資料夾手動下載 start_kvm.bat、server.py
2. 可下載至 C:\JSUSBKVM
3. 執行 start_kvm.bat，過程中會引導需要安裝 Python 與 OpenSSL
4. 完成後自動呼叫瀏覽器開啟 JTUSBKVM 使用介面。
5. 使用無誤後，可將 start_kvm.bat 捷徑放至桌面，方便日後使用

Linux/macOS:
1. 至本專案的 local_run/ 資料夾手動下載 start_kvm.sh、server.py
2. 可下載至 /opt/jtusbkvm
3. 執行 start_kvm.sh，過程中會引導需要安裝 Python 與 OpenSSL
4. 完成後自動呼叫瀏覽器開啟 JTUSBKVM 使用介面
5. 使用無誤後，可將 start_kvm.sh 在桌面建立 連結/別名/啟動器，方便日後使用

在採用本機執行時，每次執行 start_kvm 會自動先連接本程式庫，如果有新版畚會自動下載更新；若沒有網路可用則會採用先前已經下載過的本機版本運作。


---

## 使用說明

> TODO


---

## 免責聲明

本專案 (JTUSBKVM) 是基於個人興趣與研究目的而開發，以開放原始碼方式提供給社群使用。請注意：

- 本專案僅供學習、研究及個人使用，開發者不對本工具的功能完整性、穩定性或適用性提供任何明示或暗示的保證。
- 使用者需自行承擔使用本工具的一切風險，包括但不限於資料遺失、系統損壞或其他可能發生的問題。
- 開發者不對因使用或無法使用本工具而導致的任何直接或間接損失負責，包括但不限於利潤損失、業務中斷或資料損失。
- 本專案提供所有功能與原始程式碼的目的是分享知識，使用者應在符合當地法律法規的前提下使用。
- 專案內容可能會不定期更新，開發者保留隨時修改或終止服務的權利，且無需事先通知。

使用本專案表示您已閱讀、理解並同意上述免責聲明的所有條款。如不同意，請勿使用本專案。

---
