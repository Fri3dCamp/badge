#ifndef __MATRIX_H
#define __MARTIX_H

#include "Arduino.h"



class Matrix {
  public:
    Matrix();

    void start();

    void set(uint8_t eye, uint8_t x, uint8_t y);
    void clear(uint8_t eye);
    

	private:
    uint8_t buffer[10] = { 0 };
    void render(uint8_t* buffer, uint8_t row);
    void renderTask();
    static void startTaskImpl(void*);
    TaskHandle_t video_task;
};

#endif
