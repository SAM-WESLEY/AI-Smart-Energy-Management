/*
 * AI Smart Energy Management System — ESP32 Firmware
 * Reads PZEM-004T energy meter and sends to Flask server
 * Author: Sam Wesley S | Karunya Institute of Technology and Sciences
 */
#include <WiFi.h>
#include <HTTPClient.h>
#include <PZEM004Tv30.h>
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
#define SERVER_URL "http://YOUR_PC_IP:5000/data"
#define RELAY_PIN 17
PZEM004Tv30 pzem(Serial2, 16, 17);
void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nConnected: " + WiFi.localIP().toString());
}
void loop() {
  float v=pzem.voltage(), a=pzem.current(), w=pzem.power(), kwh=pzem.energy(), hz=pzem.frequency(), pf=pzem.pf();
  if (isnan(v)) { delay(5000); return; }
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http; http.begin(SERVER_URL); http.addHeader("Content-Type","application/json");
    String p = "{\"voltage\":"+String(v,1)+",\"current\":"+String(a,2)+",\"power\":"+String(w,1)+",\"energy_kwh\":"+String(kwh,3)+",\"frequency\":"+String(hz,1)+",\"power_factor\":"+String(pf,2)+"}";
    int code = http.POST(p);
    if (code==200 && http.getString().indexOf("relay_off")>=0) digitalWrite(RELAY_PIN,LOW);
    else digitalWrite(RELAY_PIN,HIGH);
    http.end();
  }
  delay(5000);
}