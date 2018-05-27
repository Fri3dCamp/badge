#include <pthread.h>

#include "Matrix.h"

#include "config.h"

const uint8_t MATRIX_LEFT_COLS[][7] = {
  { 8, 7, 4, 6, 9, 10, 11 }, // right
  { 0, 1, 2, 3, 4,  5,  6 }  // left
};

const uint8_t MATRIX_LEFT_ROWS[][5] = {
  { 0, 3,  1,  2, 5 },       // right (reversed)
  { 8, 9, 10, 11, 7 }        // left
};

// font, encoded as three bytes for three columns per char
// hint: rotate your editor/screen 90 degrees to the left to "see" chars
const uint8_t FONT[][3] = {
  // A
  {
    0b00011110,
    0b00000101,
    0b00011110
  },
  // B
  {
    0b00011111,
    0b00010101,
    0b00001010
  }
};

Matrix::Matrix() {
  //set pins to output so you can control the shift register
  pinMode(LED_LATCH_PIN,  OUTPUT);
  pinMode(LED_CLOCK_PIN,  OUTPUT);
  pinMode(LED_DATA_PIN,   OUTPUT);
  pinMode(LED_ENABLE_PIN, OUTPUT);

  digitalWrite(LED_ENABLE_PIN, LOW); // active low
}

void Matrix::start() {
  // low-level clearing of screen, resets old pin setting
  this->render(0,0);
  
  // start screen refresh thread
  xTaskCreatePinnedToCore(
    codeForTask2,            /* Task function. */
    "video_task",                 /* name of task. */
    1000,                    /* Stack size of task */
    this,                     /* parameter of the task */
    1,                        /* priority of the task */
    &video_task,               /* Task handle to keep track of created task */
    1);                       /* Core */
}

void codeForTask2( void * parameter )
{
  for (;;) {
    Serial.print("The second Task runs on Core: ");
    Serial.println(xPortGetCoreID());
    delay(2000);                       // wait for a second
  }
}

void Matrix::set(uint8_t x, uint8_t y) {
  this->matrix[x] |= 1UL << y;
}

void Matrix::clear(uint8_t x, uint8_t y) {
  this->matrix[x] &= ~(1UL << y);
}

void Matrix::clear() {
  // TODO improve with memcpy ???
  for(uint8_t y=0; y<5; y++) {
    for(uint8_t x=0; x<14; x++) {
      this->clear(x, y);
    }
  }
}

void Matrix::write(char c) {
  this->write(c, 0);
}

void Matrix::write(char c, uint8_t x) {
  this->matrix[x]   = FONT[c-'A'][0];
  this->matrix[x+1] = FONT[c-'A'][1];
  this->matrix[x+2] = FONT[c-'A'][2];
}

// private

#define BITSET(var,pos) ((var) & (1<<(pos)))

// function to perform screen refresh
void Matrix::render(void * parameter) {
  for(uint8_t y=0; y<5; y++) {
    for(uint8_t x=0; x<7; x++) {
      int right = BITSET(this->matrix[x],  y) ? pixel(x, y, RIGHT_EYE) : 0;
      int left  = BITSET(this->matrix[x+7],y) ? pixel(x, y, LEFT_EYE ) : 0;
      if( right || left ) {
        this->render( right, left );
        // delayMicroseconds(10); // TODO optimize value for light intensity
      }
    }
  }
}

void Matrix::render( int right, int left ) {
  digitalWrite(LED_LATCH_PIN, LOW);
  
  shiftOut(LED_DATA_PIN, LED_CLOCK_PIN, LSBFIRST, (left & 0x00ff));
  shiftOut(LED_DATA_PIN, LED_CLOCK_PIN, LSBFIRST, (right << 4 ) | (left >> 8));
  shiftOut(LED_DATA_PIN, LED_CLOCK_PIN, LSBFIRST, (right >> 4));
  
  digitalWrite(LED_LATCH_PIN, HIGH);
}

int Matrix::pixel(uint8_t x, uint8_t y, uint8_t eye) {
  // TODO do dynamically based on config of pins
  int e = 0b000001111111;            // all rows low, all cols high
  if(eye == RIGHT_EYE) {  e = 0b111111010000; }
  e &= ~(1UL << MATRIX_LEFT_COLS[eye][x]);  // clear column bit
  e |=   1UL << MATRIX_LEFT_ROWS[eye][y];   // set row bit
  return e;
}
