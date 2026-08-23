// ==============================
// Dependencies & Instantiation
// ==============================
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Create the sensor object
Adafruit_MPU6050 mpu;

// ============================
// Serial Communication Setup
// ============================
void setup() {
    // Initialize Serial output for debugging
    delay(1000);    // Wait for power & serial port to settle
    Serial.begin(115200);
    while(!Serial) {
        delay(10);  // Wait for Serial monitor connection (relevant on USB-native chips)
    }

    Serial.println("\n--- ESP32 MPU6050 Raw Acceleration Reader ---");

    // ===============================
    // Bus & Hardware Initialization
    // ===============================

    // Initialize Wire (I2C) with default pins: SDA=21, SCL=22
    Wire.begin(21, 22);

    // Initialize the MPU6050
    if (!mpu.begin()) {
        Serial.println("Failed to find MPU6050 chip! Check wiring connection.");
        while(1) {
            delay(10);  // Halt execution if sensor isn't detected
        };
    }
    Serial.println("MPU6050 initialized successfully!");

    // ================================
    // Sensor Calibration & Filtering
    // ================================
    // Set accelerometer range (2g is plenty for walking/step tracking)
    mpu.setAccelerometerRange(MPU6050_RANGE_2_G);

    // Set filter bandwidth to suppress high-frequency noise
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

    delay(100);
}

// ===============================
// Continuous Reading & Streaming
// ===============================
void loop() {
    // Container structures for sensor events
    sensors_event_t a, g, temp;

    // Read current sensor events
    mpu.getEvent(&a, &g, &temp);

    // Print raw Linear acceleration (in m/s^2) on X, Y, and Z axes
    Serial.print("Accel X: ");
    Serial.print(a.acceleration.x, 2);
    Serial.print(" m/s^2 | Y: ");
    Serial.print(a.acceleration.y, 2);
    Serial.print(" m/s^2 | Z: ");
    Serial.print(a.acceleration.z, 2);
    Serial.println(" m/s^2");

    // Sample roughly 20 times per second (50ms delay)
    delay(50);
}

