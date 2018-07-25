import cv2 
import numpy as np 


vc  = cv2.VideoCapture('test_main.mp4')

cv2.namedWindow('YW mask')
cv2.namedWindow("GS blur")
cv2.namedWindow("Canny Detection")
while True:

    _ , frame = vc.read()

    #YELLOW WHITE MASK
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([0, 0, 30], dtype = 'uint8')
    upper_yellow = np.array([180, 45, 255], dtype = 'uint8')
    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(gray_image, 180, 255)
    mask_yw = cv2.bitwise_or(mask_white, mask_yellow)
    mask_yw_image = cv2.bitwise_and(gray_image, mask_yw)
    
    cv2.imshow("YW mask", mask_yw_image)
  
    #GAUSSIAN BLUR 
    kernel_size = 5
    gauss_gray = cv2.GaussianBlur(mask_yw_image,(5,5),0)
    cv2.imshow("GS blur", gauss_gray)

    #CANNY EDGES 
    low_threshold = 50
    high_threshold = 150
    canny_edges = cv2.Canny(gauss_gray,low_threshold,high_threshold)
    cv2.imshow("Canny Detection", canny_edges)
    
    
    cv2.imshow("Edges", canny_edges)
    minLineLength = 200
    maxLineGap = 200
    lines = cv2.HoughLinesP(canny_edges,1,np.pi/180,100,minLineLength,maxLineGap)
    new_frame = frame.copy()
    try:
        if lines:
            for x1,y1,x2,y2 in lines[0]:
                cv2.line(new_frame,(x1,y1),(x2,y2),(0,255,0),2)
                print (x1,y1,x2,y2)
                # flag +=1 
    except:
        pass 
    cv2.imshow('output frame', new_frame)



    key = cv2.waitKey(1)
    if key == 27:
        break
