#CORE ENGINE mk1 
#notes : basic line filtering works . change the v value to assert for differences 
import cv2
import numpy as np
import basic_operations as BO


font = cv2.FONT_HERSHEY_SIMPLEX
#vc = cv2.VideoCapture('test_main_1.mov')
vc = cv2.VideoCapture('test_main.mp4')
#vc = cv2.VideoCapture('test_main_2.mp4',)

#   Set video height/width
og_width = vc.get(3)
og_height = vc.get(4)
print('width:{0} \nheight:{1}'.format(og_width,og_height))

#   Defining windows
# cv2.namedWindow('input frame',cv2.WINDOW_NORMAL)
# cv2.namedWindow('basic processing',cv2.WINDOW_NORMAL)
# cv2.namedWindow('Mask',cv2.WINDOW_NORMAL)
# cv2.namedWindow('output frame',cv2.WINDOW_NORMAL)

xAv = 160 
yAv = 640
#FIRST PROCESS THE TRACKS FOR A BETTER HOUGH TRANSFORM 

while True:
    
    no_of_lines = 0
    _,basic_frame = vc.read()
    cv2.imshow('input frame', basic_frame)

    #ROI 
    frame = basic_frame[400:720,0:1280]
    cv2.imshow('ROI main', frame)
    
    
    basic_processed_frame = BO.proc_basic(frame,'hsv')
    cv2.imshow('basic processing', basic_processed_frame)

    #COLOR BASED MASKING
    lower_blue = np.array([0, 15, 100])          #150 
    upper_blue = np.array([180, 50, 240])
    mask = cv2.inRange(basic_processed_frame, lower_blue, upper_blue)
    cv2.imshow("Mask", mask)


    #inverted image
    imagem = cv2.bitwise_not(mask)
    cv2.imshow("Inverted", imagem)
    
    #smoothing image
    gauss_mask = cv2.GaussianBlur(mask, (5, 5), 10)
    cv2.imshow("gauss2", gauss_mask)

    edges = cv2.Canny(gauss_mask,10,150,apertureSize = 3)
    cv2.imshow("Canny Output", edges)

    lines = cv2.HoughLinesP(edges,rho = 1,theta = 1*np.pi/180,threshold = 90,minLineLength = 150,maxLineGap = 100)
    
    frame_new = frame 

    print(lines)
    
    if lines == None:
        pass
    else:
        print('success')
        for line in lines:   
            no_of_lines +=1 ;
             
            
            for x1,y1,x2,y2 in line:
                cv2.line(frame_new,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.circle(frame_new,(x1,y1),2,(0,0,255),-1)
                cv2.circle(frame_new,(x2,y2),2,(0,0,255),-1)
                cv2.putText(frame_new,'{0} {1}'.format(x1,y1),(x1,y1),font,0.7,(255,255,255),1,cv2.LINE_AA)
                cv2.putText(frame_new,'{0} {1}'.format(x2,y2),(x2,y2),font,0.7,(255,255,255),1,cv2.LINE_AA)
                xAv = (x1 + x2 + xAv)/3
                yAv = (y1 + y2 + yAv)/3
                #if x1<x2 and y1<y2:
                  #  print(' {} {} {} {}'.format(x1,x2,y1,y2)) 
                    #newIm = frame_new[x1:x2,y1:y2]
                    #cv2.imshow("somethi ng{}.jpg".format(x1),newIm)
                    #cv2.imshow("last frame",final_image)
            if no_of_lines > 3:
                break 
    
    cv2.putText(frame_new,'no of lines :{0}'.format(no_of_lines),(40,100),font,1,(255,255,255),1,cv2.LINE_AA)
    #cv2.circle(frame_new,(int(xAv),int(yAv)),3,(0,255,255),-1)
    cv2.imshow("Output Image", frame_new)
    

    

    key = cv2.waitKey(1)
    if key == 27:
        break