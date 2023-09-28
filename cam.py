import serial
import cv2
import numpy as np

s = serial.Serial("COM3", 115200)

FRAME_HEAD = b"\x00\xFF"
FRAME_TAIL = b"\xCC"

s.write(b"AT+DISP=3\r") #seta para leitura de usb, disp=1 seta pra UART 

#_ = s.read_until(FRAME_HEAD)
while s.is_open:
    res = s.read(10019)
    # print("length", res.__len__())
    # if res.__len__() < 1000: 
    #     continue
    # print(res)
    # byteArray = bytearray(10000 - res.__len__())
    byteArray = bytearray()
    byteArray.extend(res)
    byteArray = byteArray[:10000]
    
    flatNumpyArray = np.array(byteArray) #convert byte array to numpyarray
    # Convert the array to make a 100x100 grayscale image.
    grayImage = flatNumpyArray.reshape(100, 100)
    grayImageResized = cv2.resize(grayImage, (500,500)) #resize image
    cv2.imshow('frame', grayImageResized)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()