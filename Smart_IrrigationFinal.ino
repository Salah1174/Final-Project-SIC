#include <Wire.h>
#include <LiquidCrystal_I2C.h>
// #define BLYNK_TEMPLATE_ID "TMPL2vycIh6V3"
// #define BLYNK_TEMPLATE_NAME "Smart Irrigation System"
// #include <BlynkSimpleEsp32.h>
#include <DHT.h>
#define TH A2 //Pin for dht11
int in1 = 9; //Declaring the pins where in1 in2 from the driver are wired 
int in2 = 10;
#define buzzer 8


#define sensor A3  // for gas detection
#define LDRPIN A1   //for LDR
#define soilMoisturePin A0

#define LED_1 2 // Pin connected to LED 1
#define LED_PIN_2 3 // Pin connected to LED 2
#define LED_PIN_3 4 // Pin connected to LED 3
#define LED_PIN_4 5 // Pin connected to LED 4

DHT dht(TH, DHT11);
// BlynkTimer timer;

char auth[] = "Mq8ClIPGLlTTzWXzezCOVRrv5CfQKSXe";

//SSID and password
char ssid[] = "";
char pass[] = "";

// const int soilMoisturePin = A0; 
LiquidCrystal_I2C lcd(0x27, 16, 2);

static int counter =  0 ;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  //Blynk.begin(auth, ssid, pass);
  dht.begin();
  lcd.init();
  lcd.begin(2,16);
  lcd.backlight();
  lcd.clear();
  pinMode(6, OUTPUT);     // for relay
  pinMode(LED_1, OUTPUT);
  pinMode(LED_PIN_2, OUTPUT);
  pinMode(LED_PIN_3, OUTPUT);
  pinMode(LED_PIN_4, OUTPUT);
  digitalWrite(6, HIGH); // relay
  pinMode(in1, OUTPUT); //Declaring the pin modes of motor
  pinMode(in2, OUTPUT);
  pinMode(buzzer, OUTPUT);
  delay(1000);
  lcd.setCursor(0, 0);
  lcd.print("Hello");
  delay(3000);

  lcd.setCursor(0, 1);
  lcd.print("System is on ");

  delay(3000);
  lcd.clear();
}

void loop() {
  if (counter >= 5 )
  {
    counter = 0 ;
    delay(5000);
  }
  counter++;
  int sensorValue = analogRead(soilMoisturePin);
  
  
  // Convert the value to a percentage (assuming 0-4095 range for ESP32 ADC)
  float moisturePercentage = 100 - ((sensorValue / 1023.0) * 100.0);
  int ldr_value = analogRead(LDRPIN);
  //Serial.print("Light Intensity Value : ");
  //Serial.println(ldr_value);
  
  //   // LDR conditions
  if (ldr_value < 200) { //very light
    // Turn off all LEDs
    digitalWrite(LED_1, LOW);
    digitalWrite(LED_PIN_2, LOW);
    digitalWrite(LED_PIN_3, LOW);
    digitalWrite(LED_PIN_4, LOW);
    
  } else if (ldr_value >=200 && ldr_value <=400) {
    // Serial.println("Almost Light");
    // Light up 1 LED
    digitalWrite(LED_1, HIGH);
    digitalWrite(LED_PIN_2, LOW);
    digitalWrite(LED_PIN_3, LOW);
    digitalWrite(LED_PIN_4, LOW);
  } else if (ldr_value >=500 && ldr_value <=700) {
    // Serial.println("Semilight");
    // Light up 2 LEDs
    digitalWrite(LED_1, HIGH);
    digitalWrite(LED_PIN_2, HIGH);
    digitalWrite(LED_PIN_3, LOW);
    digitalWrite(LED_PIN_4, LOW);

  } else if (ldr_value > 700 && ldr_value <=900) {
    // Serial.println("Semidark");
    // Light up 3 LEDs
    digitalWrite(LED_1, HIGH);
    digitalWrite(LED_PIN_2, HIGH);
    digitalWrite(LED_PIN_3, HIGH);
    digitalWrite(LED_PIN_4, LOW);

  } else if (ldr_value > 900) {
    // Serial.println("Dark");
    // Light up 4 LEDs
    digitalWrite(LED_1, HIGH);
    digitalWrite(LED_PIN_2, HIGH);
    digitalWrite(LED_PIN_3, HIGH);
    digitalWrite(LED_PIN_4, HIGH);

  }
// delay(3000);



  //Blynk.virtualWrite(V0,moisturePercentage);
  //Blynk.virtualWrite(V1, t)

  // Print the moisture percentage to the serial monitor
  //Serial.print("Soil Moisture: ");
  //Serial.println(moisturePercentage );
  // Serial.println("%");
  // digitalWrite(LED_1, HIGH);
  // digitalWrite(LED_PIN_2, HIGH);
  // digitalWrite(LED_PIN_3, HIGH);
  // digitalWrite(LED_PIN_4, HIGH);

  float h = dht.readHumidity();
  float t = dht.readTemperature();

    // Temperature conditions
  if (t > 32) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
}
  
  else {
    // Normal temperature
    // Serial.println("Normal Temprature");
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }

  int rawValue = analogRead(sensor); // Get the raw value
  //Serial.print("Gas Level: ");
  //Serial.println(rawValue); // Print the raw value directly without mapping
  if (rawValue > 205 ){
    digitalWrite(buzzer, HIGH);
  } 
  else{
    digitalWrite(buzzer, LOW);
  }  


 
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print("Moisture: ");
  Serial.print(moisturePercentage);
  Serial.print("% | Light Intensity: ");
  Serial.print(ldr_value);
  Serial.print(" | Temperature: ");
  Serial.print(t);
  Serial.print("°C | Humidity: ");
  Serial.print(h);
  Serial.print("% | Gas Level: ");
  Serial.println(rawValue); 


  if (moisturePercentage  < 50) { // need water
    digitalWrite(6, HIGH); //  Relay -> ON and ->TURN ON PUMP
    lcd.setCursor(0, 0);
    lcd.print("PUMP IS ON ");
  } else {
    digitalWrite(6, LOW); // TURN OFF PUMP
    lcd.setCursor(0, 0);
    lcd.print("PUMP IS OFF");
  }
  
  // Display moisture level on LCD
  if (moisturePercentage  > 70) {
    lcd.setCursor(0, 1);
    lcd.print("Moisture: HIGH  ");
  } else if (sensorValue  >= 50 && sensorValue  <= 70) {
    lcd.setCursor(0, 1);
    lcd.print("Moisture: MID  ");
  } else if (sensorValue  < 50) {
    lcd.setCursor(0, 1);
    lcd.print("Moisture: LOW ");
  }

 // Blynk.run();
  // Wait for a second before taking another reading
  //Serial.println(counter);
 // counter++;
delay(4000);
}
