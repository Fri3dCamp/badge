#include <Fri3dBadge.h>

Fri3dBadge badge;

bool active = true;

void refresh_state() {
  badge.rgb_set_color(active ? 255 : 0, 0, 0);
}

void toggle_color() {
  if(! badge.button_is_pressed() ) {
    active = !active; // toggle state on button up event
    refresh_state();
  }
}

void setup() {
  badge.on_button_change(toggle_color);
  refresh_state();
}

void loop() {}
