#include "Servo.h"

Servo::Servo(int pin) {
	// this->servo = new ESP32Servo(pin);
}

void Servo::draai(int hoek) {
	// this->servo->write(this->servo->read()+hoek);
}

void Servo::draai(int hoek, int interval) {
	// this->servo->write(this->servo->read()+hoek, interval);
}

void Servo::draai_naar(int hoek) {
	// this->servo->write(hoek);
}

void Servo::draai_naar(int hoek, int interval) {
	// this->servo->write(hoek, interval);
}

int Servo::hoek() {
	// return this->servo->read();
}
