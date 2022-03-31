#ifndef _SHIFTREGISTER_HEADER_
#define _SHIFTREGISTER_HEADER_

#include <Arduino.h>

enum shiftReg_pinLogicPolarity {
	SHIFTREG_PIN_HIGH_POSITIVE,
	SHIFTREG_PIN_LOW_POSITIVE
};

typedef
struct shiftReg_t {
	const uint8_t PIN_DATA;
	const uint8_t PIN_CLK;

	const uint8_t PIN_STROBE;

	const enum shiftReg_pinLogicPolarity PIN_OUTPUT_EN_POL;
	const uint8_t PIN_OUTPUT_EN;
} shiftReg_t;


inline void shiftReg_shiftIn(shiftReg_t* shiftReg) {
	digitalWrite(shiftReg->PIN_CLK, HIGH);
	digitalWrite(shiftReg->PIN_CLK, LOW);
}

//Initializes the given pins
void shiftReg_initPins(shiftReg_t* shiftReg);

//Sends "bits" amount of data to the shift register
//If "bits" is larger than 8, then it sends 8 bits.
//If more data transfer is required, the function may called multiple times.
//Returns -1 when a nullpointer is given
int shiftReg_sendData(struct shiftReg_t* shiftReg, uint8_t data, uint8_t bits);

int shiftReg_latchData(shiftReg_t* shiftReg);

int shiftReg_outputSet(shiftReg_t* shiftReg, bool enable);

#endif