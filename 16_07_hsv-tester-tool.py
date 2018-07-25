import cv2
import numpy 

#PUT ANY SOURCE VIDEO 
#PRESS p for checking pausing and checking values 


# BASIC SETUP 
font = cv2.FONT_HERSHEY_SIMPLEX
vc = cv2.VideoCapture('test_main_2.mp4')


#DYNAMIC GRADATION
# xX=0 # variable used in averaging 
# yY=0
#defining averages 
h_low = h_high = 90 
s_low = s_high = 110
v_low = v_high = 110


og_width = int(vc.get(3))
og_height = int(vc.get(4))
print('width:{0} \nheight:{1}'.format(og_width,og_height))

transfer_photo = None


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
            print('h:{} s:{} v:{}'.format(a,b,c))



def get_HSV_averages(input_frame):
    cv2.namedWindow('new_image')
    b = cv2.setMouseCallback('new_image',get_coordinates)

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