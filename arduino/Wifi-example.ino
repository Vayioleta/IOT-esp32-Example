#include <WiFi.h>
const char* ssid = "TuSSID";
const char* password = "TuContraseña";

void setup() {
  Serial.begin(115200);
  // Conexión a WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conexión exitosa a WiFi");
}
