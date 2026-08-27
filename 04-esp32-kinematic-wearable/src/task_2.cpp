#include <Arduino.h>
#include <Wire.h>
#include <cmath>

// MPU6050 Register Definitions
constexpr uint8_t MPU6050_ADDR         = 0x68;
constexpr uint8_t MPU6050_PWR_MGMT_1   = 0x6B;
constexpr uint8_t MPU6050_ACCEL_CONFIG = 0x1C;
constexpr uint8_t MPU6050_ACCEL_XOUT_H = 0x3B;

// Pin Assignments & Constants
constexpr int SDA_PIN = 21;
constexpr int SCL_PIN = 22;
constexpr float ACCEL_SCALE_4G = 8192.0f; // Scale factor for +/-4g setting

// Step Detection Parameters (Tune these based on testing)
constexpr float STEP_THRESHOLD_G = 1.25f;      // Peak threshold in g-units
constexpr unsigned long STEP_COOLDOWN_MS = 300; // Minimum time between steps (ms)
constexpr int FILTER_SIZE = 5;                  // Window size for moving average

// Signal Processing Variables
float readings[FILTER_SIZE] = {0.0f};
int readIndex = 0;
float totalSum = 0.0f;

int stepCount = 0;
unsigned long lastStepTime = 0;

void writeRegister(uint8_t reg, uint8_t value) {
    Wire.beginTransmission(MPU6050_ADDR);
    Wire.write(reg);
    Wire.write(value);
    Wire.endTransmission();
}
