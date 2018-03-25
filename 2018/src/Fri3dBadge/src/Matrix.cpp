#include <pthread.h>

#include "Matrix.h"

#include "config.h"

const int MATRIX_LEFT_COLS[][7] = {
  { 8, 7, 4, 6, 9, 10, 11 }, // right
  { 0, 1, 2, 3, 4,  5,  6 }  // left
};

const int MATRIX_LEFT_ROWS[][5] = {
  { 0, 3,  1,  2, 5 },       // right (reversed)
  { 8, 9, 10, 11, 7 }        // left
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
  pthread_t video_thread;
  pthread_create(&video_thread, NULL, &Matrix::refresh_screen, this);
}

void Matrix::set(int x, int y) {
  this->matrix[x] |= 1UL << y;
}

void Matrix::clear(int x, int y) {
  this->matrix[x] &= ~(1UL << y);
}

void Matrix::clear() {
  // TODO improve with memcpy ???
  for(int y=0; y<5; y++) {
    for(int x=0; x<14; x++) {
      this->clear(x, y);
    }
  }
}

// private

#define BITSET(var,pos) ((var) & (1<<(pos)))

// function to perform screen refresh
void Matrix::render() {
  for(int y=0; y<5; y++) {
    for(int x=0; x<7; x++) {
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

int Matrix::pixel(int x, int y, int eye) {
  // TODO do dynamically based on config of pins
  int e = 0b000001111111;            // all rows low, all cols high
  if(eye == RIGHT_EYE) {  e = 0b111111010000; }
  e &= ~(1UL << MATRIX_LEFT_COLS[eye][x]);  // clear column bit
  e |=   1UL << MATRIX_LEFT_ROWS[eye][y];   // set row bit
  return e;
}
