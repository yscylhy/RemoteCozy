const int CTRL_PIN = 2;
String inputString = "";
bool stringComplete = false;

void setup(){
  Serial.begin(9600);
  pinMode(CTRL_PIN, OUTPUT);
  digitalWrite(CTRL_PIN, LOW);
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
    else{
      digitalWrite(CTRL_PIN, LOW);
    }

    inputString = "";
    stringComplete = false;    
  }
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
