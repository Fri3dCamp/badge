#ifndef __FRI3D_BADGE_H
#define __FRI3D_BADGE_H

#include "Arduino.h"

#include "AButton.h"
#include "Servo.h"
#include "Matrix.h"

// interne indexering van de 4 servo's
enum { SERVO1, SERVO2, SERVO3, SERVO4 };

class Fri3dBadge {
  public:
    Fri3dBadge();
		// toegang tot vier servo's via de indexen zoals in de enum beschreven
		Servo servo(int index);
    
    // toegang tot screen matrix 5x14 via sub-object
    Matrix matrix;

    // toegang to buttons
    AButton button_a;
    AButton button_b;
    AButton button_d;

	private:
		Servo* servos[4];
};

#endif
