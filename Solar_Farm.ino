/***************************************************
 * Smart Energy Panel Monitor (6.9V Solar Panels)
 * Panels: A,B,C Voltage, D Current
 * LED: AB combined, C only
 ***************************************************/

// Credentials live in secrets.h (gitignored). Copy secrets.example.h to secrets.h
// next to this sketch and fill in your own values. It must define BLYNK_TEMPLATE_ID,
// BLYNK_TEMPLATE_NAME and BLYNK_AUTH_TOKEN before BlynkSimpleEsp32.h is included.
#include "secrets.h"

#include <WiFi.h>
#include <WebServer.h>
#include <BlynkSimpleEsp32.h>

// Wi-Fi
char ssid[] = WIFI_SSID;
char pass[] = WIFI_PASS;

// Pins
#define VOLTAGE_A 34
#define VOLTAGE_B 35
#define VOLTAGE_C 32
#define CURRENT_D 33

#define RED_AB 14
#define YELLOW_AB 12
#define GREEN_AB 13

#define RED_CD 25
#define YELLOW_CD 26
#define GREEN_CD 27

BlynkTimer timer;
WebServer server(80);

// Connectivity (F5): never block boot on Wi-Fi or Blynk.
#define WIFI_CONNECT_TIMEOUT_MS 15000UL
#define WIFI_RETRY_INTERVAL_MS  10000UL
#define BLYNK_CONNECT_TIMEOUT_MS 5000UL
unsigned long lastWifiRetry = 0;

// ---------------- Calibration (F4) ----------------
// The ESP32 ADC reads 0-3.3 V. Raw analogRead() codes carry a dead zone near 0 V,
// gain error and saturation near 3.1 V, so readings use the eFuse-calibrated
// analogReadMilliVolts() instead.
// Panel voltages: resistive divider maps 0-10 V at the panel to 0-3.3 V at the pin.
#define VOLTAGE_DIVIDER_GAIN (10.0 / 3.3)
// ACS712-05B output (2.5 V at 0 A, up to 5 V) MUST reach GPIO 33 through a 2:3 divider
// (10 kOhm series, 20 kOhm to GND) to stay inside the ESP32's input range.
#define ACS_DIVIDER_RATIO (2.0 / 3.0)
#define ACS_ZERO_MV 2500.0   // sensor output at 0 A; trim per board (README: Calibrate current)
#define ACS_MV_PER_A 185.0   // ACS712-05B sensitivity

// ---------------- Voltage & Current Reading ----------------
float readVoltage(int pin) {
  uint32_t mv = analogReadMilliVolts(pin);
  float voltage = (mv / 1000.0) * VOLTAGE_DIVIDER_GAIN; // 6.9V panels, sensorMax ~10V
  return voltage;
}

float readCurrent(int pin) {
  uint32_t mv = analogReadMilliVolts(pin);
  float sensorMv = mv / ACS_DIVIDER_RATIO;  // undo the 2:3 divider
  float current = (sensorMv - ACS_ZERO_MV) / ACS_MV_PER_A; // ACS712 5A
  if(current < 0) current = 0; // ignore small negatives
  return current;
}

// ---------------- Classification ----------------
// Same thresholds as the LEDs: <= 1.0 V RED, < 5.0 V YELLOW, otherwise GREEN.
String classifyVoltage(float v) {
  if(v <= 1.0) return "RED: No Voltage";
  if(v < 5.0) return "YELLOW: Low Voltage";
  return "GREEN: Normal";
}

// ---------------- LED Control ----------------
String statusAB, statusC;

// AB group health = its weakest panel, so one failing panel (e.g. a dead B next to a
// healthy A) raises the alarm instead of being averaged away.
float groupAB(float voltageA, float voltageB) {
  return (voltageA < voltageB) ? voltageA : voltageB;
}

void updateLEDs(float voltageA, float voltageB, float voltageC) {
  // AB group: weakest of A and B
  float combinedAB = groupAB(voltageA, voltageB);
  if(combinedAB <= 1.0){
    digitalWrite(RED_AB,HIGH); digitalWrite(YELLOW_AB,LOW); digitalWrite(GREEN_AB,LOW);
    statusAB = "RED: No Voltage";
  } else if(combinedAB < 5.0){
    digitalWrite(RED_AB,LOW); digitalWrite(YELLOW_AB,HIGH); digitalWrite(GREEN_AB,LOW);
    statusAB = "YELLOW: Low Voltage";
  } else {
    digitalWrite(RED_AB,LOW); digitalWrite(YELLOW_AB,LOW); digitalWrite(GREEN_AB,HIGH);
    statusAB = "GREEN: Normal";
  }

  // C Only
  if(voltageC <= 1.0){
    digitalWrite(RED_CD,HIGH); digitalWrite(YELLOW_CD,LOW); digitalWrite(GREEN_CD,LOW);
    statusC = "RED: No Voltage";
  } else if(voltageC < 5.0){
    digitalWrite(RED_CD,LOW); digitalWrite(YELLOW_CD,HIGH); digitalWrite(GREEN_CD,LOW);
    statusC = "YELLOW: Low Voltage";
  } else {
    digitalWrite(RED_CD,LOW); digitalWrite(YELLOW_CD,LOW); digitalWrite(GREEN_CD,HIGH);
    statusC = "GREEN: Normal";
  }
}

