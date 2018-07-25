#drawing in opencv 



import cv2
import numpy as np 

img = cv2.imread('track_paper_test.png')

frame = img 

cv2.namedWindow('mask')

def nothing(x):
    pass

cv2.createTrackbar('h','mask',0,255,nothing)
cv2.createTrackbar('s','mask',0,255,nothing)
cv2.createTrackbar('v','mask',0,255,nothing)



while True:

    
    # get current positions of four trackbars
    h_bar = cv2.getTrackbarPos('h','mask')
    s_bar = cv2.getTrackbarPos('s','mask')
    v_bar = cv2.getTrackbarPos('v','mask')

    cv2.imshow("Frame",frame)

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    cv2.imshow("hsv",hsv)

    lower_black = np.array([0,0,0])
    upper_black = np.array([h_bar,s_bar,v_bar])

    mask = cv2.inRange(hsv,lower_black,upper_black)

    cv2.imshow("mask",mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

   