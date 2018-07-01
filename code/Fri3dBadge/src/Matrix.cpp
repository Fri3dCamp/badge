#include <pthread.h>

#include "Matrix.h"

#include "config.h"

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
  // this->render(0,0);
  
  // start screen refresh thread
  xTaskCreatePinnedToCore(this->startTaskImpl, "video_task", 1000, this, 5, &video_task, 1);
}

void Matrix::set(uint8_t eye, uint8_t x, uint8_t y) {
  // this->matrix[x] |= 1UL << y;
}

void Matrix::clear(uint8_t eye) {
  // this->matrix[x] &= ~(1UL << y);
}

// private

#define BITSET(var,pos) ((var) & (1<<(pos)))

void Matrix::startTaskImpl(void* _this){
    ((Matrix*)_this)->renderTask();
}

void Matrix::renderTask() {
  uint8_t row = 0;

  for (;;) {
    row %= 5;
    this->render(this->buffer, row);
    row++;
  }
}

// function to perform screen refresh
void Matrix::render(uint8_t* buffer, uint8_t row) {
    digitalWrite(LED_LATCH_PIN, LOW);  

    uint d = buffer[row + 5];
    d = (d << 5) | (1 << row);
    d = (d << 7) | buffer[row];
    d = (d << 5) | (1 << row);

    shiftOut(LED_DATA_PIN, LED_CLOCK_PIN, LSBFIRST, d);
    shiftOut(LED_DATA_PIN, LED_CLOCK_PIN, LSBFIRST, (d >> 8));
    shiftOut(LED_DATA_PIN, LED_CLOCK_PIN, LSBFIRST, (d >> 16));

    digitalWrite(LED_LATCH_PIN, HIGH);
}
