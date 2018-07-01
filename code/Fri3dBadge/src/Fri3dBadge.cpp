#include "Fri3dBadge.h"

#include "config.h"

// IO controle pinnen voor de vier servo's, in volgorde van SERVO1,...
int pinnen[4] = { SERVO1_PIN, SERVO2_PIN, SERVO3_PIN, SERVO4_PIN };

Fri3dBadge::Fri3dBadge() 
{
	// creëer servo objecten voor de 4 servos
	// for(int i=0; i<4; i++) {
		// this->servos[i] = new Servo(pinnen[i]);
	// }
}

// Servo Fri3dBadge::servo(int index) {
	// return *(this->servos[index]);
// }
