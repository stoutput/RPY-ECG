/*

A sketch to control the 10-Bit, 8-channel ADC MCP3008 on the Rheingold Heavy
I2C and SPI Education Shield at speeds necessary to sample an audio frequency signal.
The code supposes the use of the Education Shield, but if you're using a breakout
board, connect the CS pin to Digital 4, and the SPI pins in their usual locations.

Website:   http://www.rheingoldheavy.com/mcp3008-tutorial-04-sampling-audio-frequency-signals
Datasheet: http://ww1.microchip.com/downloads/en/DeviceDoc/21295d.pdf

*/


#include <SPI.h>                         // Include the SPI library

SPISettings MCP3008(2000000, MSBFIRST, SPI_MODE0);

const int  CS_MCP3008       = 4;          // ADC Chip Select
const byte adc_single_ch0   = (0x08);     // ADC Channel 0
const byte adc_single_ch1   = (0x09);     // ADC Channel 1
const byte adc_single_ch2   = (0x0A);     // ADC Channel 2
const byte adc_single_ch3   = (0x0B);     // ADC Channel 3
const byte adc_single_ch4   = (0x0C);     // ADC Channel 4
const byte adc_single_ch5   = (0x0D);     // ADC Channel 5
const byte adc_single_ch6   = (0x0E);     // ADC Channel 6
const byte adc_single_ch7   = (0x0F);     // ADC Channel 7

void setup()
{

  SPI.begin     ();
  Serial.begin  (9600);
  pinMode       (CS_MCP3008, OUTPUT);
  digitalWrite  (CS_MCP3008, LOW);        // Cycle the ADC CS pin as per datasheet
  digitalWrite  (CS_MCP3008, HIGH);
  
  delay(100);
  
  for (int i = 0; i < 500; i++) {
    int adc_reading = 0;
    adc_reading = adc_single_channel_read (adc_single_ch7);
    Serial.println (adc_reading);
  }

}

