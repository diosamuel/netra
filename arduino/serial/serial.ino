

int buttonPin = 4;    // Pin where Button 1 is connected
int buttonPin2 = 5;   // Pin where Button 2 is connected
int buttonPin3 = 6;   // Pin where Button 3 is connected
int buttonPin4 = 7;

int buttonState = HIGH;  // Initialize with HIGH due to pull-up resistor
int buttonState2 = HIGH;
int buttonState3 = HIGH;
int buttonState4 = HIGH;
bool state = true;  // Global state variable to track detection
bool detected = false;  // New variable to track if someone is currently detected
#define echoPin 2 // pin 2 arduino koneksi ke pin echo dari sensor
#define trigPin 3 //pin 3 arduino koneksi ke pin trig dari sensor
long duration; // variabel duration bertipe data long
int distance; 

void setup() {
  // Set button pins as INPUT_PULLUP to enable internal pull-up resistors
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(buttonPin3, INPUT_PULLUP);
  pinMode(buttonPin4, INPUT_PULLUP);
  pinMode(trigPin, OUTPUT); // trigPin sebagai output
  pinMode(echoPin, INPUT); // echoPin sebagai input

  Serial.begin(9600);
  Serial.println("Ultrasonic Sensor HC-SR04");
  Serial.println("with Arduino UNO R3");
  delay(2000);
}

void loop() {
  // Read the state of the buttons
  buttonState = digitalRead(buttonPin);
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);
  buttonState4 = digitalRead(buttonPin4);


  // Check if Button 1 is pressed (LOW due to pull-up resistor)
  if (buttonState == LOW) {
    Serial.println("btn.1");
    delay(100);
  }
  // Check if Button 2 is pressed
  else if (buttonState2 == LOW) {
    Serial.println("btn.2");
    delay(100);
  }
  // Check if Button 3 is pressed
  else if (buttonState3 == LOW) {
    Serial.println("btn.3");
    delay(100);
  }
// Check if Button 3 is pressed
  // else if (buttonState4 == LOW) {
  //   Serial.println("btn.4");
  //   delay(100);
  // }else{

  // }

  // kondisi trigPin ke 0 (LOW)
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // atur trigPin HIGH (aktif) selama 10 ms
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // membaca echoPin, durasi waktu gelombang ke ms
  duration = pulseIn(echoPin, HIGH);
  // menghitung jarak
  distance = duration * 0.034 / 2; // kecepatan suara dibagi 2 (datang dan kembali)
  
  // Check distance and toggle detection state accordingly
  if (distance < 30 && !detected) {  // Detect when someone hovers for the first time
    Serial.println("jarak.1");
    detected = true;  // Set detected to true to avoid repeating the message
  }
  
  if (distance >= 30 && detected) {  // Detect when the person moves away for the first time
    Serial.println("jarak.0");
    detected = false;  // Set detected to false to avoid repeating the message
  }

  delay(100);  // Short delay before next loop iteration
}
