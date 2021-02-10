#include "DHT.h"

const int DHTPIN = 7;
const int CTRL_PIN = 2;
const int BUZZER_PIN = 3;
const int DHTTYPE = DHT11;

String inputString = "";
bool stringComplete = false;
float h = 0;
float t = 0;

DHT dht(DHTPIN, DHTTYPE);


void setup(){
  Serial.begin(9600);
  pinMode(CTRL_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT); 
  digitalWrite(CTRL_PIN, LOW);
  dht.begin();
  Serial.println("Initialization Done.");
}


void loop(){
   if (stringComplete) {
    Serial.println(inputString);
    if (inputString == String("0\n")){
      digitalWrite(CTRL_PIN, LOW);
    }
    else if ((inputString == String("1\n"))){
      digitalWrite(CTRL_PIN, HIGH);
    }
    else if((inputString==String("2\n"))){
      bee();
    }
    else if((inputString==String("3\n"))){
      bee_bee();
    }
    else if((inputString==String("4\n"))){
      read_dht11();
    }
    else{
      digitalWrite(CTRL_PIN, LOW);
    }

    inputString = "";
    stringComplete = false;    
  }
}


void bee(){
   tone(BUZZER_PIN, 2000); 
   delay(500);                  
   noTone(BUZZER_PIN);   
}


void bee_bee() {
   tone(BUZZER_PIN, 2000); 
   delay(250);                 
   noTone(BUZZER_PIN); 
   delay(50);
   tone(BUZZER_PIN, 2000); 
   delay(250);             
   noTone(BUZZER_PIN);   
}


void read_dht11() {
  h = dht.readHumidity();
  t = dht.readTemperature();  
  if (isnan(h) || isnan(t)) {
     h = 0;
     t = 0;
  }

  Serial.print('#');
  Serial.print(h);
  Serial.print('#');
  Serial.print(t);
}


/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
