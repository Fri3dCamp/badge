#include <Fri3dBadge.h>

Fri3dBadge badge;

enum activities {
  AWAKE,
  BLACK,
  RED,
  GREEN,
  BLUE
};

uint8_t activity = AWAKE;

void cycle_activity() {
  if(! badge.button_is_pressed() ) { // button up event
    if(activity < BLUE) {
      activity++;
    } else {
      activity = AWAKE;
    }
  }
}

void setup() {
  badge.on_button_change(cycle_activity);
}

void loop() {
  switch(activity) {
    case AWAKE:
      badge.rgb_set_color(255, 255, 255);
      break;
    case BLACK:
      badge.rgb_set_color(  0,   0,   0);
      break;
    case RED:
      badge.rgb_set_color(255,   0,   0);
      break;
    case GREEN:
      badge.rgb_set_color(  0, 255,   0);
      break;
    case BLUE:
      badge.rgb_set_color(  0,   0, 255);
      break;
  }

  if(activity != AWAKE) { badge.sleep(); }
  else { delay(5); } // TODO is this really needed?
}
