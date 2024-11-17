/*
* Developer: Jason Cheng
* Email: jason@jason.tools
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
