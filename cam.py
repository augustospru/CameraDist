import serial
import cv2
import numpy as np
import time

s = serial.Serial("COM3", 115200)

FRAME_HEAD = b"\x00\xFF"
FRAME_TAIL = b"\xDD"

s.write(b"AT+FPS=10\r") #seta FPS para 10 
time.sleep(0.1)
s.write(b"AT+DISP=3\r") #seta para leitura de usb e display no lcd, disp=1 seta pra UART 
time.sleep(0.1)
s.write(b"AT+BINN=4\r") #seta frame para 25x25 
time.sleep(0.1)
s.flush() #flush buffer

def dist(value: int):
    return ((value/5.1)**2)/10 #distance in cm, If UNIT is 0，the distance between this pixel and top is (p/5.1)^2

while s.is_open:
    if not s.readable():
        continue

    packet = s.read(647) #get whole packet
    idxHead = packet.find(FRAME_HEAD) #locate frame head
    if idxHead < 0:
            continue
    packet = packet [idxHead:] #get packet from frame head
    packet += s.read(647 - len(packet)) #get the rest of the frame

    img = packet[20:645] #get the image
    # print(packet[0:2].hex(' '), packet[10020:10022].hex(' '))
    # distpixel = dist(img[4949])
    # distimg = ([dist(img[i]) for i in range(10000)]) #get the distance for each pixel
    # print(img[4949], distpixel, distimg[4949])
    # for idx, item in enumerate(img):
    #     if dist(item) < 100:
    #         if idx % 100 < 33: print("esquerda")
    #         elif idx % 100 < 66: print("meio")
    #         elif idx % 100 < 100: print("direita")

    byteArray = bytearray()
    byteArray.extend(img)
    
    flatNumpyArray = np.array(byteArray) #convert byte array to numpyarray
    grayImage = flatNumpyArray.reshape(25,25) # Convert the array to make a 100x100 grayscale image.
    grayImageResized = cv2.resize(grayImage, (500,500)) #resize image
    cv2.imshow('frame', grayImageResized)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()