import cv2
import numpy as np
import copy  

frame = cv2.imread('track_paper_test.png')

cv2.namedWindow("hsv")
contour_counter = 0 
while True:
    contour_counter  = 0 
    #basic processing
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    cv2.imshow("main",frame)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv",hsv)
    
    #masking the color
    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([130, 145, 110])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow("Mask", mask)
 
    #Contouring
    new_frame = frame.copy()
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
 
        if area > 5000:
            cv2.drawContours(new_frame, contour, -1, (0, 255, 0), 3)
            contour_counter  += 1
  
    cv2.imshow("Frame", new_frame)
    print(contour_counter)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
 

cv2.destroyAllWindows()