// ---------------- Send Data ----------------
void sendData() {
  float voltageA = readVoltage(VOLTAGE_A);
  float voltageB = readVoltage(VOLTAGE_B);
  float voltageC = readVoltage(VOLTAGE_C);
  float currentD = readCurrent(CURRENT_D);

  Blynk.virtualWrite(V0, voltageA);
  Blynk.virtualWrite(V1, voltageB);
  Blynk.virtualWrite(V2, voltageC);
  Blynk.virtualWrite(V3, currentD);

  updateLEDs(voltageA, voltageB, voltageC);

  Blynk.virtualWrite(V4, statusAB);
  Blynk.virtualWrite(V5, statusC);

  Serial.printf("A: %.2f V | B: %.2f V | C: %.2f V | D Current: %.2f A\n", voltageA, voltageB, voltageC, currentD);
}

// ---------------- API ----------------
void handleAPI(){
  float voltageA = readVoltage(VOLTAGE_A);
  float voltageB = readVoltage(VOLTAGE_B);
  float voltageC = readVoltage(VOLTAGE_C);
  float currentD = readCurrent(CURRENT_D);

  // Classify the readings returned in this response, not the last timer tick's
  // (otherwise status is empty before the first tick and up to 2 s stale).
  String apiStatusAB = classifyVoltage(groupAB(voltageA, voltageB));
  String apiStatusC = classifyVoltage(voltageC);

  String json = "{";
  json += "\"PanelA_Voltage\":" + String(voltageA,2) + ",";
  json += "\"PanelB_Voltage\":" + String(voltageB,2) + ",";
  json += "\"PanelC_Voltage\":" + String(voltageC,2) + ",";
  json += "\"PanelD_Current\":" + String(currentD,2) + ",";
  json += "\"Status_PanelAB\":\"" + apiStatusAB + "\",";
  json += "\"Status_PanelC\":\"" + apiStatusC + "\",";
  // Per-panel detail (appended, so existing consumers keep working)
  json += "\"Status_PanelA\":\"" + classifyVoltage(voltageA) + "\",";
  json += "\"Status_PanelB\":\"" + classifyVoltage(voltageB) + "\"";
  json += "}";

  // Allow browser dashboards opened from file:// or another origin (index.html) to read /api.
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200,"application/json",json);
}

// ---------------- Setup ----------------
void setup() {
  Serial.begin(115200);

  pinMode(RED_AB,OUTPUT); pinMode(YELLOW_AB,OUTPUT); pinMode(GREEN_AB,OUTPUT);
  pinMode(RED_CD,OUTPUT); pinMode(YELLOW_CD,OUTPUT); pinMode(GREEN_CD,OUTPUT);

  // Bounded Wi-Fi wait: boot even when the network is down so the LEDs, Serial log
  // and (once Wi-Fi returns) /api keep working. Blynk.begin() would block forever.
  WiFi.begin(ssid,pass);
  Serial.print("Connecting WiFi");
  unsigned long wifiStart = millis();
  while(WiFi.status()!=WL_CONNECTED && millis() - wifiStart < WIFI_CONNECT_TIMEOUT_MS){delay(500); Serial.print(".");}
  if(WiFi.status()==WL_CONNECTED){
    Serial.println("\nWi-Fi Connected! IP: "); Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWi-Fi unavailable - running offline, will keep retrying");
  }

  Blynk.config(BLYNK_AUTH_TOKEN);
  if(WiFi.status()==WL_CONNECTED) Blynk.connect(BLYNK_CONNECT_TIMEOUT_MS);

  server.on("/api",handleAPI);
  server.begin();
  Serial.println("API Ready");

  timer.setInterval(2000L, sendData);
}

// ---------------- Loop ----------------
void loop(){
  if(WiFi.status()!=WL_CONNECTED && millis() - lastWifiRetry >= WIFI_RETRY_INTERVAL_MS){
    lastWifiRetry = millis();
    WiFi.reconnect();
  }
  if(WiFi.status()==WL_CONNECTED) Blynk.run();  // Blynk.run() reconnects to the cloud itself
  timer.run();
  server.handleClient();
}

