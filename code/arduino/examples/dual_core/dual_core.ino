#define LED1 2
TaskHandle_t Task1;
TaskHandle_t Task2;

void codeForTask1( void * parameter )
{
  for (;;) {
    Serial.print("The first Task runs on Core: ");
    Serial.println(xPortGetCoreID());
    digitalWrite(LED1, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);                       // wait for a second
    digitalWrite(LED1, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);                       // wait for a second
  }
}

void codeForTask2( void * parameter )
{
  for (;;) {
    Serial.print("The second Task runs on Core: ");
    Serial.println(xPortGetCoreID());
    delay(2000);                       // wait for a second
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED1, OUTPUT);
  xTaskCreatePinnedToCore(
    codeForTask1,            /* Task function. */
    "Task_1",                 /* name of task. */
    1000,                    /* Stack size of task */
    NULL,                     /* parameter of the task */
    1,                        /* priority of the task */
    &Task1,                   /* Task handle to keep track of created task */
    0);                       /* Core */

  xTaskCreatePinnedToCore(
    codeForTask2,            /* Task function. */
    "Task_2",                 /* name of task. */
    1000,                    /* Stack size of task */
    NULL,                     /* parameter of the task */
    1,                        /* priority of the task */
    &Task2,                   /* Task handle to keep track of created task */
    1);                       /* Core */
}

// the loop function runs over and over again forever
void loop() {
  Serial.print("The main loop runs on Core: ");
  Serial.println(xPortGetCoreID());
  delay(2000);
}