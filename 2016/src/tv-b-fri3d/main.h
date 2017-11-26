#include <avr/pgmspace.h>


/*
2-September-2015
Updated definition for 
     struct IrCode {
so that the sketch will compile with Arduino 1.6.5 software.
Also: add conditional define for changing DELAY_CNT, 
      since the new Arduino software compiles to make the delay_ten_us() function execute too quickly.

*/


// The TV-B-Gone for Arduino can use
//   either the EU or the NA database of POWER CODES
// EU is for Europe, Middle East, Australia, New Zealand, and some countries in Africa and South America
// NA is for North America, Asia, and the rest of the world not covered by EU

// Two regions!
#define NA 1
#define EU 0

// What pins do what
#define DBG 12
#define LED 13
#define IRLED 3
#define TRIGGER 2
#define REGIONSWITCH 5  // add a 1K pull-down resistor from Pin 5 to ground for EU (blank for NA)

// Lets us calculate the size of the NA/EU databases
#define NUM_ELEM(x) (sizeof (x) / sizeof (*(x)));

// set define to 0 to turn off debug output
#define DEBUG 0
#define DEBUGP(x) if (DEBUG == 1) { x ; }

// Shortcut to insert single, non-optimized-out nop
#define NOP __asm__ __volatile__ ("nop")

// Arduino software that is newer than V1.0 needs a different value for DELAY_CNT
// set ARD_VER_10X to 1 for Arduino software V1.0.x
// set ARD_VER to 0 for newer versions of Arduino software (such as V1.6.5)
#define ARD_VER_10X 0

// DELAY_CNT is used for delay_ten_us() for timing ontime and offtime values
// Tweak this if neccessary to change timing for accuracy (which must be done empirically)
#if ARD_VER_10X
# define DELAY_CNT 25
#else
# define DELAY_CNT 30
#endif

// Makes the codes more readable. the OCRA is actually
// programmed in terms of 'periods' not 'freqs' - that
// is, the inverse!
#define freq_to_timerval(x) (F_CPU / 8 / x - 1)

// The structure of compressed code entries
struct IrCode {
  const uint8_t timer_val;
  const uint8_t numpairs;
  const uint8_t bitcompression;
  const uint16_t * const times;
  const uint8_t * const codes;
};
