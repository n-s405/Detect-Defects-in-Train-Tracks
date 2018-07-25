# ENTRY DYNAMIC MASKING 

# p to pause and select parts in the video and see the masked output


import cv2
import numpy  as np 
import math

# BASIC SETUP 
font = cv2.FONT_HERSHEY_SIMPLEX
vc = cv2.VideoCapture('test_main.mp4')


#DYNAMIC GRADATION
# xX=0 # variable used in averaging 
# yY=0
#Average Variabsles
h_av =  90 
s_av = 110
v_av =  110
#Calculation Variables
transfer_photo = None
h_l=h_u=s_l=s_u=v_l=v_u = None
lower_thresh = upper_thresh = 0 


og_width = int(vc.get(3))
og_height = int(vc.get(4))
print('width:{0} \nheight:{1}'.format(og_width,og_height))



def main():

    line_av = 0 
    xAv = 160 
    yAv = 640

    while True:
        no_of_lines = 0
        _, frame_raw = vc.read()
        
        #SET NEW HEIGHT AND WIDTH
        frame_shaped_01 = shape_set(frame_raw,400,0)    #set height and width

        print(frame_shaped_01.shape)
        cv2.imshow('frame',frame_shaped_01)
        
        global transfer_photo
        transfer_photo= cv2.cvtColor(frame_shaped_01, cv2.COLOR_BGR2HSV)
        
        next_frame = transfer_photo


        global lower_thresh , upper_thresh 
        frame_blurred_01 = cv2.GaussianBlur(next_frame, (5, 5), 10)
        mask = cv2.inRange(frame_blurred_01, lower_thresh, upper_thresh)
        cv2.imshow('Mask', mask)

        #smoothing image
        gauss_mask = cv2.GaussianBlur(mask, (5, 5), 10)
        cv2.imshow("gauss2", gauss_mask)
        cv2.imwrite('old_mask.png',gauss_mask)
        oldie = cv2.imread('old_mask.png',0)
        image1 = cv2.bitwise_and(gauss_mask,oldie)
        cv2.imshow('mask difference',image1)
        cv2.imwrite('old_mask.png' , gauss_mask)

        edges = cv2.Canny(image1,10,150,apertureSize = 3)
        cv2.imshow("Canny Output", edges)

        lines = cv2.HoughLinesP(edges,rho = 1,theta = 1*np.pi/180,threshold = 90,minLineLength = 150,maxLineGap = 100)

        frame_new= cv2.cvtColor(next_frame, cv2.COLOR_HSV2BGR)

        #print(lines)   - PRINT THE LINES ON THE IMAGE 
        

        if lines == None:
            pass
        else:
            print('success')
            for line in lines:   
                no_of_lines +=1 
                
                
                for x1,y1,x2,y2 in line:
                    if abs(y1-y2) > 20 :
                        cv2.line(frame_new,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.circle(frame_new,(x1,y1),2,(0,0,255),-1)
                    cv2.circle(frame_new,(x2,y2),2,(0,0,255),-1)
                    cv2.putText(frame_new,'{0} {1}'.format(x1,y1),(x1,y1),font,0.7,(255,255,255),1,cv2.LINE_AA)
                    cv2.putText(frame_new,'{0} {1}'.format(x2,y2),(x2,y2),font,0.7,(255,255,255),1,cv2.LINE_AA)
                    line_len = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
                    line_av = (line_len + line_av) /2
                    
                    xAv = (x1 + x2 + xAv)/3
                    yAv = (y1 + y2 + yAv)/3
                    #if x1<x2 and y1<y2:
                    #  print(' {} {} {} {}'.format(x1,x2,y1,y2)) 
                        #newIm = frame_new[x1:x2,y1:y2]
                        #cv2.imshow("somethi ng{}.jpg".format(x1),newIm)
                        #cv2.imshow("last frame",final_image)
                if no_of_lines > 3:
                    break 
            
            #cv2.putText(frame_new,'GPS X / Y OVERLAY : XXXX   YYYY'.format(line_av),(40,40),font,0.6,(255,255,255),2,cv2.LINE_AA)
            cv2.putText(frame_new,'no of lines :{0}'.format(no_of_lines),(40,80),font,0.6,(255,255,255),2,cv2.LINE_AA)
            if line_av < 290:
                cv2.putText(frame_new,'average len : {0}'.format(line_av),(40,100),font,0.6,(255,0,255),2,cv2.LINE_AA)
                cv2.imwrite('foundvar.png',frame_new)
            else:
                cv2.putText(frame_new,'average len : {0}'.format(line_av),(40,100),font,0.6,(255,255,255),2,cv2.LINE_AA)
            #cv2.circle(frame_new,(int(xAv),int(yAv)),3,(0,255,255),-1)
            cv2.imshow("Output Image", frame_new)
     
        # KEY PROMPTS 
        key = cv2.waitKey(1)
        if key == 27 :  
            break
        elif key == 112: 
            #h_low,h_high,s_low,s_high,v_low,v_high = 
            get_HSV_averages(frame_shaped_01)
            
        # elif key == 'm':        #     points = get_sample_points(frame_shaped_01)

    
    cv2.destroyAllWindows




def shape_set(input_frame , new_height , new_width):
    result_frame = input_frame[new_height:og_height,new_width:og_width]
    return result_frame

def get_coordinates(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global xX 
            xX= x 
            global yY 
            yY = y 
            print('x:{} , y:{}'.format(x,y))

            a , b , c = transfer_photo[yY,xX]
            global h_av , s_av , v_av
            h_av = (h_av + a )// 2
            s_av = (s_av + b )// 2
            v_av = (v_av + c )// 2
            

            #Scaling Algorithm 
            T_h = 0.8   #h scaling factor
            T_s = 0.15   #s scaling factor
            T_v = 0.4   #v scaling factor

            global h_l,h_u,s_l,s_u,v_l,v_u
            h_l = int(h_av - T_h * abs(h_av-0))
            h_u = int(h_av + T_h * abs(h_av-180))

            s_l = int(s_av - T_s * abs(s_av-0))
            s_u = int(s_av + T_s * abs(s_av-255))

            v_l = int(v_av - T_v * abs(v_av-80))
            v_u = 250 #int(v_av + T_v * abs(v_av-255))

            global lower_thresh , upper_thresh 
            lower_thresh = np.array([h_l, s_l, v_l])       
            upper_thresh = np.array([h_u, s_u, v_u])

            

            print('h:{} s:{} v:{}'.format(a,b,c))
            print('hAv:{} sAv:{} vAv:{}'.format(h_av,s_av,v_av))
            print('lower h:{} lower s:{} lower v:{}'.format(h_l,s_l,v_l))
            print('lower h:{} lower s:{} lower v:{}'.format(h_u,s_u,v_u))
            
            mask = cv2.inRange(transfer_photo, lower_thresh, upper_thresh)
            cv2.imshow('mask tester', mask)




def get_HSV_averages(input_frame):
    cv2.namedWindow('new_image')
    cv2.setMouseCallback('new_image',get_coordinates)

    while True:
        cv2.imshow('new_image',input_frame)
        
        a = cv2.waitKey(1)
        if a == 112:
            cv2.destroyWindow('new_image')
            cv2.destroyWindow('mask tester')
            break


    
    
    cv2.destroyAllWindows
    #return h_low,h_high,s_low,s_high,v_low,v_high





if __name__ == "__main__":
    main()