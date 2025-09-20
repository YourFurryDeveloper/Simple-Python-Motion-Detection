import cv2
import math
import time

camFeed = cv2.VideoCapture(0)

lastFramePixelDat = 0

if not camFeed.isOpened():
    print("Error: Could not open camera.")
    exit()

i = 0
while True:
    ret, frame = camFeed.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    curFramePixelDat = sum(cv2.mean(frame))
    #print("Frame", curFramePixelDat)
    
    if curFramePixelDat > lastFramePixelDat + 3:
        print("Motion detected!", i)
        i += 1
    lastFramePixelDat = curFramePixelDat

    #cv2.imshow('Camera Feed', pixelCaptureRegion)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camFeed.release()
cv2.destroyAllWindows()