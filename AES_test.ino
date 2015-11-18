// Uses the AESLib encryption library for Arduino
// https://github.com/DavyLandman/AESLib

#include <AESLib.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  digitalWrite(13,LOW);
  delay(1000);
  digitalWrite(13,HIGH);
  uint8_t key[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
  char data[] = "ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890"; //128 byte
  for(size_t ix = 0; ix < 128; ix += 16)
  {
    digitalWrite(13,LOW);
    delay(.5 );
    digitalWrite(13,HIGH);
    aes128_enc_single(key, data+ix);
  }
  digitalWrite(13,LOW);
  Serial.println(data);
}

void loop() {

}
