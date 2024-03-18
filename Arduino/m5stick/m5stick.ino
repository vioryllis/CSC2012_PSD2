#include <WiFi.h>
#include <M5StickCPlus.h> // Include M5StickCPlus library
#include <HTTPClient.h>

const char* ssid = "cookiie";
const char* password = "rllr4884";
const char* serverName = "http://192.168.133.159:8000/api/data";

void setup() {
  M5.begin();
  M5.Lcd.setRotation(1); // Set display rotation if necessary
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
}

void loop() {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Example payload
    String httpRequestData = "{\"sensor\":\"temperature\",\"value\":23.4}";

    int httpResponseCode = http.POST(httpRequestData);

    if(httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);

      // Display temperature and response on the M5StickC Plus
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextSize(2);
      M5.Lcd.setTextColor(WHITE);
      M5.Lcd.setCursor(0, 0);
      M5.Lcd.println("Temperature:");
      M5.Lcd.println("Response:");
      M5.Lcd.setTextSize(1);
      M5.Lcd.println(httpResponseCode);
      M5.Lcd.println(response);
    }
    else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }
  else {
    Serial.println("WiFi Disconnected");
  }
  delay(10000); // Send data every 10 seconds
}