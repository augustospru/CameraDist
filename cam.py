import serial
import cv2
import numpy as np
import time
import threading
import RPi.GPIO as GPIO
import os

def dist(value: int):
    return ((value/5.1)**2)/10 #distance in cm, If UNIT is 0，the distance between this pixel and top is (p/5.1)^2

def vibration_main(dist: float, idx: int): #main vibration controller
    if dist < 150:
        idx_relative = idx % 25 # module by frame to get every line
        if idx_relative < 8: 
            GPIO.output(GPIO_1, True) # vibrates left motor
        elif idx_relative < 16: 
            GPIO.output(GPIO_2, True) # vibrates middle motor
        elif idx_relative < 25: 
            GPIO.output(GPIO_3, True) # vibrates right motor
            
def unpack(packet: list[int]): #function to unpack frame packet and send to vibrate
    for idx, value in enumerate(packet):
        vibration_main(dist(value), idx)

s = serial.Serial("/dev/ttyUSB0", 115200) # init serial for communication

FRAME_HEAD = b"\x00\xFF"
FRAME_TAIL = b"\xDD"

s.write(b"AT+FPS=10\r") #seta FPS para 10 
time.sleep(0.1)
s.write(b"AT+DISP=3\r") #seta para leitura de usb e display no lcd, disp=1 seta pra UART 
time.sleep(0.1)
s.write(b"AT+BINN=4\r") #seta frame para 25x25
time.sleep(0.1)
s.flush() #flush buffer

# Define GPIO to use on Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_1 = 4
GPIO_2 = 3
GPIO_3 = 2

#define GPIO as outputs
GPIO.setup(GPIO_1, GPIO.OUT)
GPIO.setup(GPIO_2, GPIO.OUT)
GPIO.setup(GPIO_3, GPIO.OUT)

while s.is_open:
    if not s.readable():
        continue

    packet = s.read(647) #get whole packet
    idxHead = packet.find(FRAME_HEAD) #locate frame head
    if idxHead < 0:
            continue
    
    packet = packet [idxHead:] #get packet from frame head
    packet += s.read(647 - len(packet)) #get the rest of the frame
    
    #initiate vibrate motors with false
    GPIO.output(GPIO_1, False)
    GPIO.output(GPIO_2, False)
    GPIO.output(GPIO_3, False)

    #instanciate threads
    vibration_thread = threading.Thread(target=unpack, args=(packet[20:645],))
    vibration_thread.run()
