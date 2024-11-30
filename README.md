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
* 一條 USB C 線接至控制端電腦 (搭配 TYPE A 轉接頭)
* 一條 USB A 及 HDMI 線接至被控端電腦 (搭配 VGA 轉接頭)
* 顯示訊號輸入 (BIOS 等級)，可輸入 1920x1080 (最高可能支援 4K，未測)
* 鍵盤、滑鼠操作
* 一條 RJ45 終端機控制線，可連接至網路設備 RJ45 Console 連接埠

### 軟體功能
* 被控端畫面顯示
* 送出鍵盤與滑鼠操作，包括滑鼠滾輪行為
* 支援功能鍵、特殊鍵與修飾鍵
* 支援貼上功能，可一次送出一批指令 (僅限英文、數字、符號，中日韓文等無法送出)
* 具擷圖、錄影功能
* 支援 Windows、Linux、macOS，搭配 Chrome、Chromium 或 Edge 瀏覽器
* 網路設備 Console 連線設定終端機
  
---

## 組成

硬體雛形版本
![硬體雛形版本](https://github.com/jasoncheng7115/JTUSBKVM/blob/main/screenshot/1%20%E5%85%A8%E9%85%8D.JPG?raw=true)



### 硬體組成
* Arduino Pro Micro 開發板 x 2
* SP3232 RS232 轉接板 x 1
* HDMI 影像擷取器 x 1 
* VGA to HDMI 轉接頭 x 1
* Type C USB Hub x 1
* Type C 延長線 1M x 1
* HDMI 0.3M 線材 x 1
* DB9 to RJ45 轉接線 x 1
* MicroUSB to TypeA 0.3M 線材 x 2
* 透明收納盒 x 1
* 全都在蝦皮購入，成本合計大約 一千二

### 軟體組成
* 控制端與被控端免安裝任何軟體
* 純前端 HTML + CSS + JavaScript
* 完全無後端程式碼，均在使用者本機運作
* 視訊輸入採用瀏覽器標準 MediaStream API
* 控制器連接採用瀏覽器標準 Web Serial API
* Web 控制端頁面可使用我的 https://kvm.jason.tools
* Web 控制端頁面也可以使用我撰寫的離線應用程式，說明待撰寫 (local_run 下)

### 韌體組成
* Arduino 程式碼分為 A B 兩片開發板，已先釋出 A 板，`B 板要過段時日` (個人考量)
 
  
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

## 接線圖

> TODO
>


---

## 使用說明

> TODO


---

## 本機執行

> TODO

