#include <Servo.h> 
#include <SPI.h>
#include <PusherClient.h>
#include <Bridge.h>

#include <Adafruit_NeoPixel.h>
#include <avr/power.h>

#define PIN 6

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800);

PusherClient client;
String val;
int led = 13;           // the pin that the LED is attached to
int val_eeg;
int l=0;
int j;
int i;

void setup() {
  
    // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
#if defined (__AVR_ATtiny85__)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif
  // End of trinket special code
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
 
  Serial.begin(9600);
   pinMode(led, OUTPUT);
  Bridge.begin();
  delay(1000);
  Serial.println("coglab pusher setup"); // so I can keep track of what is loaded
   if(client.connect("b8aa4e777b69f94c7803")) {
     client.bind("my_event", set_led);
     client.subscribe("test_channel");
     Serial.println("bind process pusher OK ");
  }
  else {
     Serial.println("BUGGG"); // so I can keep track of what is loaded
  }
}


void loop() {
   delay(30);                
   if (client.connected()) {
        client.monitor();
   }
}

void set_led(String data) {
  Serial.println(data);
   val = data.substring(30,33);
  Serial.println(val);
  val_eeg = (val.toInt() * 60) / 100;
  Serial.println(val_eeg);
  j = val_eeg;
   for(i=0; i<j; i++) {
     strip.setPixelColor(i, strip.Color(127,127, 127));
     strip.show();
    
  }
  
  if (l != 0) {
      for(i=j; i<61; i++) {
         strip.setPixelColor(i, strip.Color(0, 0, 0));
         strip.show();
        
      }
    }
  delay(1000);
  l = j;
  
     
}
