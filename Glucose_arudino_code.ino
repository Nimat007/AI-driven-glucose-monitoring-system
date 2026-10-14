#include <SoftwareSerial.h>

SoftwareSerial BT(10, 11); // RX, TX

const int LED_PINS[] = {3, 4, 5, 6, 7, 8};
const int SENSOR_PINS[] = {A0, A1, A2, A3, A4, A5};

const int NUM_LEDS = 6;

String command = "";

void setup() {

  Serial.begin(9600);
  BT.begin(9600);

  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW);
  }

  Serial.println("READY");
}

void loop() {

  // -----------------------------
  // Receive command from Python
  // -----------------------------
  while (Serial.available()) {

    char c = Serial.read();

    if (c == '\n') {

      command.trim();

      // Sensor measurement commands
      if (command == "I0" || command == "I") {

        performSweep();
      }

      // Absorbance forwarding command
      else if (command.startsWith("ABS:")) {

        String absData = command.substring(4);

        BT.println(absData);

        Serial.println("Absorbance sent to HC-05");
      }

      command = "";

    } else {

      command += c;
    }
  }
}

// ------------------------------------
// Perform LED sweep and sensor reading
// ------------------------------------
void performSweep() {

  for (int i = 0; i < NUM_LEDS; i++) {

    digitalWrite(LED_PINS[i], HIGH);

    delay(300);

    long sum = 0;

    for (int j = 0; j < 20; j++) {

      sum += analogRead(SENSOR_PINS[i]);
      delay(5);
    }

    int sensorValue = sum / 20;

    Serial.print(i + 1);
    Serial.print(",");
    Serial.println(sensorValue);

    digitalWrite(LED_PINS[i], LOW);

    delay(200);
  }

  Serial.println("END");
}