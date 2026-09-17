#include <WiFi.h>
#include <FirebaseESP32.h>

// Pinos
#define RELE_PIN 26

// Credenciais do Wi-Fi
// ATENÇÃO: Caracteres especiais como "ã" costumam dar erro no ESP32. 
// O ideal seria mudar o nome do seu celular para "IphoneJoao" (sem acento)
const char* WIFI_SSID = "Iphone de Jo\xc3\xa3o"; 
const char* WIFI_PASSWORD = "gremio01";

// Credenciais do Firebase
#define FIREBASE_HOST "https://next-fiap-default-rtdb.firebaseio.com"
#define FIREBASE_API_KEY "AIzaSyDkWmQvgU9Mf-vHMBkKr9ujKX_vw9rKQk4"

// Objetos do Firebase
FirebaseData fbdo;
FirebaseAuth firebaseAuth;
FirebaseConfig firebaseConfig;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n\n=== ESP32 - INICIO ===");

  // Configuração do Pino do Relé
  pinMode(RELE_PIN, OUTPUT);

  // === TESTE DO RELE ===
  Serial.println("[TESTE] Piscando rele 2x para testar fiacao...");
  digitalWrite(RELE_PIN, HIGH);
  delay(1000);
  digitalWrite(RELE_PIN, LOW);
  delay(1000);
  digitalWrite(RELE_PIN, HIGH);
  delay(1000);
  digitalWrite(RELE_PIN, LOW);
  delay(1000);
  
  // Relé inicia desligado (Voltei para a lógica normal como você pediu)
  digitalWrite(RELE_PIN, LOW);
  Serial.println("[TESTE] Fim do teste da lampada.");

  // Conectar ao Wi-Fi
  Serial.print("[WIFI] Conectando a: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
    tentativas++;
    if (tentativas > 30) {
      Serial.println("\n[WIFI] FALHOU! O ESP32 nao achou o Wi-Fi.");
      Serial.println("[DICA] Ligue o 'Maximizar Compatibilidade' no iPhone.");
      Serial.println("[DICA] Ou mude o nome do iPhone para tirar o 'a' com til.");
      delay(3000);
      ESP.restart();
    }
  }

  Serial.println();
  Serial.println("[WIFI] Conectado!");

  // Inicializar Firebase
  firebaseConfig.database_url = FIREBASE_HOST;
  firebaseConfig.api_key = FIREBASE_API_KEY;
  firebaseAuth.user.email = "";
  firebaseAuth.user.password = "";

  Firebase.begin(&firebaseConfig, &firebaseAuth);
  Firebase.reconnectWiFi(true);
  Serial.println("[FIREBASE] Iniciado. Aguardando comandos...");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    delay(5000);
    return;
  }

  if (Firebase.getBool(fbdo, "/estacao1/sessao_ativa")) {
    bool sessaoAtiva = fbdo.boolData();

    if (sessaoAtiva) {
      digitalWrite(RELE_PIN, HIGH); // Liga a luz
      Firebase.setBool(fbdo, "/estacao1/esp_status_ligado", true);
    } else {
      digitalWrite(RELE_PIN, LOW);  // Desliga a luz
      Firebase.setBool(fbdo, "/estacao1/esp_status_ligado", false);
    }
  }

  delay(1000);
}
