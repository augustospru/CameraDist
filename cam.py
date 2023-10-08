import serial
import cv2
import numpy as np
import time

s = serial.Serial("COM3", 11520)

FRAME_HEAD = b"\x00\xFF"
FRAME_TAIL = b"\xDD"

s.write(b"AT+FPS=10\r") #seta FPS para 10 
time.sleep(0.1)
s.write(b"AT+DISP=3\r") #seta para leitura de usb e display no lcd, disp=1 seta pra UART 
time.sleep(0.1)
s.flush() #flush buffer

while s.is_open:
    if not s.readable():
        continue

    packet = s.read(10022)
    idxHead = packet.find(FRAME_HEAD)
    if idxHead < 0:
            continue
    packet = packet [idxHead:]
    packet += s.read(10022 - len(packet))

    img = packet[20:10020]
    # print(packet[0:2].hex(' '), packet[10020:10022].hex(' '))
    dist = ((img[4949]/5.1)**2)/10 #distance in cm, If UNIT is 0，the distance between this pixel and top is (p/5.1)^2
    print(img[4949], dist)

    byteArray = bytearray()
    byteArray.extend(img)
    
    flatNumpyArray = np.array(byteArray) #convert byte array to numpyarray
    grayImage = flatNumpyArray.reshape(100,100) # Convert the array to make a 100x100 grayscale image.
    grayImageResized = cv2.resize(grayImage, (500,500)) #resize image
    cv2.imshow('frame', grayImageResized)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()