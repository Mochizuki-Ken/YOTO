# def NewBackGround_Size(TYPE,ObjectID,File_Path,light_accuracy,size_accuracy,background_light):

#     global count

#     BackGroundFolder:list = os.listdir(f"{PROJECT_PATH}/Input/BackGroundSet/{TYPE}")
#     print(BackGroundFolder)
#     for BackGround in BackGroundFolder:
#         if(BackGround==".DS_Store"):continue
#         print(BackGround)

#         BackGroundImage = Image.open(f"{PROJECT_PATH}/Input/BackGroundSet/{TYPE}/{BackGround}")
#         TargetObjectImage =  Image.open(File_Path)

#         BASE = "W"

#         BGwidth, BGheight = BackGroundImage.size

#         if(BackGroundImage.size[0]>BackGroundImage.size[1]): 
#             largerSize = BackGroundImage.size[1]
#             smallerSize = BackGroundImage.size[1]
#             WH_Percentage = TargetObjectImage.size[0]/TargetObjectImage.size[1]
#             BASE = "H"
#         else:
#             largerSize = BackGroundImage.size[0]
#             smallerSize = BackGroundImage.size[0]
#             WH_Percentage = TargetObjectImage.size[1]/TargetObjectImage.size[0]
#             BASE = "W"

#         # if(TargetObjectImage.size[0]>TargetObjectImage.size[1]): 

#         for size in range(int(size_accuracy/10)+1):
#             if(size==0):
#                 largerSize = int(largerSize / 4)
#                 smallerSize = int(smallerSize / 4)
#                 if(BASE=="W"):
#                     image = TargetObjectImage.copy()
#                     image = image.resize((largerSize,int(largerSize*WH_Percentage)),Image.BICUBIC)
                    
#                 else:
#                     image = TargetObjectImage.copy()
#                     image = image.resize((int(largerSize*WH_Percentage),largerSize),Image.BICUBIC)
                    
                
#             else:
#                 largerSize = int(largerSize *(1+(float(((size_accuracy/10))/10)*0.15)))
#                 smallerSize = int(smallerSize *((float(((size_accuracy/10))/10)*1.15)))

#                 if(size%2==0):
#                     if(BASE=="W"):
#                         image = TargetObjectImage.copy()
#                         image = image.resize((largerSize,int(largerSize*WH_Percentage)),Image.BICUBIC)
                        
#                     else:
#                         image = TargetObjectImage.copy()
#                         image = image.resize((int(largerSize*WH_Percentage),largerSize),Image.BICUBIC)
#                 else:
#                     if(BASE=="W"):
#                         image = TargetObjectImage.copy()
#                         image = image.resize((smallerSize,int(smallerSize*WH_Percentage)),Image.BICUBIC)
                        
#                     else:
#                         image = TargetObjectImage.copy()
#                         image = image.resize((int(smallerSize*WH_Percentage),smallerSize),Image.BICUBIC)
            
#             XMaxRange = BGwidth-image.size[0]
#             YMaxRange = BGheight-image.size[1]

#             if(XMaxRange<0):
#                 XMaxRange=10
#             if(YMaxRange<0):
#                 YMaxRange=10

#             print(largerSize,smallerSize)

#             print("XY",XMaxRange,YMaxRange)

#             X=random.randint(0,XMaxRange)
#             Y=random.randint(0,YMaxRange)

#             BackGroundImageCopy = Image.new("RGBA",BackGroundImage.size)
#             BackGroundImageCopy.paste(BackGroundImage,(0,0))
#             _, _, _, mask = image.split()
#             BackGroundImageCopy.paste(image,(X,Y),mask=mask)

#             # NewBackGround_Light(Image=BackGroundImageCopy,light_accuracy=light_accuracy,background_light=background_light,X=X,Y=Y)
            
#             BackGroundImageCopy.save(f"{PROJECT_PATH}/Train/images/{TYPE}/{count}.png")

#             w,h=image.size

#             Center_X:float = float((X+float(w/2))/BGwidth)
#             Center_Y:float = float((Y+float(h/2))/BGheight)
            
            

#             w=float(w/BGwidth)
#             h=float(h/BGheight)

#             with open(f'{PROJECT_PATH}/Train/labels/{TYPE}/{count}.txt', 'w') as f:
#                 f.write(f'{ObjectID}  {Center_X}  {Center_Y}  {w}  {h}')

#             image.close()
#             BackGroundImageCopy.close()
#             count+=1
        
