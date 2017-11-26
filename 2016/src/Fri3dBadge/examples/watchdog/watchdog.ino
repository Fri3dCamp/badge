#include <Fri3dBadge.h>
#include <avr/wdt.h>

Fri3dBadge badge;

bool on       = true;
bool sleeping = false;

void toggle_sleeping() {
  if( ! badge.button_is_pressed() ) { sleeping = !sleeping; }
}

void setup() {
  badge.on_button_change(toggle_sleeping);
}

void loop() {
  on = !on;
  if(sleeping) {
    // sleeping = blue
    on ? badge.rgb_set_color(0, 0, 255) : badge.rgb_set_color(0, 0, 0);
    badge.sleep_for(3);
  } else {
    // not sleeping = red
    on ? badge.rgb_set_color(255, 0, 0) : badge.rgb_set_color(0, 0, 0);
    delay(500);
  }
}

