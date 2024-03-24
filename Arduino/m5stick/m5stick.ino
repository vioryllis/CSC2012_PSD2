#include <WiFi.h>
#include <M5StickCPlus.h>
#include <HTTPClient.h>

// change accordingly to connect your own network
const char* ssid = "NETWORK_NAME";
const char* password = "NETWORK_PW"; 

// change to own ip address eg. "http://IPADDRESS:8000/api/data"
const char* serverName = "http://192.168.248.159:8000/api/data"; // POST url
const char* waterPlant = "http://192.168.248.159:8000/api/water_plant/"; // GET url
const char* fertilizePlant = "http://192.168.248.159:8000/api/fertilize_plant/"; // GET url
const char* plantSettings = "http://192.168.248.159:8000/api/water_plant_amt/"; // GET url

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
    String postRequestData = "{\"water_level\":10.5,\"nutrient_level\":5.2,\"plant_id\":17}";
    int postResponseCode = http.POST(postRequestData);

    if(postResponseCode > 0) {
      String post_response = http.getString();
      Serial.println("POST Success:");
      Serial.println(postResponseCode);
      Serial.println(post_response);
      Serial.println(postRequestData);

      // Display temperature and response on the M5StickC Plus
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextSize(2);
      M5.Lcd.setTextColor(WHITE);
      M5.Lcd.setCursor(0, 0);
      M5.Lcd.println("Response:");
      M5.Lcd.setTextSize(1);
      M5.Lcd.println(postResponseCode);
      M5.Lcd.println(post_response);
      M5.Lcd.println(postRequestData);
    }
    else {
      Serial.print("Error on sending POST: ");
      Serial.println(postResponseCode);
      Serial.println(http.errorToString(postResponseCode));
    }

    http.end();
    
    Delay before initiating the GET request
    delay(1000);

    //===================================================================
    // GET REQUEST (for water plant)
    HTTPClient http_water;
    http_water.begin(waterPlant);
    http_water.addHeader("Content-Type", "application/json");

    int getWater = http_water.GET();
    
    if(getWater > 0) {
      String get_water = http_water.getString();
      Serial.println(getWater);
      Serial.println(get_water);

      // Display response on the M5StickC Plus
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextSize(2);
      M5.Lcd.setTextColor(WHITE);
      M5.Lcd.setCursor(0, 0);
      M5.Lcd.println("Response:");
      M5.Lcd.setTextSize(1);
      M5.Lcd.println(getWater);
      M5.Lcd.println(get_water);
    }
    else {
      Serial.print("Error on sending GET: ");
      Serial.println(getWater);
    }

    http_water.end();

    delay(1000);

    //===================================================================
    // GET REQUEST (for fertilize plant)
    HTTPClient http_fertilize;
    http_fertilize.begin(fertilizePlant);
    http_fertilize.addHeader("Content-Type", "application/json");

    int getFertilizer = http_fertilize.GET();
    
    if(getFertilizer > 0) {
      String get_fertilizer = http_fertilize.getString();
      Serial.println(getFertilizer);
      Serial.println(get_fertilizer);

      // Display response on the M5StickC Plus
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextSize(2);
      M5.Lcd.setTextColor(WHITE);
      M5.Lcd.setCursor(0, 0);
      M5.Lcd.println("Response:");
      M5.Lcd.setTextSize(1);
      M5.Lcd.println(getFertilizer);
      M5.Lcd.println(get_fertilizer);
    }
    else {
      Serial.print("Error on sending GET: ");
      Serial.println(getFertilizer);
    }

    http_fertilize.end();

    delay(1000);

    //===================================================================
    // GET REQUEST (for plant settings)
    HTTPClient http_settings;
    http_settings.begin(plantSettings);
    http_settings.addHeader("Content-Type", "application/json");

    int getSettings = http_settings.GET();
    
    if(getSettings > 0) {
      String get_Settings = http_settings.getString();
      Serial.println(getSettings);
      Serial.println(get_Settings);

      // Display response on the M5StickC Plus
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextSize(2);
      M5.Lcd.setTextColor(WHITE);
      M5.Lcd.setCursor(0, 0);
      M5.Lcd.println("Response:");
      M5.Lcd.setTextSize(1);
      M5.Lcd.println(getSettings);
      M5.Lcd.println(get_Settings);
    }
    else {
      Serial.print("Error on sending GET: ");
      Serial.println(getSettings);
    }

    http_settings.end();
  }

  else {
    Serial.println("WiFi Disconnected");
  }
  delay(10000); // Send data every 10 seconds
}