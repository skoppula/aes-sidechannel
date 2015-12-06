// Uses the AESLib encryption library for Arduino
// https://github.com/DavyLandman/AESLib

#include <AESLib.h>

unsigned char data[17];    // Allocate some space for the data string
char inChar = -1; // Where to store the character read
byte index = 0;   // Index into array; where to store the character
uint8_t key[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}; //16 bytes of Key
char temp[4];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  //digitalWrite(13,HIGH);
  //delay(3000);
  digitalWrite(13,LOW);
  data[16]='\0';
  Serial.println("Running AES");
}

void print_data(unsigned char data[])
{
   for(int i=0; i<16; i++)
   {
      sprintf(temp, "%02X ", data[i]);
      Serial.print(temp);
   }
   Serial.println();
}

void loop() {
  while(Serial.available() > 0) // Don't read unless you know there is data
  {
    if(index < 16) {
      inChar = Serial.read(); // Read a character
      // Serial.println(inChar);
      data[index] = inChar;   // Store it
      index++;                // Increment where to write next
    } 
    if(index == 16) {
      //print_data(data);
      for(int i=0; i<100; i++) {
        delay(2000);
        cli();
        //digitalWrite(13,HIGH);
        //Serial.print(i);
        //Serial.print(": ");
        //print_data(data);
        aes128_enc_single(key, data);
        //digitalWrite(13,LOW);
        //Serial.print(i);
        //Serial.print(":");
        //print_data(data);
        //aes128_dec_single(key,data);
        //print_data(data);
        index = 0;
        sei();
      }
    }
  }
}

