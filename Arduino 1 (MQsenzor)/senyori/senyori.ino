#include <LiquidCrystal.h>

/*portovi*/
const int gas_sensor_port = A0;
const int beeper_port = 8;
const int rs = 7, en = 11, d4 = 15, d5 = 14, d6 = 13, d7 = 12;
const int relay_port_1 = 9, relay_port_2 = 10;

int status_value = 0;

/*varijable sa vrednostima*/
int gas_normal_value = 0;
int gas_medium_value = 0;
int gas_high_value = 0;
int gas_current_value = 0;

/*pomocne varijable*/
int counter = 0;
unsigned long start_millis = millis();
unsigned long current_millis = 0;



void setup() {
  pinMode(relay_port_1, OUTPUT);
  pinMode(relay_port_2, OUTPUT);

  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(2, OUTPUT);

  digitalWrite(relay_port_1, LOW);
  digitalWrite(relay_port_2, LOW);

  pinMode(beeper_port,OUTPUT);

  Serial.begin(9600);
}

void loop() {
  LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
  /*initalise gas sesnsor normal value*/
  
  if (counter == 0){
    gas_normal_value = analogRead(gas_sensor_port);
    counter = 1;
  }
  if (counter == 1) {
    current_millis = millis();
    while (current_millis - start_millis < 2000){
      gas_normal_value += analogRead(gas_sensor_port);
      gas_normal_value /= 2;
      current_millis = millis();
      }
      gas_medium_value = gas_normal_value + 50;
      gas_high_value = gas_normal_value + 100;
      counter = 2;
  }
  gas_current_value = analogRead(gas_sensor_port);
  if (gas_current_value >= gas_medium_value && gas_current_value < gas_high_value){
    digitalWrite(relay_port_1, HIGH);
    digitalWrite(relay_port_2, HIGH);
    digitalWrite(4,LOW);
    digitalWrite(3,HIGH);
    digitalWrite(2,LOW);
    status_value = 1;
    
    }
  else{
    if (gas_current_value >= gas_high_value){

       tone(beeper_port,1500);
        lcd.begin(16,2);
        lcd.print("opasnost");
        lcd.setCursor(0,1);
        lcd.print("gasovi");
        digitalWrite(relay_port_1, HIGH);
        digitalWrite(relay_port_2, HIGH);
        digitalWrite(4,LOW);
        digitalWrite(2,HIGH);
        digitalWrite(3,LOW);

        status_value = 2;
      }

      else {
        digitalWrite(relay_port_1,LOW);
        digitalWrite(relay_port_2,LOW);
        digitalWrite(4,HIGH);
        digitalWrite(3,LOW);
        digitalWrite(2,LOW);
        tone(beeper_port,-500);
        status_value = 0;
        }
    }
    if (Serial.read() - '0' == 1){
    Serial.println(status_value);
    }
    
   
  }
