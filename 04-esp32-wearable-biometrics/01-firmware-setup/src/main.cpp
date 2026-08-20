#include <Arduino.h>

void setup() {
  // Initialize Serial communication at 115200 baud rate
  Serial.begin(115200);
  
  // Wait a moment for serial connection to stabilize
  delay(1000);
  
  Serial.println("--- Task 1: ESP32 Baseline Setup ---");
  Serial.println("GPIO and Serial Communication Verified.");
}

void loop() {
  // Simple heartbeat message to verify main loop execution
  Serial.println("ESP32 system running...");
  delay(2000);
}
