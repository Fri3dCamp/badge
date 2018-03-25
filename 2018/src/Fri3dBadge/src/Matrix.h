#ifndef __MATRIX_H
#define __MARTIX_H

#include "Arduino.h"

#define RIGHT_EYE 0
#define LEFT_EYE  1

class Matrix {
  public:
    Matrix();
    void set(int i, int y);
    void clear(int i, int y);
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

	private:
    // screen is encoded as a byte per column
    int matrix[14] = { 0 };
    void render(int right, int left);
    int pixel(int x, int y, int eye);
};

#endif
