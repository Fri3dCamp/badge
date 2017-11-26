#include <Fri3dBadge.h>

// create an instance of the badge
Fri3dBadge badge;

void setup() {
  // prepare randomness with some random reading from an unconnected analog pin
  randomSeed(analogRead(0));
	
  // select our own random color at boot ...
	select_color();
	
  // ... and allow to reselect using the button
  badge.on_button_change(reselect_color);
  
  // start the IR receiver
  badge.on_ir_activity(handle_activity);
  badge.ir_rx_start();
}

uint8_t r = 0, g = 0, b = 0;

void select_color() {
  r = g = b = 0;
  while( (r == 0) && (g == 0) && (b == 0)) {
    r = random(2) * 25;
    g = random(2) * 25;
    b = random(2) * 25;
  }
}

bool select_new_color = false;

void reselect_color() {
  if( ! badge.button_is_pressed() ) {
    select_new_color = true;
  }
}

bool activity_detected = false;

// don't respond to the very first interrupt, but make sure the received pulse
// was part of a pulse train
#define SKIP_ACTIVITY 2
int8_t skip_activity;

// don't respond to our own IR signals ;-)
volatile bool sending = false;

void handle_activity() {
  if(sending) { return; }
  if(skip_activity-- > 0) { return; }
  // set a flag to handle the activity (don't do too much in interrupt handler)
  activity_detected = true;
}

void flash_color() {
  badge.rgb_set_color(r, g, b);
  delay(500);
	badge.rgb_set_color(0, 0, 0);
}

void fade_color() {
  for(uint8_t i=0; i<25; i++) {
    badge.rgb_set_color(r/25*i, g/25*i, b/25*i);
    delay(10);
  }
  delay(500);
  for(int8_t i=25; i>0; i--) {
    badge.rgb_set_color(r/25*i, g/25*i, b/25*i);
    delay(10);
  }
  badge.rgb_set_color(0, 0, 0);
}

void wheel( byte pos ) {
  if(pos < 85) {
   badge.rgb_set_color( pos, 85 - pos, 0 );
  } else if( pos < 170) {
   pos -= 85;
   badge.rgb_set_color( 85 - pos, 0, pos );
  } else {
   pos -= 170;
   badge.rgb_set_color( 0, pos, 85 - pos );
  }
}

void reply_with_party_parrot() {
  for(uint8_t i = 0; i < 255; i++) {
    wheel(i);
    delay(4);
  }
  badge.rgb_set_color(0, 0, 0);
}

// timestamp of next dialog (= send pulse train)
uint32_t next_dialog = 0;

// we take a minimal interval of 5s and add a random part of the same length
#define INTERVAL    5000 + (random(6) * 1000) // start dialog every 5s + [0-5]s

// a pulse train of x pulses of pulse length y
#define PULSES        10
#define PULSE_LENGTH 500   // us

void loop() {
  uint32_t now = millis(); // rollover of ~49.7 days ... not gonna happen ;-)

  // start a dialog at INTERVAL
  if( now >= next_dialog ) {
    fade_color();
    
    // send an IR pulse train
    sending = true;
    for(uint8_t t=0; t<PULSES; t++) {
      badge.ir_send_pulse(PULSE_LENGTH);
      delayMicroseconds(PULSE_LENGTH);
    }
    sending = false;

    // schedule the next dialog after interval
    next_dialog = now + INTERVAL;
  }

  // respond to activity
  if(activity_detected) {
    delay(250);
    activity_detected = false;
    reply_with_party_parrot();
    skip_activity = SKIP_ACTIVITY;
    next_dialog = now + INTERVAL;
  }

  // handle new color selection request
  if(select_new_color) {
    select_color();
    flash_color();
    select_new_color = false;
    next_dialog = now + INTERVAL;
  }

  delay(5);
}
