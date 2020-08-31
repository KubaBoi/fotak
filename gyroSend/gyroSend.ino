// Arduino gyroskop a akcelerometr 2

// knihovny potřebné pro modul
#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"

// nastavení adresy modulu
// 0x68 nebo 0x69, dle připojení AD0
// MPU6050 mpu(0x69)
MPU6050 mpu;
// číslo pinu s LED diodou pro notifikaci
#define LED_PIN 13 
#define TAKESHOT_PIN 3
#define RECORDING_PIN 4
#define REC_DIOD 5

bool recording = false;

// inicializace proměnných, do kterých se uloží data
bool dmpReady = false;
uint8_t mpuIntStatus;
uint8_t devStatus;
uint16_t packetSize;
uint16_t fifoCount;
uint8_t fifoBuffer[64];

// inicializace proměnných pro výpočet
Quaternion q;           // [w, x, y, z] kvaternion
VectorFloat gravity;    // [x, y, z] vektor setrvačnosti
float rotace[3];        // rotace kolem os x,y,z

// Rutina přerušení
volatile bool mpuInterrupt = false;
void dmpINT() {
  mpuInterrupt = true;
}

void setup() {
  // nastavení LED jako výstupní
  pinMode(LED_PIN, OUTPUT);
  // nastavení I2C sběrnice
  Wire.begin();
  // komunikace přes sériovou linku rychlostí 115200 baud
  Serial.begin(115200);
  while (!Serial);
  // inicializace akcelerometru a gyroskopu
  mpu.initialize();
  // incializace DMP
  devStatus = mpu.dmpInitialize();
  // kontrola funkčnosti DMP
  if (devStatus == 0) {
      // zapnutí DMP
      mpu.setDMPEnabled(true);
      // nastavení pinu INT jako přerušovacího, interrupt 0 odpovídá pinu 2
      attachInterrupt(0, dmpINT, RISING);
      mpuIntStatus = mpu.getIntStatus();
      dmpReady = true;
      // načtení velikosti zpráv, které bude DMP posílat
      packetSize = mpu.dmpGetFIFOPacketSize();
  }
  digitalWrite(LED_PIN, LOW);
}

//paket se sklada z rotace, a tlacitek
//rotace <0, 180>
//tlacitka 0/1
//|x,y,z,vyfotit,natacet|
void loop() {
  String data = "";

  data += getRotation();
  data += "," + takeShot();
  data += "," + takeRecording();

  if (recording) digitalWrite(REC_DIOD, HIGH);
  else digitalWrite(REC_DIOD, LOW);
  
  Serial.println(data);
}

String oldData = "0,0,0";
String getRotation() {
  if (!dmpReady) return oldData;
  
  mpuInterrupt = false;
  mpuIntStatus = mpu.getIntStatus();
  fifoCount = mpu.getFIFOCount();
  if ((mpuIntStatus & 0x10) || fifoCount == 1024) {
      mpu.resetFIFO();
  }
  else if (mpuIntStatus & 0x02) {
      while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();
      mpu.getFIFOBytes(fifoBuffer, packetSize);
      fifoCount -= packetSize;
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      mpu.dmpGetGravity(&gravity, &q);
      mpu.dmpGetYawPitchRoll(rotace, &q, &gravity);
  
      int x = rotace[2] * 180/M_PI;
      int y = rotace[1] * 180/M_PI;
      int z = rotace[0] * 180/M_PI;
  
      String data = String(x) + "," + String(y) + "," + String(z);
      oldData = data;
      return data;
  }
  return oldData;
}

int oldButtonTakeShot = 0;
String takeShot() {
  String response = "";
  int buttonState = digitalRead(TAKESHOT_PIN);
  if (buttonState == 1 && oldButtonTakeShot != buttonState) {
    response = "1";
  }
  else {
    response = "0";
  }
  
  oldButtonTakeShot = buttonState;
  return response;
}

int oldButtonRecording = 0;
String takeRecording() {
  String response = "";
  int buttonState = digitalRead(RECORDING_PIN);
  if (buttonState == 1 && oldButtonRecording != buttonState) {
    response = "1";
    if (recording) recording = false;
    else recording = true;  
  }
  else {
    response = "0";
  }
  oldButtonRecording = buttonState;
  return response;
}
