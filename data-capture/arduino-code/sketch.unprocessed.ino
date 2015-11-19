// Uses the AES encryption/decryption Arduino library found at:
// http://utter.chaos.org.uk/~markt/AES-library.zip
#include <AES.h>
#include <stdio.h>

int size_key = 128;
byte key[] = 
{
  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F
};

AES aes;
// const uint8_t N_PLAINTEXTS; NUMBER OF PLAINTEXTS INSERT HERE [see process_input.py @1]
// const byte plaintext [N_PLAINTEXTS][N_BLOCK]; PLAINTEXT INSERTS HERE [see process_input.py @2]

byte cipher [N_BLOCK];
char print_buffer [100];

void loop() {}

void setup () {
  pinMode(13, OUTPUT);
  digitalWrite(13,LOW);

  Serial.begin(57600);
  for(int i = 0; i < N_PLAINTEXTS; i++) {
    run_aes_ecb(i);
  }
}

void run_aes_ecb(int plain_index) {
  //Signal start of encryption
  byte succ = aes.set_key (key, 129);
  sprintf(print_buffer, "Encrypting plaintext index: %d out of %d \0", plain_index, N_PLAINTEXTS);
  Serial.println(print_buffer);
  digitalWrite(13,HIGH);

  succ = aes.encrypt (plaintext[plain_index], cipher);
  Serial.println("Finished encryption");

  // succ = aes.decrypt (cipher, plain) ;
}
