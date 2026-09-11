#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <cmath>

// OLED Display Configuration
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

// Custom BLE UUIDs
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

// Hardware & Service Objects
Adafruit_MPU6050 mpu;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

BLEServer* pServer = nullptr;
BLECharacteristic* pCharacteristic = nullptr;
bool deviceConnected = false;

// Signal Processing Variables
float readings[FILTER_SIZE] = {0.0f};
int readIndex = 0;
float totalSum = 0.0f;

int stepCount = 0;
unsigned long lastStepTime = 0;

// BLE Server Callbacks
class MyServerCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) override {
        deviceConnected = true;
        Serial.println("[BLE] Client Connected!");
    }

    void onDisconnect(BLEServer* pServer) override {
        deviceConnected = false;
        Serial.println("[BLE] Client Disconnected. Restarting Advertising...");
        pServer->startAdvertising(); // Resume advertising when client drops
    }
};

void updateDisplay(float mag, int steps, bool bleConnected) {
    display.clearDisplay();

    // Header Title
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.print("TRACKER");

    // BLE Connection Status Indicator
    display.setCursor(85, 0);
    if (bleConnected) {
        display.print("[BLE]");
    } else {
        display.print("[---]");
    }

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

void initBLE() {
    BLEDevice::init("ESP32_StepTracker");

    pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());

    BLEService* pService = pServer->createService(SERVICE_UUID);

    pCharacteristic = pService->createCharacteristic(
        CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
    );

    pCharacteristic->addDescriptor(new BLE2902());

    // Initial value setup
    pCharacteristic->setValue(stepCount);

    pService->start();

    BLEAdvertising* pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->setScanResponse(true);
    pAdvertising->setMinPreferred(0x06); // Functions for iPhone connection stability
    pAdvertising->setMinPreferred(0x12);
    BLEDevice::startAdvertising();

    Serial.println("[BLE] Service active and advertising as 'ESP32_StepTracker'");
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

    // Initialize Display
    if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
        Serial.println("[ERROR] SSD1306 allocation failed!");
        while (1) delay(10);
    }

    // Initialize BLE Server
    initBLE();

    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);
    display.setCursor(15, 25);
    display.println("BLE Step Tracker Ready");
    display.display();
    delay(1000);
}

void loop() {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // 1. Vector Magnitude Calculation
    float rawMag = sqrt(a.acceleration.x * a.acceleration.x +
                        a.acceleration.y * a.acceleration.y +
                        a.acceleration.z * a.acceleration.z);

    // 2. Filter Signal
    totalSum -= readings[readIndex];
    readings[readIndex] = rawMag;
    totalSum += readings[readIndex];
    readIndex = (readIndex + 1) % FILTER_SIZE;
    float filteredMag = totalSum / FILTER_SIZE;

    // 3. Step Logic & BLE Notification Update
    unsigned long currentTime = millis();
    if (filteredMag > STEP_THRESHOLD_MS2 && (currentTime - lastStepTime > STEP_COOLDOWN_MS)) {
        stepCount++;
        lastStepTime = currentTime;

        // Broadcast step value via BLE if a device is connected
        if (deviceConnected) {
            pCharacteristic->setValue(stepCount);
            pCharacteristic->notify();
            Serial.print("[BLE] Notified step count: ");
            Serial.println(stepCount);
        }
    }

    // 4. Update Screen at 10 Hz
    static unsigned long lastDisplayTime = 0;
    if (currentTime - lastDisplayTime >= 100) {
        lastDisplayTime = currentTime;
        updateDisplay(filteredMag, stepCount, deviceConnected);
    }

    delay(20); // ~50 Hz sampling rate
}
