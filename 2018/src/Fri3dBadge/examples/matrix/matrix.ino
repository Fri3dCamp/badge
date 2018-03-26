#include "Fri3dBadge.h"

Fri3dBadge badge;

void setup() {
  badge.matrix.start(); // if done before (e.g. in badge construction)
                        // blocks setup from starting ?! 

  badge.button_a.on_click(&on_click_a);
  badge.button_b.on_click(&on_click_b);

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

bool show_a     = false;
bool show_b     = false;
bool text_dirty = false;

void on_click_a() {
  show_a = !show_a;
  text_dirty = true;
}

void on_click_b() {
  show_b = !show_b;  
  text_dirty = true;
}

unsigned long last_pixel = 0;

void loop() {
  if( text_dirty ) {
    write();
  }
  unsigned long now = millis();
  if( ! show_a && ! show_b && now - last_pixel > 500 ) {
    render_random_pixel();
    last_pixel = now;
  }
  delay(1); // needed to give threads chance to run ;-)
}

void render_random_pixel() {
  static int x = 0, y = 0;
  badge.matrix.clear(x, y);
  x = random(14);
  y = random(5);
  badge.matrix.set(x, y);
}

void write() {
  badge.matrix.clear();
  if( show_a ) {
    badge.matrix.write('A');
  }
  if( show_b ) {
    badge.matrix.write('B', 8);
  }
  text_dirty = false;
}
