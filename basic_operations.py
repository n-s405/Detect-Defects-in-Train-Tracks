
import numpy 
import cv2 



def proc_basic(processFrame, colorOperation = 'hsv'):

    process_frame_1 = cv2.GaussianBlur(processFrame, (5, 5), 10)

    if colorOperation  == 'hsv':
        color_processed = cv2.cvtColor(process_frame_1, cv2.COLOR_BGR2HSV)
    elif colorOperation == 'gray':
        color_processed = cv2.cvtColor(process_frame_1, cv2.COLOR_BGR2HSV)

    return color_processed
    