#include "shiftRegister.h"


void shiftReg_initPins(shiftReg_t* shiftReg) {
	pinMode(shiftReg->PIN_DATA, OUTPUT);
	pinMode(shiftReg->PIN_CLK, OUTPUT);
	pinMode(shiftReg->PIN_STROBE, OUTPUT);

	digitalWrite(shiftReg->PIN_DATA, LOW);
	digitalWrite(shiftReg->PIN_CLK, LOW);
	digitalWrite(shiftReg->PIN_STROBE, LOW);
	
	//If the output enable function is available, then we init the corresponding pins
	pinMode(shiftReg->PIN_OUTPUT_EN, OUTPUT);
	digitalWrite(shiftReg->PIN_OUTPUT_EN, (shiftReg->PIN_OUTPUT_EN_POL == SHIFTREG_PIN_LOW_POSITIVE) ? HIGH : LOW);
}

int shiftReg_sendData(shiftReg_t* shiftReg, uint8_t data, uint8_t bits) {
	if(shiftReg == NULL) {
		return -1;
	}
	if(bits > 8) {
		bits = 8;
	}

	for (uint8_t i = 0; i < bits; i++) {
		//Set pin to the corresponding data
		if((data & (1 << i)) != 0) {
			digitalWrite(shiftReg->PIN_DATA, HIGH);
		} else {
			digitalWrite(shiftReg->PIN_DATA, LOW);
		}
		//Record the data with a CLK pulse
		shiftReg_shiftIn(shiftReg);
	}
	digitalWrite(shiftReg->PIN_DATA, LOW);	//Reset the data pin
	return 0;
}

int shiftReg_latchData(shiftReg_t* shiftReg) {
	if(shiftReg == NULL) {
		return -1;
	}
	digitalWrite(shiftReg->PIN_STROBE, HIGH);
	digitalWrite(shiftReg->PIN_STROBE, LOW);
	return 0;
}

int shiftReg_outputSet(shiftReg_t* shiftReg, bool enable) {
	if(shiftReg == NULL) {
		return -1;
	}
	//If low positive logic, then enable requires LOW signal level
	if(shiftReg->PIN_OUTPUT_EN_POL == SHIFTREG_PIN_LOW_POSITIVE) {
		enable = !enable;
	}
	if(enable) {
		digitalWrite(shiftReg->PIN_OUTPUT_EN, HIGH);
	} else {
		digitalWrite(shiftReg->PIN_OUTPUT_EN, LOW);
	}
	return 0;
}