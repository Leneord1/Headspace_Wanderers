#include <Wire.h>
#include "RTClib.h"
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

RTC_DS3231 rtc;
DHT dht(DHTPIN, DHTTYPE);

// Logging intervals
const unsigned long READ_INTERVAL = 30000;   // 30 seconds
const unsigned long PRINT_INTERVAL = 60000; // 10 minutes

unsigned long lastReadTime = 0;
unsigned long lastPrintTime = 0;

String logBuffer = "";  // Stores 20 readings (10 minutes)

String formatCSV(DateTime now, float temp, float hum) {
    String line = "";
    line += String(now.year()) + "-";
    line += String(now.month()) + "-";
    line += String(now.day()) + " ";
    line += String(now.hour()) + ":";
    line += String(now.minute()) + ":";
    line += String(now.second()) + ",";
    line += String(temp, 2) + ",";
    line += String(hum, 2);
    return line;
}

void setup() {
    Serial.begin(9600);
    Wire.begin();
    dht.begin();

    if (!rtc.begin()) {
        Serial.println("RTC not found");
        while (1);
    }

    // Set RTC once, then comment out
    // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));

    Serial.println("timestamp,temperature_c,humidity_percent");

    lastReadTime = millis();
    lastPrintTime = millis();
}

void loop() {
    unsigned long nowMillis = millis();

    // Read sensors every 30 seconds
    if (nowMillis - lastReadTime >= READ_INTERVAL) {
        lastReadTime = nowMillis;

        DateTime now = rtc.now();
        float temp = dht.readTemperature();
        float hum = dht.readHumidity();

        String csvLine = formatCSV(now, temp, hum);
        logBuffer += csvLine + "\n";  // Append to buffer
    }

    // Print buffer every 10 minutes
    if (nowMillis - lastPrintTime >= PRINT_INTERVAL) {
        lastPrintTime = nowMillis;

        Serial.print(logBuffer);  // Dump all readings at once
        logBuffer = "";           // Clear buffer
    }
}
