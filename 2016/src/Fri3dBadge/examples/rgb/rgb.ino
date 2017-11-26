#include <Fri3dBadge.h>

Fri3dBadge badge;

void setup() {}

#define RED   0
#define GREEN 1
#define BLUE  2

void fade(uint8_t color) {
  for(int8_t value=0; value<30; value++) {
    switch(color) {
      case RED:   badge.rgb_set_color(value,     0,     0); break;
      case GREEN: badge.rgb_set_color(    0, value,     0); break;
      case BLUE:  badge.rgb_set_color(    0,     0, 2*value); break;
    }
    delay(50);
  }

  delay(200);

  for(int8_t value=30; value>=0; value--) {
    switch(color) {
      case RED:   badge.rgb_set_color(value,     0,     0); break;
      case GREEN: badge.rgb_set_color(    0, value,     0); break;
      case BLUE:  badge.rgb_set_color(    0,     0, 2*value); break;
    }
    delay(50);
  }

  delay(1000);
}

void loop() {
  fade(RED);
  fade(GREEN);
  fade(BLUE);
}
