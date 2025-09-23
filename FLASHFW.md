> 本頁內容經過 ChatGPT 整理

## 二進位檔案燒錄方式（不需安裝 Arduino IDE）

> 本專案使用 **2 片 Arduino Pro Micro（ATmega32U4）**，請將 v1.0.4 釋出的 **A / B 兩個 .hex** 分別燒錄到對應的板子。建議使用 `avrdude` 直接燒錄。([GitHub][1])

**重點參數**

* MCU：`-p atmega32u4`
* Programmer：`-c avr109`（ATmega32U4 的 bootloader 協定）([learn.adafruit.com][2])
* Baud：`-b 57600`（常見 32U4 bootloader 速率）([GitHub][3])

> 小提醒：32U4 進入 bootloader 後，**序列埠會短暫換成另一個 Port，且只維持數秒**；建議先備妥指令，再「雙擊 Reset」切進 bootloader 後立即執行。某些環境也可用 **1200 bps 觸發重置** 進 bootloader。([Arduino Stack Exchange][4])

---

### Windows（PowerShell / CMD）

1. 安裝 `avrdude`（解壓後確定同資料夾內有 `avrdude.exe` 與 `avrdude.conf`）。
2. 讓 Pro Micro **雙擊 Reset** 進入 bootloader，記下此時的 **COM 埠**（會與一般運作時不同）。
3. 執行（請把 `COM8` 與檔名改成你的實際值）：

```powershell
avrdude -C C:\avrdude\avrdude.conf ^
  -p atmega32u4 -c avr109 -P COM8 -b 57600 -D ^
  -U flash:w:JTUSBKVM_A.hex:i
```

> B 板同樣執行一次，將檔名改為 `JTUSBKVM_B.hex`。

---

### macOS（Terminal）

1. 安裝：

```bash
brew install avrdude
```

2. **雙擊 Reset** 進入 bootloader，查 Port：

```bash
ls /dev/tty.usb* /dev/cu.usb*
```

3. 燒錄（修改成你的埠名與檔名）：

```bash
avrdude -p atmega32u4 -c avr109 -P /dev/cu.usbmodemXXXX -b 57600 -D \
  -U flash:w:JTUSBKVM_A.hex:i
```

> B 板同樣執行一次，將檔名改為 `JTUSBKVM_B.hex`。
> （`avr109` 為 32U4 bootloader 所用的 programmer 名稱。）([learn.adafruit.com][2])

---

### Linux（以 Debian/Ubuntu 為例）

1. 安裝：

```bash
sudo apt update
sudo apt install avrdude
```

2. **雙擊 Reset** 進入 bootloader，查 Port（常見 `/dev/ttyACM0`）：

```bash
dmesg | grep -E "ttyACM|ttyUSB" | tail
```

3. 燒錄（修改成你的埠名與檔名）：

```bash
avrdude -p atmega32u4 -c avr109 -P /dev/ttyACM0 -b 57600 -D \
  -U flash:w:JTUSBKVM_A.hex:i
```

> B 板同樣執行一次，將檔名改為 `JTUSBKVM_B.hex`。

---

#### 常見問題

* **一直連不上 / `butterfly_recv` 類錯誤**：請確認使用的是 **bootloader 的那個 Port**，且在進入 bootloader 後**立即**下指令；必要時避免經由 USB Hub。([Stack Overflow][5])
* **燒錄後沒反應**：確認 A/B 檔案是否各自燒錄到對應的那片板（本專案硬體為兩片 Pro Micro）。([GitHub][1])


[1]: https://github.com/jasoncheng7115/JTUSBKVM "GitHub - jasoncheng7115/JTUSBKVM: 自製可攜式帶線 USBKVM，搭配筆電即可成為伺服器維護最強工具人 (誤)"
[2]: https://learn.adafruit.com/atmega32u4-breakout/using-with-avrdude "Using with AVRDude | Atmega32u4 Breakout | Adafruit Learning System"
[3]: https://github.com/mariusgreuel/avrdude/issues/10 "Arduino Leonardo problem · Issue #10 · mariusgreuel/avrdude - GitHub"
[4]: https://arduino.stackexchange.com/questions/60591/cant-upload-sketch-avrdude-butterfly-recv-programmer-is-not-responding "arduino pro micro - Can't upload sketch - avrdude: butterfly_recv (): programmer is not responding - Arduino Stack Exchange"
[5]: https://stackoverflow.com/questions/49283074/arduino-leonardo-avrdude-butterfly-recv-programmer-is-not-responding "Arduino Leonardo - \"avrdude: butterfly_recv (): programmer is not responding\" - Stack Overflow"
