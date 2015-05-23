
#define LED_PIN 13

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()) {
    int value = Serial.read();
    flash(value);
    //continu(value);
    }
    delay(1000);
}

void continu(int n) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(1000);
  }
  digitalWrite(LED_PIN, LOW);
}

void flash(int n) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(n*10);
    digitalWrite(LED_PIN, LOW);
    delay(n*10);
  }
}

