import cv2
import numpy as np

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)


if vc.isOpened(): 
    rval, frame = vc.read()
else:
    rval = False

while rval:
    #conveting from rgb to hsv 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_face = np.array([80,70,40])
    upper_face = np.array([200,150,160])

    mask = cv2.inRange(hsv, lower_face, upper_face)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
   
    cv2.resizeWindow('frame', 100,100)
    cv2.imshow('frame',frame)

    
    cv2.resizeWindow('mask', 100,100)
    cv2.imshow('mask',mask)
    
    cv2.resizeWindow('image', 100,100)
    cv2.imshow('res',res)

    rval, frame = vc.read()
    key = cv2.waitKey(1)
    if key == 27: #Exit Condition
        break

# cv2.destroyWindow("Webcam Feed")
cv2.destroyAllWindows()

vc.release()
