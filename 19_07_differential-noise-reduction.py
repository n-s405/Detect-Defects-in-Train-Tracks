# the countour approach 



import cv2
import numpy as np



vc = cv2.VideoCapture('test_main.mp4')


og_width = int(vc.get(3))
og_height = int(vc.get(4))

past =img2_fg = None

def main():




    while True:
        _ , frame = vc.read()
        global past , img2_fg
        
        frame_shaped_01 = shape_set(frame,400,0)  

       
        cv2.imshow('Stuff',frame_shaped_01)


        imgray = cv2.cvtColor(frame_shaped_01,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,125,180,0)
        image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


        if past == None:
            past = image
            img2_fg = image
        else :
            img2_fg = cv2.bitwise_and(past,image)
            past = image
            
        

        cv2.imshow('Stuff2',image)


        cv2.imshow('diff',img2_fg)

        key = cv2.waitKey(1)
        if key == 27 :
            break


def shape_set(input_frame , new_height , new_width):
    result_frame = input_frame[new_height:og_height,new_width:og_width]
    return result_frame


if __name__ == "__main__":
    main()
