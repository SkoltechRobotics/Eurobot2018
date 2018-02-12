/* This minimal example shows how to get single-shot range
measurements from the VL6180X.

The range readings are in units of mm. */

#include <Wire.h>
#include <VL6180X.h>

int serial;


int s1 = 2;
int s2 = 4;
int s3 = 7;
int s4 = 8;
//calibration coefficient
uint8_t p2p_1 = -5;
uint8_t p2p_2 = 5;
uint8_t p2p_3 = 4;
uint8_t p2p_4 = 4;

VL6180X sensor;
VL6180X sensor1;
VL6180X sensor2;
VL6180X sensor3;
VL6180X sensor4;

void setup() 
{
  pinMode(s1,OUTPUT);
  digitalWrite(s1,HIGH);
  pinMode(s2,OUTPUT);
  digitalWrite(s2,HIGH);
  pinMode(s3,OUTPUT);
  digitalWrite(s3,HIGH);
  pinMode(s4,OUTPUT);
  digitalWrite(s4,HIGH);
  
  Serial.begin(9600);
  Wire.begin();
  
  delay(1000);
  
  
  


  digitalWrite(s1,LOW);
  delay(200);
  digitalWrite(s1,HIGH);
  delay(200);
  sensor1.setAddress(81);
  
  sensor1.setTimeout(500);

   
  digitalWrite(s2,LOW);
  delay(200);
  digitalWrite(s2,HIGH);
  delay(200);
  sensor2.setAddress(82);

  sensor2.setTimeout(500);

  digitalWrite(s3,LOW);
  delay(200);
  digitalWrite(s3,HIGH);
  delay(200);
  sensor3.setAddress(83);

  sensor3.setTimeout(500);
  
  digitalWrite(s4,LOW);
  delay(200);
  digitalWrite(s4,HIGH);
  delay(200);
  sensor4.setAddress(84);

  sensor4.setTimeout(500);
  
/*
  Serial.print("I2C_SLAVE__DEVICE_ADDRESS_1_=_");
  Serial.print(sensor1.readReg(0x212));
  Serial.println();
  Serial.print("I2C_SLAVE__DEVICE_ADDRESS_2_=_");
  Serial.print(sensor2.readReg(0x212));
  Serial.println();
  Serial.print("I2C_SLAVE__DEVICE_ADDRESS_3_=_");
  Serial.print(sensor3.readReg(0x212));
  Serial.println();
  Serial.print("I2C_SLAVE__DEVICE_ADDRESS_4_=_");
  Serial.print(sensor4.readReg(0x212));
  Serial.println();
*/
  sensor1.writeReg(0x24, p2p_1);
  /*Serial.print("p2p_offset_1_=_");
  Serial.print(sensor1.readReg(0x024));
  Serial.println();
  */sensor2.writeReg(0x24, p2p_2);
  /*Serial.print("p2p_offset_2_=_");
  Serial.print(sensor2.readReg(0x024));
  Serial.println();
  */sensor3.writeReg(0x24, p2p_3);
  /*Serial.print("p2p_offset_3_=_");
  Serial.print(sensor3.readReg(0x024));
  Serial.println();
  */sensor4.writeReg(0x24, p2p_4);
  /*Serial.print("p2p_offset_=_");
  Serial.print(sensor4.readReg(0x024));
  Serial.println();
*/
  sensor1.init();
  sensor1.configureDefault();
  sensor2.init();
  sensor2.configureDefault();
  sensor3.init();
  sensor3.configureDefault();
  sensor4.init();
  sensor4.configureDefault();

}

void loop() 
{ 
  Serial.print(sensor1.readRangeSingleMillimeters());
  if (sensor1.timeoutOccurred()) { Serial.println(" TIMEOUT"); }
  Serial.print(" ");  
  

  Serial.print(sensor2.readRangeSingleMillimeters());
  if (sensor2.timeoutOccurred()) { Serial.println(" TIMEOUT"); }
  Serial.print(" ");
  
  Serial.print(sensor3.readRangeSingleMillimeters());
  if (sensor3.timeoutOccurred()) { Serial.println(" TIMEOUT"); }
  Serial.print(" ");
  
  Serial.print(sensor4.readRangeSingleMillimeters());
  if (sensor4.timeoutOccurred()) { Serial.println(" TIMEOUT"); }
  Serial.println(" ");
}
