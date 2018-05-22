#ifndef __MATRIX_H
#define __MARTIX_H

#include "Arduino.h"

#define RIGHT_EYE 0
#define LEFT_EYE  1

class Matrix {
  public:
    Matrix();
    void set(uint8_t i, uint8_t y);
    void clear(uint8_t i, uint8_t y);
    void clear();

    void render(); // called from refresh_screen
    // static function for threaded screenrefresh, accepts matrix object pointer
    static void* refresh_screen(void* matrix) {
      Serial.println("start refresh screen");
      while(true) {
        ((Matrix *)matrix)->render();
      }
    }
    void start();
    void write(char c, uint8_t x);
    void write(char c);

	private:
    // screen is encoded as a byte per column
    uint8_t matrix[14] = { 0 };
    void render(int right, int left);
    int pixel(uint8_t x, uint8_t y, uint8_t eye);
};

#endif