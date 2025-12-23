#include <Arduino.h>

void setup()
{
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  pinMode(22, OUTPUT);

  digitalWrite(4, LOW);
  digitalWrite(22, HIGH);
}

void loop()
{
  if (touchRead(14) <= 75)
  {
    Serial.println("Detected touch");
    digitalWrite(4, HIGH);
    digitalWrite(22, LOW);

    sleep(1);
    digitalWrite(4, LOW);
    digitalWrite(22, HIGH);
    touchRead(14);
  }
}