#         BackGroundImage.close()


        
#     return 0



# def Label_Object(index,name,video):
#     drawing = False # true if mouse is pressed
#     ix,iy = -1,-1
#     end = False
#     # mouse callback function
#     def draw_rectanlge(event, x, y, flags, param):
#         """ Draw rectangle on mouse click and drag """
#         global ix,iy,drawing,mode,end
#         # if the left mouse button was clicked, record the starting and set the drawing flag to True
#         if event == cv2.EVENT_LBUTTONDOWN:
#             drawing = True
#             ix,iy = x,y
#         # mouse is being moved, draw rectangle
#         elif event == cv2.EVENT_MOUSEMOVE:
#             if drawing == True:
#                 # frame = cv2.imread(frame,-1)
#                 cv2.rectangle(frame, (ix, iy), (x, y), (250,250, 250,0.2), -1)
#         # if the left mouse button was released, set the drawing flag to False
#         elif event == cv2.EVENT_LBUTTONUP:
#             print(ix,iy,x,y)
#             Size:dict={"Top":iy,"Left":ix,"Bottom":y,"Right":x}
#             if(len(TARGET_OBJECTS_LABEL)>=index):
#                 TARGET_OBJECTS_LABEL[index]=Size
#             else:
#                 TARGET_OBJECTS_LABEL.append(Size)
#             drawing = False
#             end=True
#             cv2.destroyWindow(name)


#         # create a black image (height=360px, width=512px), a window and bind the function to window
#     f = cv2.VideoCapture(video)
#     rval, frame = f.read()
#     f.release()
#     cv2.namedWindow(name) 
#     cv2.setMouseCallback(name,draw_rectanlge)
#     cv2.imshow(name,frame)
#     while(end==False):
#         cv2.imshow(name,frame)
        
        
#         if cv2.waitKey(20) & 0xFF == 27 or end:
#             break
#         if cv2.getWindowProperty(name, cv2.WND_PROP_VISIBLE) <1:
#             break
            
#     cv2.destroyAllWindows()

import numpy as np
import cv2
from PIL import Image

i = Image.open("/Users/mochizukiken/Desktop/Projects/YOTO/CustomBackground/train/mountains-8379756_1280.jpg")



def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

i = cv2.cvtColor(np.asarray(i),cv2.COLOR_RGB2BGR)

cv2.imshow("gammam image 1", adjust_gamma(i,4))

cv2.waitKey(0)
cv2.destroyAllWindows()


def Label_Object_Each_Object(self,index,name,frame):
        self.drawing = False # true if mouse is pressed
        self.ix,self.iy = -1,-1
        self.end = False
        self.New_Frame = frame.copy()
        self.Size={}
        # mouse callback function
        def draw_rectanlge(event, x, y, flags, param):
            """ Draw rectangle on mouse click and drag """
            if event == cv2.EVENT_LBUTTONDOWN:
                self.New_Frame = frame.copy()
                self.drawing = True
                self.ix,self.iy = x,y
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing == True:
                    cv2.rectangle(self.New_Frame, (self.ix, self.iy), (x, y), (250,250, 250,0.2), -1)
            elif event == cv2.EVENT_LBUTTONUP:
                print(self.ix,self.iy,x,y)
                self.Size={"Top":self.iy,"Left":self.ix,"Bottom":y,"Right":x}
                self.drawing = False

        cv2.namedWindow(name) 
        cv2.setMouseCallback(name,draw_rectanlge)
        cv2.imshow(name,self.New_Frame)

        while(self.end==False):
            cv2.imshow(name,self.New_Frame)
            if cv2.waitKey(1) & 0xFF == ord('e'):
                self.FRAMES.append(self.Size)
                self.New_Frame=None
                break      
                
        cv2.destroyAllWindows()

        return 1

def Label_Object(self,index,name,video):
        c=1

        Video = cv2.VideoCapture(video)

        RATE = 101-int(self.OPTION_LIST["postition accuracy"].get())

        while Video.isOpened() :
            ret , frame = Video.read()
            if ret == True and c%RATE==0:
                self.Label_Object_Each_Object(index=index,name=f'{name}{c}',frame=frame)
            elif ret!=True:
                break
            c+=1

        if(len(self.TARGET_OBJECTS_LABEL)>=index):
            self.TARGET_OBJECTS_LABEL[index]=self.FRAMES
        else:
            self.TARGET_OBJECTS_LABEL.append(self.FRAMES)
        
        Video.release()
        
        self.FRAMES=[]

        return 1