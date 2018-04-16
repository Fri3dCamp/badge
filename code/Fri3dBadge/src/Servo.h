#ifndef __SERVO_H
#define __SERVO_H

#include "Arduino.h"

#include <ESP32Servo.h>

// een verpakking voor de technische ESP32Servo klasse

class Servo {
	public:
		Servo(int pin);
		void draai(int hoek);
		void draai(int hoek, int interval);
		void draai_naar(int hoek);
		void draai_naar(int hoek, int interval);
		int hoek();
	private:
		ESP32Servo* servo;
};

#endif
