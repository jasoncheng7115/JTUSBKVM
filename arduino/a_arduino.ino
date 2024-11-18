/*

=========================================================================

JTUSBKVM - Arduino Board A (Source Controller)

Version: 1.0.0
Last Update: 2024-11-18

Author: Jason Cheng
E-mail: jason@jason.tools
GitHub: https://github.com/jasoncheng7115

License: GNU Affero General Public License v3.0
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
any later version.

=========================================================================

*/

void setup() {
   Serial.begin(115200);    // Serial communication with webpage
   Serial1.begin(115200);   // Serial communication with Arduino B
}

void loop() {
   // Receive data from webpage and forward to Arduino B
   if (Serial.available()) {
       String data = Serial.readStringUntil('\n');
       Serial1.println(data);
   }

   // Receive data from Arduino B (if needed)
   if (Serial1.available()) {
       String data = Serial1.readStringUntil('\n');
       // Process received data (if needed)
   }
}
