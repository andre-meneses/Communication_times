#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "yourSSID"; // Substitua pelo SSID da sua rede
const char* password = "yourPassword"; // Substitua pela senha da sua rede

const int localUdpPort = 12345; // A porta em que o servidor irá escutar

WiFiUDP udp;

void setup() {
    Serial.begin(115200);

    // Conectar ao WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("WiFi conectado");
    Serial.println("Endereço IP: ");
    Serial.println(WiFi.localIP());

    udp.begin(localUdpPort);
    Serial.printf("Agora escutando na porta UDP %d\n", localUdpPort);
}

void loop() {
    int packetSize = udp.parsePacket();
    if (packetSize) {
        // buffer para receber dados
        char packetBuffer[1024];
        int len = udp.read(packetBuffer, 1024);
        if (len > 0) {
            packetBuffer[len] = 0; // Null-terminate a string
        }

        // Processamento de pacotes (por exemplo, echo back)
        Serial.printf("Pacote recebido. Tamanho: %d\n", len);
        Serial.printf("Conteúdo: %s\n", packetBuffer);

        // Echo o pacote de volta para o remetente
        udp.beginPacket(udp.remoteIP(), udp.remotePort());
        udp.write(packetBuffer, len);
        udp.endPacket();
    }
}

