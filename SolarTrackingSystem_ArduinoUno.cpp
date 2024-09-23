#include <Servo.h>
#include <HCSR04.h>
#define LDR1 A0
#define LDR2 A1
#define VOLTAGE_SENSOR_PIN A2
#define ERROR 10

HCSR04 hc(12, 10); //initialisation class HCSR04 (trig pin , echo pin)

float resetDistance;


int Spoint = 90;
Servo servo;
int counter = 0 ;


void setup()
 {
  servo.attach(11);
  servo.write(Spoint);
  delay(1000);
  
  // Initialize hardware serial communication for TX/RX
  Serial.begin(9600);  // Use Serial for TX/RX communication with Raspberry Pi
}

void loop() {
  float  distance = hc.dist();

  int ldr1 = analogRead(LDR1);
  int ldr2 = analogRead(LDR2);

  int value1 = abs(ldr1 - ldr2);
  int value2 = abs(ldr2 - ldr1);

  if ((value1 <= ERROR) || (value2 <= ERROR)) {
    // Do nothing; the servo remains in place
  } else {
    if (ldr1 > ldr2) {
      Spoint = Spoint - 2; // Move the servo left
    }
    if (ldr1 < ldr2) {
      Spoint = Spoint + 2; // Move the servo right
    }
  }

  servo.write(Spoint);
  delay(80);

      if(distance<14)
    {
      resetDistance =((12.50) - (distance));

      Serial.print("Deep : ");
      Serial.print(resetDistance);
      delay(150);
      }

  int sensorValue = analogRead(VOLTAGE_SENSOR_PIN);
  float voltage = sensorValue * (5.0 / 1023.0);

  // Send data to Raspberry Pi via TX pin
  // Serial.print(" LDR1: ");
  // Serial.print(ldr1);
  // Serial.print(", LDR2: ");
  // Serial.print(ldr2);
  Serial.print(", Servo Position: ");
  Serial.print(Spoint);
  Serial.print(", Voltage: ");
  Serial.println(voltage);
  // Serial.print("Counter : ");
  // Serial.println(counter);
  // counter++;
  delay(5000); // Wait before the next loop iteration
}


