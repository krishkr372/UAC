// Install Arduino IDE 
// Install libraries: Adafruit GFX and Adafruit SSD1306 
// Connect the OLED display to the Arduino using I2C (SDA to A4, SCL to A5 for Arduino Uno)
// Upload the following code to the Arduino in required port.


#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32  
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

String inputString = "";         
bool stringComplete = false;     

void setup() {
  Serial.begin(9600);
  inputString.reserve(200);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(2);
  display.setCursor(0, 10); 
  display.println("SLI Ready...");
  display.display();
}

void loop() {
  if (stringComplete) {
    display.clearDisplay();
    
    // Wipe out accidental leading/trailing spaces from the raw stream
    inputString.trim(); 
    int textLength = inputString.length();
    
    if (textLength == 0) {
      // Clear display when an empty string is received (on space erase)
      display.display();
    } 
    else {
      // DYNAMIC FONT SCALING: Adjust size so text always stays on line
      if (textLength <= 5) {
        display.setTextSize(3);   // Large text for short words or the first few letters
        display.setCursor(4, 4);  // Small margin shift
      } 
      else if (textLength <= 10) {
        display.setTextSize(2);   // Medium text as the word grows
        display.setCursor(2, 8);  
      } 
      else {
        display.setTextSize(1);   // Small text for long words
        display.setCursor(0, 12); 
      }
      
      display.println(inputString);
      display.display();
    }
    
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}
