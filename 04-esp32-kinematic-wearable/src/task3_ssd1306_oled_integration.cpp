#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <cmath>

// Display Specifications
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDR 0x3C

// Hardware Pins
constexpr int SDA_PIN = 21;
constexpr int SCL_PIN = 22;

// Step Detection Parameters
constexpr float STEP_THRESHOLD_MS2 = 11.2f;
constexpr unsigned long STEP_COOLDOWN_MS = 300;
constexpr int FILTER_SIZE = 5;

// Hardware Objects
Adafruit_MPU6050 mpu;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Signal Processing Variables
float readings[FILTER_SIZE] = {0.0f};
int readIndex = 0;
float totalSum = 0.0f;

int stepCount = 0;
unsigned long lastStepTime = 0;

void updateDisplay(float mag, int steps) {
    display.clearDisplay();
    
    // Header Title
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(18, 0);
    display.println("FITNESS TRACKER");
    display.drawFastHLine(0, 10, 128, SSD1306_WHITE);

    // Large Step Counter Display
    display.setCursor(0, 18);
    display.print("STEPS:");
    display.setTextSize(2);
    display.setCursor(0, 30);
    display.print(steps);

    // Sensor Telemetry Line
    display.setTextSize(1);
    display.setCursor(0, 52);
    display.print("Mag: ");
    display.print(mag, 1);
    display.print(" m/s^2");

    display.display();
}

void setup() {
    Serial.begin(115200);
    while (!Serial) delay(10);

    Wire.begin(SDA_PIN, SCL_PIN, 100000);

    // Initialize MPU6050
    if (!mpu.begin(0x68, &Wire)) {
        Serial.println("[ERROR] MPU6050 not found!");
        while (1) delay(10);
    }
    mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

    // Initialize SSD1306 Display
    if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
        Serial.println("[ERROR] SSD1306 allocation failed!");
        while (1) delay(10);
    }

    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);
    display.setCursor(15, 25);
    display.println("System Starting...");
    display.display();
    delay(1000);
}

void loop() {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // 1. Calculate Vector Magnitude
    float rawMag = sqrt(a.acceleration.x * a.acceleration.x +
                        a.acceleration.y * a.acceleration.y +
                        a.acceleration.z * a.acceleration.z);

    // 2. Filter Signal
    totalSum -= readings[readIndex];
    readings[readIndex] = rawMag;
    totalSum += readings[readIndex];
    readIndex = (readIndex + 1) % FILTER_SIZE;
    float filteredMag = totalSum / FILTER_SIZE;

    // 3. Step Logic
    unsigned long currentTime = millis();
    if (filteredMag > STEP_THRESHOLD_MS2 && (currentTime - lastStepTime > STEP_COOLDOWN_MS)) {
        stepCount++;
        lastStepTime = currentTime;
    }

    // 4. Refresh Screen at 10 Hz (every 100 ms) to avoid I2C bottlenecking
    static unsigned long lastDisplayTime = 0;
    if (currentTime - lastDisplayTime >= 100) {
        lastDisplayTime = currentTime;
        updateDisplay(filteredMag, stepCount);
    }

    delay(20); // ~50 Hz sampling rate
}
