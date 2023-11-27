import PIL
from PIL import Image
import cv2
# import rembg
import os
import random
import numpy as np

Input_Path="./Input"
ObjectImage_Path="./ObjectImage"
ProcessedImage_Path="./ProcessedImage"
Output_Path="./Output"
Target_ObjectImage_Path = "ObjectImages/Target_Objects"
Interference_ObjectImage_Path = "ObjectImages/Interference_Objects"
PROJECT_PATH = os.path.dirname(os.path.abspath(os.getcwd()))+"/YOTO"
#################################

ObjectFolders = []



# def GetObjectFoldersList():

#     return 0

# def GetObjectFiles(Folder_Path):

#     return 0

count = 1

# def GetBackGround(,light_accuracy):

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

def NewBackGround_Light(TYPE,image,light_accuracy,background_light,LABEL_POSITION,Terminal_Text,Terminal_Content):
    # Image.
    global count
    BackGround = ""

    Standard = 1.0

    Brighter = 1.0
    Dacker = 1.0


    for i in range(int(light_accuracy/10)):

        IMAGE_COPY = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)

        

        if(i%2 == 0):

            Terminal_Text.set(f"Adjusting Brighter Gamma of {Terminal_Content}")

            NEW_IMAGE = adjust_gamma(IMAGE_COPY,Brighter)

            Brighter = float(Brighter) + float((light_accuracy/10)/10) + float((light_accuracy/10)/10)   + float((light_accuracy/10)/10)  + float((light_accuracy/10)/10) 

            if(i==0):Dacker = float(Dacker) - float((light_accuracy/10)/10) 
        else:

            Terminal_Text.set(f"Adjusting Dacker Gamma of {Terminal_Content}")

            NEW_IMAGE = adjust_gamma(IMAGE_COPY,Dacker)

            Dacker = float(Dacker) - float((light_accuracy/10)/10) - float((light_accuracy/10)/10) #- float((light_accuracy/10)/10)


        NEW_IMAGE = Image.fromarray(cv2.cvtColor(NEW_IMAGE,cv2.COLOR_RGB2BGR))

        NEW_IMAGE.save(f"{PROJECT_PATH}/Train/images/{TYPE}/{count}.png")

        NEW_IMAGE.close()

        with open(f'{PROJECT_PATH}/Train/labels/{TYPE}/{count}.txt', 'w') as f:
            f.write(LABEL_POSITION)

        count+=1

    


    return BackGround
    

