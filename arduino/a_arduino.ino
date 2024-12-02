/*
=========================================================================
JTUSBKVM - Arduino Board A (Source Controller)
Version: 1.0.4
Last Update: 2024-12-01

Author: Jason Cheng
E-mail: jason@jason.tools
GitHub: https://github.com/jasoncheng7115

License: GNU Affero General Public License v3.0
=========================================================================
*/

#include <SoftwareSerial.h>

// 使用實體 Pin 腳編號 RX=9, TX=8
SoftwareSerial boardBSerial(9, 8);  // Arduino B 通訊

String inputBuffer = "";         // 用於收集完整輸入指令
bool collectingCommand = false;  // 標記是否正在收集指令

void setup() {
   boardBSerial.begin(19200);   // Arduino B 通訊，19200
   Serial.begin(115200);        // USB 與控制端 PC 通訊，保持 115200
   Serial1.begin(9600);         // RS232 預設速率
   
   // 等待 USB Serial 準備好
   // while(!Serial);           

   // 改為加入 Timeout 機制
   unsigned long startTime = millis();
   while(!Serial && (millis() - startTime < 2000)); // 最多等待 2 秒
   
   // 清空所有緩衝區
   while(Serial.available()) Serial.read();
   while(boardBSerial.available()) boardBSerial.read();
   while(Serial1.available()) Serial1.read();
   
   delay(100);  // 等待穩定
}

void loop() {
   // 從 RS232 讀取並發送到 USB 往控制端 PC
   if (Serial1.available()) {
       char c = Serial1.read();
       Serial.write(c);
   }

   // 從 USB 讀取並依據前置判斷路由
   if (Serial.available()) {
       char c = Serial.read();

       if (collectingCommand) {
           // 正在收集 B: 指令
           inputBuffer += c;
           if (c == '\n') {
               // 指令收集完成，傳送到 B Arduino
               boardBSerial.print(inputBuffer);
               inputBuffer = "";
               collectingCommand = false;
           }
       }
       else if (c == 'B') {
           // 開始收集 B: 指令
           if (Serial.peek() == ':') {  // 檢查下一個字元是否為 ':'
               Serial.read();  // 讀取 ':'
               collectingCommand = true;
               inputBuffer = "";  // 清空緩衝區開始收集新指令
           }
       }
       else if (c == 'R') {
           if (Serial.peek() == ':') {  // 檢查下一個字元是否為 ':'
               Serial.read();  // 讀取 ':'
               String cmd = "";
               // 檢查是否是速率設定指令
               while (Serial.available()) {
                   char nextChar = Serial.read();
                   cmd += nextChar;
                   if (nextChar == '\n') break;
               }
               
               if (cmd.startsWith("BAUD=")) {
                   // 處理速率設定
                   long baudRate = cmd.substring(5).toInt();
                   if (baudRate > 0) {
                       Serial1.end();           // 先關閉連接埠
                       delay(10);               // 等待連接埠關閉
                       Serial1.begin(baudRate); // 以新速率重新開啟
                       delay(10);               // 等待連接埠穩定
                   }
               } else {
                   // 一般 RS232 指令，逐字元發送
                   for(int i = 0; i < cmd.length(); i++) {
                       Serial1.write(cmd[i]);
                       delay(1);
                   }
               }
           }
       }
   }
}
