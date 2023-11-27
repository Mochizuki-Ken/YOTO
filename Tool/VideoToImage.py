import PIL
from PIL import Image
import cv2
import os

Input_Path = "./Input"
ObjectImage = "./ObjectImage"
ProcessedImage = "./ProcessedImage"
Output = "./Output"
PROJECT_PATH = os.path.dirname(os.path.abspath(os.getcwd()))+"/YOTO"

def VideoToImage(Video_Name:str,RATE:int,Size:list[dict] = [{"Top":0,"Left":0,"Bottom":0,"Right":0}]):
    cap = cv2.VideoCapture(f"{PROJECT_PATH}/Input/Target_Objects_Videos/{Video_Name}")
    c=1
    id=1
    
    # Path 
    path=os.path.join(PROJECT_PATH+"/Input/Target_Objects_Images/", Video_Name[:len(Video_Name)-4]) 
    os.mkdir(path) 
    while(cap.isOpened()):
        ret, frame = cap.read() 
        if ret == True and c%RATE == 0: 
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)

            if(Size[id-1]["Bottom"]==0 and Size[id-1]["Right"]==0):
                Size[id-1]["Bottom"]=frame.size[1]
                Size[id-1]["Right"]=frame.size[0]

            frame=frame.crop((Size[id-1]["Left"],Size[id-1]["Top"],Size[id-1]["Right"],Size[id-1]["Bottom"]))
            frame.save(f"{PROJECT_PATH}/Input/Target_Objects_Images/{Video_Name[:len(Video_Name)-4]}/{str(id)}.png")
            frame.close()
            id+=1
        
        elif(ret == False) : break
        c+=1

    cap.release()
    
    return 0

