#CORE ENGINE mk1 

import cv2
import numpy as np
import basic_operations as BO

vc = cv2.VideoCapture("test_main.mp4")

#   Set video height/width
og_width = vc.get(3)
og_height = vc.get(4)
print('width:{0} \nheight:{1}'.format(og_width,og_height))

#   Defining windows
# cv2.namedWindow('input frame',cv2.WINDOW_NORMAL)
# cv2.namedWindow('basic processing',cv2.WINDOW_NORMAL)
# cv2.namedWindow('Mask',cv2.WINDOW_NORMAL)
# cv2.namedWindow('output frame',cv2.WINDOW_NORMAL)


#FIRST PROCESS THE TRACKS FOR A BETTER HOUGH TRANSFORM 

while True:
    
    
    _,basic_frame = vc.read()
    cv2.imshow('input frame', basic_frame)

    #ROI 
    frame = basic_frame[400:720,0:1280]
    cv2.imshow('ROI main', frame)
    
    
    basic_processed_frame = BO.proc_basic(frame,'hsv')
    cv2.imshow('basic processing', basic_processed_frame)

    #COLOR BASED MASKING
    lower_blue = np.array([0, 0, 100])          #150 
    upper_blue = np.array([180, 50, 240])
    mask = cv2.inRange(basic_processed_frame, lower_blue, upper_blue)
    cv2.imshow("Mask", mask)

    imagem = cv2.bitwise_not(mask)

    cv2.imshow("Inverted", imagem)



    key = cv2.waitKey(1)
    if key == 27:
        break