#define LED 2

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  
}

void loop() {
  Serial.println("LED aan");
  digitalWrite(LED, HIGH);
  delay(1000);
  Serial.println("LED uit");
  digitalWrite(LED, LOW);
  delay(1000);
}

