#include <Wire.h>
#include <Servo.h>


int Yvalue,Xvalue,ServoRightLeftValue,ServoUpDownValue;

int EMGsig;           // Store the EMG signal value
int servoPosition;    // The position (angle) value for the servo
int threshold = 425;  // Move the servo when EMG signal is above this threshold. Remember it ranges 0–1023.

long   acceLX ,acceLY ,acceLZ ;
float  gFroceX,gFroceY,gFroceZ;

long   gyroX,gyroY  ,gyroZ;
float  rotX ,rotY   ,rotZ ;

void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);
   Wire.begin();
   //servoRightLeft.attach(9);
   //servoUpDown.attach(8);
   SetupMPU();
   elbowJoint.attach(9); // Tell the servo it is plugged into pin 9
 
    elbowJoint.write(servoPosition); 
  // Move the servo to the ‘servoPosition’ degree
  

}
void SetupMPU()
{
  Wire.beginTransmission(0b1101000); //This is the I2C address of the MPU (b1101000/b1101001 for AC0 low/high datasheet sec. 9.2)
  Wire.write(0x6B); //Accessing the register 6B - Power Management (Sec. 4.28)
  Wire.write(0b00000000); //Setting SLEEP register to 0. (Required; see Note on p. 9)
  Wire.endTransmission();  
  Wire.beginTransmission(0b1101000); //I2C address of the MPU
  Wire.write(0x1B); //Accessing the register 1B - Gyroscope Configuration (Sec. 4.4) 
  Wire.write(0x00000000); //Setting the gyro to full scale +/- 250deg./s 
  Wire.endTransmission(); 
  Wire.beginTransmission(0b1101000); //I2C address of the MPU
  Wire.write(0x1C); //Accessing the register 1C - Acccelerometer Configuration (Sec. 4.5) 
  Wire.write(0b00000000); //Setting the accel to +/- 2g
  Wire.endTransmission();
}
void RecordAccelRegisters()
{
  Wire.beginTransmission(0b1101000);
  Wire.write(0x3B); //Starting register for Accel Readings
  Wire.endTransmission();
  Wire.requestFrom(0b1101000,6); //Request Accel Registers (3B - 40)
 while(Wire.available() < 6);
  acceLX = Wire.read()<<8|Wire.read(); //Store first two bytes into accelX
  acceLY = Wire.read()<<8|Wire.read(); //Store middle two bytes into accelY
  acceLZ = Wire.read()<<8|Wire.read(); //Store last two bytes into accelZ
  ProccessAccelData();
  
}
void ProccessAccelData()
{
   gFroceX=acceLX/16384.0;
   gFroceY=acceLY/16384.0;
   gFroceZ=acceLZ/16384.0;
}
void RecordGyroRegisters()
{
  Wire.beginTransmission(0b1101000);
  Wire.write(0x43);
  Wire.endTransmission();
  Wire.requestFrom(0b1101000,6);
  while(Wire.available()<6);
  
  gyroX = Wire.read()<<8 | Wire.read() ;
  gyroY = Wire.read()<<8 | Wire.read() ;
  gyroZ = Wire.read()<<8 | Wire.read() ;
  ProccessGyroData();
}
void ProccessGyroData()
{
  rotX=gyroX/131.0 ;
  rotY= gyroY/131.0 ;  
  rotZ= gyroZ/131.0 ;
}
void PrintData()
{
  Serial.print("Gyro (deg) ");
  Serial.print(" X=");
  Serial.print(rotX);
  Serial.print(" Y=");
  Serial.print(rotY);
  Serial.print(" Z=");
  Serial.println(rotZ);
  Serial.println();
  Serial.println();
  /////////////////////////////////////
  Serial.print("Accel (deg) ");
  Serial.print(" X=");
  Serial.print(gFroceX);
  Serial.print(" Y=");
  Serial.print(gFroceY);
  Serial.print(" Z=");
  Serial.println(gFroceZ);

  Serial.print(servoPosition);
 Serial.print(" degrees, with EMG: ");
// Serial.println(EMGsig); 
  // Display the servo and EMG values.
 //delay(300); 
  // 1 second (1000ms) delay to not cause it to move as frantically. But this can be adjusted as you like.

  
  ///////////////////////////////////////
   Yvalue=map(acceLX,-16834,16834,-90,90);// I got this number  16834 from the datasheet of MPU for sensitivity it is scale range
   Xvalue=map(acceLY,-16834,16834,-90,90);//-90,90 it is the scale range of the Servo motor  it is 180  degree
   
  ServoRightLeftValue=map(Xvalue,-90,90,179,0);
  ServoUpDownValue=map(Yvalue,-90,90,179,0);
  
  //servoRightLeft.write(ServoRightLeftValue);

  //servoUpDown.write(ServoUpDownValue); 
  elbowJoint.write(ServoRightLeftValue);
}
  


void loop() {
  // put your main code here, to run repeatedly:
  RecordAccelRegisters();
  RecordGyroRegisters();
  PrintData();
  
  EMGsig = analogRead(A0);// Read the analog values of the rectified+integrated EMG signal (0–1023)

  //Serial.println("*******************************");
  Serial.println(EMGsig);
  if (EMGsig < threshold)
{      //if EMG signal is below the threshold
    servoPosition = 20;       // Servo will remain at 20 degrees.
  } 
  else
  {            // If the EMG signal is above the threshold,
   servoPosition=map(EMGsig,threshold,450,20,200); 

   elbowJoint.write(servoPosition);

  // The servo angle will be mapped with the EMG signal, 
  // changing the range of 300(our threshold)-1023 into the range of 20-160 degrees.
  // 20 and 160 can be switched depending on which direction of rotation you want.
  }
}