def NewBackGround_Size(TYPE,ObjectID,File_Path,light_accuracy,size_accuracy,background_light,Terminal_Text,background):

    global count

    BackGroundFolderPath=f"{PROJECT_PATH}/Input/BackGroundSet"

    BackGroundFolder:list = os.listdir(f"{BackGroundFolderPath}/{TYPE}")

    if(background=="AI"):
        
        if (background_light=="NORMAL"):
            BackGroundFolderPath=f"{PROJECT_PATH}/DefaultData/BackGroundImage"
            BackGroundFolder:list = os.listdir(f"{BackGroundFolderPath}/{TYPE}")
        elif (background_light=="LIGHT"):
            BackGroundFolderPath=f"{PROJECT_PATH}/DefaultData/BrightBackGroundImage"
            BackGroundFolder:list = os.listdir(f"{BackGroundFolderPath}/{TYPE}")
        else:
            BackGroundFolderPath=f"{PROJECT_PATH}/DefaultData/DarkBackGroundImage"
            BackGroundFolder:list = os.listdir(f"{BackGroundFolderPath}/{TYPE}")
        

    print(BackGroundFolder)

    for BackGround in BackGroundFolder:
        if(BackGround==".DS_Store"):continue
        print(BackGround)
        Terminal_Text.set(f"Processing BackGround [ {BackGround} ]")

        BackGroundImage = Image.open(f"{BackGroundFolderPath}/{TYPE}/{BackGround}")
        TargetObjectImage =  Image.open(File_Path)

        BASE = "W"

        BGwidth, BGheight = BackGroundImage.size

        if(BackGroundImage.size[0]>BackGroundImage.size[1]): 
            largerSize = BackGroundImage.size[1]
            smallerSize = BackGroundImage.size[1]
            WH_Percentage = TargetObjectImage.size[0]/TargetObjectImage.size[1]
            BASE = "H"
        else:
            largerSize = BackGroundImage.size[0]
            smallerSize = BackGroundImage.size[0]
            WH_Percentage = TargetObjectImage.size[1]/TargetObjectImage.size[0]
            BASE = "W"

        First_Size = largerSize

        # if(TargetObjectImage.size[0]>TargetObjectImage.size[1]): 

        for size in range(int(size_accuracy/10)+1):
            if(size==0):
                largerSize = int(largerSize / 4)
                smallerSize = int(smallerSize / 4)
                First_Size = largerSize
                if(BASE=="W"):
                    image = TargetObjectImage.copy()
                    image = image.resize((largerSize,int(largerSize*WH_Percentage)),Image.BICUBIC)
                    
                else:
                    image = TargetObjectImage.copy()
                    image = image.resize((int(largerSize*WH_Percentage),largerSize),Image.BICUBIC)
                    
                
            else:
                if(int(size_accuracy/10)<=3): 
                    BASE = 2.2
                elif(int(size_accuracy/10)<=4): 
                    BASE = 1.75
                elif(int(size_accuracy/10)<=7):
                    BASE = 1.45
                else :
                    BASE = 1.15
                largerSize = int(largerSize *(1+(float(((size_accuracy/10))/11)*0.25)))
                smallerSize = int(smallerSize *((float(((size_accuracy/10))/11)*BASE)))#*1.15

                # if (First_Size/smallerSize) > 5:
                #     smallerSize

                if(size%2==0):
                    if(BASE=="W"):
                        image = TargetObjectImage.copy()
                        image = image.resize((largerSize,int(largerSize*WH_Percentage)),Image.BICUBIC)
                        
                    else:
                        image = TargetObjectImage.copy()
                        image = image.resize((int(largerSize*WH_Percentage),largerSize),Image.BICUBIC)
                    print(f"Larger {First_Size/largerSize} Times")

                    
                    Terminal_Text.set(f"Processing {ObjectID} Type {TYPE} BackGround [ {BackGround} ] Larger  Size [ {size} ] {First_Size/largerSize} Times")
                else:
                    if(BASE=="W"):
                        image = TargetObjectImage.copy()
                        image = image.resize((smallerSize,int(smallerSize*WH_Percentage)),Image.BICUBIC)
                        
                    else:
                        image = TargetObjectImage.copy()
                        image = image.resize((int(smallerSize*WH_Percentage),smallerSize),Image.BICUBIC)
                    print(f"Smaller {First_Size/smallerSize} Times")
                    # Terminal_Text.set(f"Smaller {First_Size/smallerSize} Times")
                    Terminal_Text.set(f"Processing {ObjectID} Type {TYPE} BackGround [ {BackGround} ] Smaller  Size [ {size} ] {First_Size/smallerSize} Times")

            XMaxRange = BGwidth-image.size[0]
            YMaxRange = BGheight-image.size[1]

            if(XMaxRange<0):
                XMaxRange=10
            if(YMaxRange<0):
                YMaxRange=10

            # print(largerSize,smallerSize)

            # print("XY",XMaxRange,YMaxRange)

            X=random.randint(0,XMaxRange)
            Y=random.randint(0,YMaxRange)

            BackGroundImageCopy = Image.new("RGBA",BackGroundImage.size)
            BackGroundImageCopy.paste(BackGroundImage,(0,0))
            _, _, _, mask = image.split()
            BackGroundImageCopy.paste(image,(X,Y),mask=mask)

            
            
            # BackGroundImageCopy.save(f"{PROJECT_PATH}/Train/images/{TYPE}/{count}.png")

            w,h=image.size

            Center_X:float = float((X+float(w/2))/BGwidth)
            Center_Y:float = float((Y+float(h/2))/BGheight)

            w=float(w/BGwidth)
            h=float(h/BGheight)

            LABEL_POSITION = f'{ObjectID}  {Center_X}  {Center_Y}  {w}  {h}'

            Terminal_Content = f"{ObjectID} Type {TYPE} BackGround [ {BackGround} ] "
            
            NewBackGround_Light(TYPE=TYPE,image=BackGroundImageCopy,light_accuracy=light_accuracy,background_light=background_light,LABEL_POSITION=LABEL_POSITION,Terminal_Text=Terminal_Text,Terminal_Content=Terminal_Content)
            

            

            # with open(f'{PROJECT_PATH}/Train/labels/{TYPE}/{count}.txt', 'w') as f:
            #     f.write(f'{ObjectID}  {Center_X}  {Center_Y}  {w}  {h}')

            image.close()
            BackGroundImageCopy.close()
            # count+=1
        
        BackGroundImage.close()


        
    return 0

def AutoBackGround(ObjectFolderList,light_accuracy,size_accuracy,background_light,Terminal_Text,background):

    global count

    # ObjectFolderList:list = os.listdir(f"{PROJECT_PATH}/ObjectFolder/")
    for i,ObjectFolder in enumerate(ObjectFolderList):

        FilesList:list = os.listdir(f"{PROJECT_PATH}/{Target_ObjectImage_Path}/{ObjectFolder}")

        for File in FilesList:
            # print(f"{PROJECT_PATH}/ObjectFolder/{ObjectFolder}/{File}")
            NewBackGround_Size(TYPE="train",ObjectID=i,File_Path=f"{PROJECT_PATH}/{Target_ObjectImage_Path}/{ObjectFolder}/{File}",light_accuracy=light_accuracy,size_accuracy=size_accuracy,background_light=background_light,Terminal_Text=Terminal_Text,background=background)
    count=1

    for i,ObjectFolder in enumerate(ObjectFolderList):

        FilesList:list = os.listdir(f"{PROJECT_PATH}/{Target_ObjectImage_Path}/{ObjectFolder}")

        for File in FilesList:
            # print(f"{PROJECT_PATH}/ObjectFolder/{ObjectFolder}/{File}")
            NewBackGround_Size(TYPE="val",ObjectID=i,File_Path=f"{PROJECT_PATH}/{Target_ObjectImage_Path}/{ObjectFolder}/{File}",light_accuracy=light_accuracy,size_accuracy=size_accuracy,background_light=background_light,Terminal_Text=Terminal_Text,background=background)
            

        pass

    return 0

# AutoBackGround(["Apple"],20,20,20)