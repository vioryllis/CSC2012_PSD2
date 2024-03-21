#include <WiFi.h>
#include <M5StickCPlus.h> // Include M5StickCPlus library
#include <HTTPClient.h>

const char* ssid = "cookiie";
const char* password = "rllr4884";
const char* serverName = "http://192.168.133.159:8000/api/data"; // POST url
const char* sendServer = "http://192.168.133.159:8000/api/water_plant/"; // GET url

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

    // POST REQUEST
    String postRequestData = "{\"sensor\":\"temperature\",\"value\":23.4}";
    int postResponseCode = http.POST(postRequestData);

    if(postResponseCode > 0) {
      String post_response = http.getString();
      Serial.println("POST Success:");
      Serial.println(postResponseCode);
      Serial.println(post_response);

      // Display temperature and response on the M5StickC Plus
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextSize(2);
      M5.Lcd.setTextColor(WHITE);
      M5.Lcd.setCursor(0, 0);
      M5.Lcd.println("Temperature:");
      M5.Lcd.println("Response:");
      M5.Lcd.setTextSize(1);
      M5.Lcd.println(postResponseCode);
      M5.Lcd.println(post_response);
    }
    else {
      Serial.print("Error on sending POST: ");
      Serial.println(postResponseCode);
      Serial.println(http.errorToString(postResponseCode));
    }

    http.end();

    // Delay before initiating the GET request
    delay(1000);

    // GET REQUEST
    HTTPClient http_get;
    http_get.begin(sendServer);
    http_get.addHeader("Content-Type", "application/json");

    int getResponseCode = http_get.GET();
    
    if(getResponseCode > 0) {
      String get_response = http_get.getString();
      Serial.println(getResponseCode);
      Serial.println(get_response);

      // Display response on the M5StickC Plus
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextSize(2);
      M5.Lcd.setTextColor(WHITE);
      M5.Lcd.setCursor(0, 0);
      M5.Lcd.println("Response:");
      M5.Lcd.setTextSize(1);
      M5.Lcd.println(getResponseCode);
      M5.Lcd.println(get_response);
    }
    else {
      Serial.print("Error on sending GET: ");
      Serial.println(getResponseCode);
    }

    http_get.end();
  }

  else {
    Serial.println("WiFi Disconnected");
  }
  delay(10000); // Send data every 10 seconds
}