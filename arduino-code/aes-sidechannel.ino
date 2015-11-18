// Uses the AESLib encryption library for Arduino
// https://github.com/DavyLandman/AESLib

#include <AESLib.h>

char data[17];    // Allocate some space for the data string
char inChar = -1; // Where to store the character read
byte index = 0;   // Index into array; where to store the character
uint8_t key[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}; //16 bytes of Key

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  digitalWrite(13,LOW);
  data[16]='\0';
}

void loop() {
  while (Serial.available() > 0) // Don't read unless you know there is data
  {
    if(index < 16) {
      inChar = Serial.read(); // Read a character
      data[index] = inChar;   // Store it
      index++;                // Increment where to write next
    } else {
      Serial.println(data);
      Serial.println("START");
      digitalWrite(13,HIGH);
      aes128_enc_single(key, data);
      digitalWrite(13,LOW);
      Serial.println("DONE");
      Serial.println(data);
      aes128_dec_single(key,data);
      Serial.println(data);
      index = 0;       
    }
  }
}
