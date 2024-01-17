#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configuracion
const char* ssid = "my-wifi";
const char* password = "password-wifi";
const char* apiEndpoint = "http://192.168.10.12:8000"; // Coloca la URL de la API aquí <- la ip del host donde se ejecuta el servidor de python

// JSON para almacenar informacion del sensor
DynamicJsonDocument doc(1024);

void setup() {
  Serial.begin(115200);
   // Conectar con el Wifi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conexión exitosa a WiFi");
  Serial.println( WiFi.localIP() );
}

void send_data() {
  HTTPClient http;
  Serial.println("Enviando datos por POST...");
  http.begin(apiEndpoint);
  // Configurar cabecera para indicar que se envían datos en formato JSON
  http.addHeader("Content-Type", "application/json");
  // Configurar datos a enviar por POST utilizando los valores actuales del documento
  String postData;
  serializeJson(doc, postData);
  int httpResponseCode = http.POST(postData);
  if (httpResponseCode > 0) {
    String response = http.getString();
    deserializeJson(doc, response);
    Serial.println("Envío exitoso");
  } else {
    Serial.print("Error en el envío. Código de respuesta: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}

void loop() {
   // Generar números aleatorios para simular sensores
  int temperatura = random(15, 30); // Temperatura entre 15 y 30 grados Celsius
  int humedad = random(30, 70); // Humedad entre 30% y 70%
  int viento = random(5, 20); // Velocidad del viento entre 5 y 20 km/h

  // Asignar los valores aleatorios al documento JSON
  doc["id_sensor"] = "sensor-exterior";
  doc["temperatura"] = temperatura;
  doc["humedad"] = humedad;
  doc["viento"] = viento;

  send_data();
  delay(1000); // Esperar un segundo antes de la próxima iteración
}