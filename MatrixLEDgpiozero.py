#!/usr/bin/env python3
#############################################################################
# Filename    : LEDMatrix.py
# Description : Control LEDMatrix with 74HC595 using gpiozero
# Author      : www.freenove.com
# Modification: 2021/11/22
########################################################################
from gpiozero import DigitalOutputDevice
import time

LSBFIRST = 1
MSBFIRST = 2

# Define the pins connect to 74HC595
dataPin = DigitalOutputDevice(17, active_high=True)  # DS Pin of 74HC595(Pin14)
latchPin = DigitalOutputDevice(27, active_high=True)  # ST_CP Pin of 74HC595(Pin12)
clockPin = DigitalOutputDevice(22, active_high=True)  # SH_CP Pin of 74HC595(Pin11)

pic = [0x1c, 0x22, 0x51, 0x45, 0x45, 0x51, 0x22, 0x1c]  # data of a smiling face

data = {
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    '0': [0x00, 0x00, 0x3E, 0x41, 0x41, 0x3E, 0x00, 0x00],
    '1': [0x00, 0x00, 0x21, 0x7F, 0x01, 0x00, 0x00, 0x00],
    '2': [0x00, 0x00, 0x23, 0x45, 0x49, 0x31, 0x00, 0x00],
    '3': [0x00, 0x00, 0x22, 0x49, 0x49, 0x36, 0x00, 0x00],
    '4': [0x00, 0x00, 0x0E, 0x32, 0x7F, 0x02, 0x00, 0x00],
    '5': [0x00, 0x00, 0x79, 0x49, 0x49, 0x46, 0x00, 0x00],
    '6': [0x00, 0x00, 0x3E, 0x49, 0x49, 0x26, 0x00, 0x00],
    '7': [0x00, 0x00, 0x60, 0x47, 0x48, 0x70, 0x00, 0x00],
    '8': [0x00, 0x00, 0x36, 0x49, 0x49, 0x36, 0x00, 0x00],
    '9': [0x00, 0x00, 0x32, 0x49, 0x49, 0x3E, 0x00, 0x00],
    'A': [0x00, 0x00, 0x3F, 0x44, 0x44, 0x3F, 0x00, 0x00],
    'B': [0x00, 0x00, 0x7F, 0x49, 0x49, 0x36, 0x00, 0x00],
    'C': [0x00, 0x00, 0x3E, 0x41, 0x41, 0x22, 0x00, 0x00],
    'D': [0x00, 0x00, 0x7F, 0x41, 0x41, 0x3E, 0x00, 0x00],
    'E': [0x00, 0x00, 0x7F, 0x49, 0x49, 0x41, 0x00, 0x00],
    'F': [0x00, 0x00, 0x7F, 0x48, 0x48, 0x40, 0x00, 0x00],
}


def shiftOut(order, val):
    for i in range(0, 8):
        clockPin.off()
        if order == LSBFIRST:
            dataPin.value = (0x01 & (val >> i) == 0x01)
        elif order == MSBFIRST:
            dataPin.value = (0x80 & (val << i) == 0x80)
        clockPin.on()


def setup():
    pass  

def matrix_display(arr, duration):
    for j in range(0, duration):
        x = 0x80
        for i in range(0, 8):
            latchPin.off()
            shiftOut(MSBFIRST, arr[i])  # First shift data of line information to the first stage 74HC959
            shiftOut(MSBFIRST, ~x)  # Then shift data of column information to the second stage 74HC959
            latchPin.on()  # Output data of two-stage 74HC595 at the same time
            time.sleep(0.001)  # Display the next column
            x >>= 1


def loop():
    while True:
        for j in range(0, 1):  # Repeat enough times to display the smiling face a period of time
            x = 0x80
            for i in range(0, 8):
                latchPin.off()
                shiftOut(MSBFIRST, pic[i])  # First shift data of line information to the first stage 74HC959

                shiftOut(MSBFIRST, ~x)  # Then shift data of column information to the second stage 74HC959
                latchPin.on()  # Output data of two-stage 74HC595 at the same time
                time.sleep(0.001)  # Display the next column
                x >>= 1
        for k in range(0, len(data)):  # len(data) total number of "0-F" columns
            for j in range(0, 20):  # Times of repeated displaying LEDMatrix in every frame, the bigger the "j", the longer the display time.
                x = 0x80  # Set the column information to start from the first column
                for key in data:
                   matrix_display(data[key],100) 
                # for i in range(k, k + 8):
                #     latchPin.off()
                #     shiftOut(MSBFIRST, data[i])
                #     shiftOut(MSBFIRST, ~x)
                #     latchPin.on()
                #     time.sleep(0.001)
                #     x >>= 1


picTest = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]


def testLED():
    print("test led")
    # Display each of the 64 LEDs from left to right, top to bottom for 0.1 seconds each.
    x = 0x80
    for i in range(0, 64):
        latchPin.off()
        shiftOut(MSBFIRST, picTest[i % 8])  # First shift data of line information to first stage 74HC959
        shiftOut(MSBFIRST, ~x)  # Then shift data of column information to second stage 74HC959
        latchPin.on()  # Output data of two-stage 74HC595 at the same time
        time.sleep(0.1)  # Display the next column
        if i in [7, 15, 23, 31, 39, 47, 55]:
            x >>= 1


def destroy():
    latchPin.off()
    dataPin.off()
    clockPin.off()

def displayMessage(message):
    for char in message:
        try:
            matrix_display(data[char],100)
        except:
            matrix_display(data[" "],100)
    matrix_display(data[" "],1)



if __name__ == '__main__':  # Program entrance
    print('Program is starting...')
    try:
        # testLED()
        # loop()
        matrix_display(pic,100)
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
