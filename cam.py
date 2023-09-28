import serial
import cv2
import numpy as np

s = serial.Serial("COM3", 115200)

FRAME_HEAD = b"\x00\xFF"
FRAME_TAIL = b"\xDD"

s.write(b"AT+DISP=3\r") #seta para leitura de usb, disp=1 seta pra UART 
# s.write(b"AT+FPS=15\r") #seta FPS para 10 

s.flush() #flush buffer
while True:
    head = s.read_until(FRAME_HEAD)

    if head.__len__() != 19:
        continue
    print(head.hex(' '))

    img = s.read(10002)

    byteArray = bytearray()
    byteArray.extend(img)
    byteArray = byteArray[:10000] #remove frame_head
    
    flatNumpyArray = np.array(byteArray) #convert byte array to numpyarray
    # Convert the array to make a 100x100 grayscale image.
    grayImage = flatNumpyArray.reshape(100, 100)
    grayImageResized = cv2.resize(grayImage, (500,500)) #resize image
    cv2.imshow('frame', grayImageResized)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()