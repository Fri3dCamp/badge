#include <Arduino.h>

#ifndef LED_BUILTIN
// Set LED_BUILTIN if it is not defined by Arduino framework
#define LED_BUILTIN 13
#endif

void setup()
{
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
    Serial.println("LED aan");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    Serial.println("LED uit");
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
}
