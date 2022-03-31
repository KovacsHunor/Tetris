#include <Arduino.h>

//Custom files
#include "shiftRegister.h"
#include "driver.h"

uint8_t data[21];

void setup() {
    driver_init();
    Serial.begin(19200);
    Serial.setTimeout(3);
}
int b = 0;
void loop() {
    while(!Serial.available());
    Serial.readBytes(data, 21);
    driver_setBuffer(data, DRV_DATABUFF_SIZE); 
    driver_writeScreen();
}