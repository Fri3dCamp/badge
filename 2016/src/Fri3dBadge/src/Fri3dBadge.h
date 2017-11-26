#ifndef __FRI3D_BADGE_H
#define __FRI3D_BADGE_H

#include "Arduino.h"

typedef void(*badge_event_handler_t)(void);

class Fri3dBadge {
  public:
    Fri3dBadge();

    void on_button_change(badge_event_handler_t handler);

    void sleep();
    void sleep_for(uint8_t sec);

    void rgb_set_color(uint8_t red, uint8_t green, uint8_t blue);

    bool button_is_pressed();
    
    void on_ir_activity(badge_event_handler_t handler);
    void ir_rx_start();
    void ir_rx_stop();
    void ir_send_pulse(uint32_t micros);
  private:
    badge_event_handler_t ir_rx_handler = NULL;
};

#endif
