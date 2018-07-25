


import cv2 
import numpy as np 



vc = cv2.VideoCapture('test_main.mp4')

flag_picture_init = 1

def main():
    
    og_width = vc.get(3)
    og_height = vc.get(4)
    print(og_height)

    while True:

        _ , frame_raw_unshaped = vc.read()

        frame_raw = frame_raw_unshaped[500:int(og_height)]
        #find difference between 2 frames 



        #Absolute Difference of the two frames 
        mask_diff_main = frame_difference_mask(frame_raw)
        

        #Some processing on the frames 
        blur_mask = cv2.blur(mask_diff_main,(5,5))
        blur_frame_raw = cv2.blur(frame_raw,(5,5))
        frame_subtracted = cv2.bitwise_and(blur_mask,blur_frame_raw)
        invert_img = cv2.bitwise_not(mask_diff_main)

        gray  = invert_img
        #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    

        #video out 
        cv2.imshow('difference',mask_diff_main)
        cv2.imshow('subtracted frame',frame_subtracted)  
        cv2.imshow('blurred frame',blur_frame_raw) 

    




        key = cv2.waitKey(1)
        if key == 27:
            break 






def frame_difference_mask(current_frame):
    global flag_picture_init

    if flag_picture_init :
        cv2.imwrite('old.png',current_frame)
        flag_picture_init= 0

    frame_old = cv2.imread('old.png',1)       
    mask_diff_main = cv2.absdiff(frame_old,current_frame)
    cv2.imwrite('old.png',current_frame)

    return mask_diff_main

    




if __name__ == "__main__":
    main()