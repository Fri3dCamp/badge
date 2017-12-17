#include "Fri3dBadge.h"

// IO controle pinnen voor de vier servo's (hardware configuratie)
int pinnen[4] = { 5, 16, 17, 18 };

Fri3dBadge::Fri3dBadge() {
	// creëer servo objecten voor de 4 servos
	for(int i=0; i<4; i++) {
		this->servos[i] = new Servo(pinnen[i]);
	}
}

Servo Fri3dBadge::servo(int index) {
	return *(this->servos[index]);
}
