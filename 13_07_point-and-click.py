import cv2
import numpy 


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



og_width = int(vc.get(3))
og_height = int(vc.get(4))
print('width:{0} \nheight:{1}'.format(og_width,og_height))



def main():
    while True:
        _, frame_raw = vc.read()
        
        #SET NEW HEIGHT AND WIDTH
        frame_shaped_01 = shape_set(frame_raw,400,0)    #set height and width

        print(frame_shaped_01.shape)
        cv2.imshow('frame',frame_shaped_01)
        
        global transfer_photo
        transfer_photo= cv2.cvtColor(frame_shaped_01, cv2.COLOR_BGR2HSV)






        # KEY PROMPTS 
        key = cv2.waitKey(1)
        if key == 27 :  
            break
        elif key == 112: 
            #h_low,h_high,s_low,s_high,v_low,v_high = 
            get_HSV_averages(frame_shaped_01)
            
        # elif key == 'm':
        #     points = get_sample_points(frame_shaped_01)

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
            T_h = 0.7   #h scaling factor
            T_s = 0.2   #s scaling factor
            T_v = 0.4   #v scaling factor

            global h_l,h_u,s_l,s_u,v_l,v_u

            h_l = int(h_av - T_h * abs(h_av-0))
            h_u = int(h_av + T_h * abs(h_av-180))

            s_l = int(s_av - T_s * abs(s_av-0))
            s_u = int(s_av + T_s * abs(s_av-255))

            v_l = int(v_av - T_v * abs(v_av-0))
            v_u = int(v_av + T_v * abs(v_av-255))


            print('h:{} s:{} v:{}'.format(a,b,c))
            print('hAv:{} sAv:{} vAv:{}'.format(h_av,s_av,v_av))
            print('lower h:{} lower s:{} lower v:{}'.format(h_l,s_l,v_l))
            print('lower h:{} lower s:{} lower v:{}'.format(h_u,s_u,v_u))



def get_HSV_averages(input_frame):
    cv2.namedWindow('new_image')
    cv2.setMouseCallback('new_image',get_coordinates)

    while True:
        cv2.imshow('new_image',input_frame)
        
        a = cv2.waitKey(1)
        if a == 112:
            cv2.destroyWindow('new_image')
            break


    
    
    cv2.destroyAllWindows
    #return h_low,h_high,s_low,s_high,v_low,v_high





if __name__ == "__main__":
    main()