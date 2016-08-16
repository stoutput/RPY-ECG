#!/usr/bin/env python
 
import os
from time import sleep
 
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
GPIO.setup(20, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(12, GPIO.IN)
GPIO.setup(26, GPIO.IN)
GPIO.setup(19, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(6, GPIO.IN)

 
while True:
    if (GPIO.input(21) == True):
        print("1/n")
 
    if (GPIO.input(20) == True):
        print("2/n")
 
    if (GPIO.input(16)== True):
        print("3/n")
        
    if (GPIO.input(12)== True):
        print("4/n")
        
    if (GPIO.input(26)== True):
        print("5/n")
        
    if (GPIO.input(19)== True):
        print("6/n")
        
    if (GPIO.input(13)== True):
        print("7/n")
        
    if (GPIO.input(6)== True):
        print("8/n")
    sleep(0.15);
