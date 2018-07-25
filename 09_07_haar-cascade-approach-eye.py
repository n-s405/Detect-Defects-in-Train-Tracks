import cv2
import numpy as np
 
cap = cv2.VideoCapture(0)

path = 'haarcascade_eye.xml'
 
while True:
    _, frame = cap.read()
    # blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    eye_cascade = cv2.CascadeClassifier(path)

    eyes = eye_cascade.detectMultiScale(gray , scaleFactor=1.02 , minNeighbors = 20 , minSize = (10,10))

    print(len(eyes))

    for (x , y , w , h ) in eyes :
        xC = (x + x+w)/2
        yC = (y + y+h)/2
        radius = w/2 
        cv2.circle(frame,(int(xC),int(yC)),int(radius),(255,0,0),2)

    cv2.imshow("Frame", frame)
 
    key = cv2.waitKey(1)
    if key == 27:
        break
 
cap.release()
cv2.destroyAllWindows()