#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <cmath>

// Hardware Pin Definitions
constexpr int SDA_PIN = 21;
constexpr int SCL_PIN = 22;

// Sensor & Step Detection Parameters
constexpr float STEP_THRESHOLD_MS2 = 11.2f;    // Threshold in m/s^2 (at rest = ~9.81 m/s^2)
constexpr unsigned long STEP_COOLDOWN_MS = 300; // Minimum time between steps
constexpr int FILTER_SIZE = 5;                  // Moving-average window size

// Global Objects & Variables
Adafruit_MPU6050 mpu;

float readings[FILTER_SIZE] = {0.0f};
int readIndex = 0;
float totalSum = 0.0f;

int stepCount = 0;
unsigned long lastStepTime = 0;

void setup() {
    Serial.begin(115200);
    while (!Serial) delay(10);

    Serial.println("\n--- Task 2: Step Detection Logic ---");

    Wire.begin(SDA_PIN, SCL_PIN, 100000);

    if (!mpu.begin(0x68, &Wire)) {
        Serial.println("[ERROR] MPU6050 not found! Check wiring connections.");
        while (1) delay(10);
    }

    // Configure sensor settings
    mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ); // Enable internal hardware low-pass filter

    Serial.println("[MPU6050] Driver initialized successfully!");
    delay(100);
}

void loop() {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // 1. Calculate 3D Vector Magnitude (m/s^2)
    float rawMag = sqrt(a.acceleration.x * a.acceleration.x +
                        a.acceleration.y * a.acceleration.y +
                        a.acceleration.z * a.acceleration.z);

    // 2. Moving Average Filter
    totalSum -= readings[readIndex];
    readings[readIndex] = rawMag;
    totalSum += readings[readIndex];
    readIndex = (readIndex + 1) % FILTER_SIZE;
    float filteredMag = totalSum / FILTER_SIZE;

    // 3. Step Detection Logic (sampled every 20ms)
    unsigned long currentTime = millis();
    if (filteredMag > STEP_THRESHOLD_MS2 && (currentTime - lastStepTime > STEP_COOLDOWN_MS)) {
        stepCount++;
        lastStepTime = currentTime;

        Serial.print(">> STEP DETECTED! << Total Steps: ");
        Serial.println(stepCount);
    }

    // 4. Slow down output printing (prints once every 250 ms)
    static unsigned long lastPrintTime = 0;
    if (currentTime - lastPrintTime >= 250) {
        lastPrintTime = currentTime;
        
        Serial.print("Mag: ");
        Serial.print(filteredMag, 2);
        Serial.print(" m/s^2 | Steps: ");
        Serial.println(stepCount);
    }

    delay(20); // ~50 Hz sampling rate for accurate peak detection
}
