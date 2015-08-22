
#define LED_PIN 13
#define LED_A 3
#define LED_B 4
#define LED_C 5

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_PIN, OUTPUT);
  pinMode(LED_A, OUTPUT);
  pinMode(LED_B, OUTPUT);
  pinMode(LED_C, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()) {
    //int value = Serial.read();
    //int value_a = Serial.read();
    //int value_b = Serial.read();
    int value_c = Serial.read();
    //flashA(value_a);
    //flashB(value_b);
    flashC(value_c);
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

void flashA(int n) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED_A, HIGH);
    delay(n*5);
    digitalWrite(LED_A, LOW);
    delay(n*5);
  }
}

void flashB(int n) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED_B, HIGH);
    delay(n);
    digitalWrite(LED_B, LOW);
    delay(n);
  }
}

void flashC(int n) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED_C, HIGH);
    delay(n);
    digitalWrite(LED_C, LOW);
    delay(n);
  }
}
