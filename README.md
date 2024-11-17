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
* 顯示訊號輸入 (BIOS 等級)，可輸入 1080P (4K 應該也可以收，沒測過)
* 鍵盤、滑鼠操作

### 軟體功能
* 被控端畫面顯示
* 送出鍵盤與滑鼠操作，包括滑鼠滾輪行為
* 支援功能鍵、特殊鍵與修飾鍵
* 支援貼上功能，可一次送出一批指令
* 具擷圖、錄影功能
  
---

## 組成

### 硬體組成
* Arduino Pro Micro 開發板 x 2
* HDMI 影像擷取器 x 1 
* VGA to HDMI 轉接頭 x 1
* Type C USB Hub x 1
* Type C 延長線 1M x 1
* HDMI 0.3M 線材 x 1
* MicroUSB to TypeA 0.3M 線材 x 2
* 透明收納盒 x 1
* 全都在蝦皮購入，成本合計大約 一千一

### 軟體組成
* 控制端與被控端免安裝任何軟體
* 純前端 HTML + CSS + JavaScript
* 完全無後端程式碼，均在使用者本機運作
* 視訊輸入採用瀏覽器標準 MediaStream API
* 控制器連接採用瀏覽器標準  Web Serial API
* Web 面我還沒放到外網，暫時只有我這內網可以連，之後會開放
* Arduino 程式碼分為 A B 兩片開發板，已先釋出 A 板

---

## 實例


連接控制 Windows 主機擷圖

![控制 Windows 主機擷圖](https://raw.githubusercontent.com/jasoncheng7115/JTUSBKVM/refs/heads/main/screenshot/4%20windows.png)

連接控制 Linux 主機擷圖

![控制 Linux 主機擷圖](https://raw.githubusercontent.com/jasoncheng7115/JTUSBKVM/refs/heads/main/screenshot/3%20linux.png)

連接控制 Linux 主機錄影

![控制 Linux 主機錄影](https://github.com/jasoncheng7115/JTUSBKVM/blob/main/screenshot/6%20linux_ok_cut.gif?raw=true)


連接控制 Windows 主機錄影

![控制 Windows 主機錄影](https://github.com/jasoncheng7115/JTUSBKVM/blob/main/screenshot/5%20windows_ok_cut.gif?raw=true)
