#include <Servo.h>

// SERVO MOTOR PIN
#define UD_SERVO    6
#define LR_SERVO    9

Servo   ud_servo;
Servo   lr_servo;
int     UD,LR,NS=0;

void catch_command();
void reset_command();
void run_command();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ud_servo.attach(UD_SERVO);
  lr_servo.attach(LR_SERVO);
}

void loop() {
  if(Serial.available() >= (sizeof(char)*5)) catch_command();
  if(NS >= 50) reset_command();
  delay(200);
}

void catch_command() {
  Serial.println("catch");
  NS = 0;
  switch(Serial.read()) {
    case 'U': UD = ((Serial.read()-48)*10)+((Serial.read()-48)); break;
    case 'L': LR = ((Serial.read()-48)*100)+((Serial.read()-48)*10)+((Serial.read()-48)); break;
    default : NS++; break;
  }
  run_command();
}

void reset_command() {
  UD = 60;
  LR = 90;
  run_command();
}


void run_command() {
  ud_servo.write(UD);
  lr_servo.write(LR);
}
