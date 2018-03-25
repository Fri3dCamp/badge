#include "Fri3dBadge.h"

Fri3dBadge badge;

void setup() {
  badge.matrix.start(); // if done before (e.g. in badge construction)
                        // blocks setup from starting ?! 
  render_swipe();
}

void render_swipe() {
  for(int x=0; x<14; x++) {
    for(int y=0; y<5; y++) {
      badge.matrix.set(x, y);
    }
    delay(50);
  }
  delay(150);
  for(int x=0; x<14; x++) {
    for(int y=0; y<5; y++) {
      badge.matrix.clear(x, y);
    }
    delay(50);
  }
}

void loop() {
  // render_random_pixel();
  badge.matrix.clear();
  badge.matrix.write('A');
  delay(2000);
  badge.matrix.clear();
  badge.matrix.write('B', 8);
  delay(2000);
}

void render_random_pixel() {
  static int x = 0, y = 0;
  badge.matrix.clear(x, y);
  x = random(14);
  y = random(5);
  badge.matrix.set(x, y);
}
