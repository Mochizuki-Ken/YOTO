import PIL
from PIL import Image
import cv2
import rembg
from rembg import remove as RemoveBackground
import os

Input_Path = "./Input"
ObjectImage = "./ObjectImage"
ProcessedImage = "./ProcessedImage"
Output = "./Output"
Target_ObjectImage_Path = "ObjectImages/Target_Objects"
Interference_ObjectImage_Path = "ObjectImages/Interference_Objects"
PROJECT_PATH = os.path.dirname(os.path.abspath(os.getcwd()))+"/YOTO"

def SaveImages(IMAGE,Folder_Name:str,Id:str,Format:str):
    print(Format)
    # IMAGE.save(f'{PROJECT_PATH}/Test/{Id}.{str(Format).lower()}', str(Format)) #TEST
    IMAGE.save(f'{PROJECT_PATH}/{Target_ObjectImage_Path}/{Folder_Name}/{Id}.{Format.lower()}', 'PNG')
    IMAGE.close()
    return 0

def RemoveImageBackGround(Id:str,Folder_Name:str,File_Name:str):
    # IMAGE = Image.open(f"{PROJECT_PATH}/Test/{File_Name}") #TEST

    print(f"{PROJECT_PATH}/Input/Images/{Folder_Name}/{File_Name}")
    # Format=IMAGE.format

    IMAGE = Image.open(f"{PROJECT_PATH}/Input/Target_Objects_Images/{Folder_Name}/{File_Name}")

    IMAGE=RemoveBackground(IMAGE)

    SaveImages(IMAGE=IMAGE,Folder_Name=Folder_Name,Id=Id,Format="PNG")#str(Format)

    return 0

def RemoveAllImagesBackGround():
    FolderList:list = os.listdir(f"{PROJECT_PATH}/Input/Target_Objects_Images/")
    print(FolderList)
    for Folder in FolderList:
        Folder_Path = os.listdir(f"{PROJECT_PATH}/Input/Target_Objects_Images/{Folder}")
        path=os.path.join(PROJECT_PATH+f"/{Target_ObjectImage_Path}/", Folder) 
        os.mkdir(path) 
        Id=1
        for File in Folder_Path:
            RemoveImageBackGround(Id=Id,File_Name=File,Folder_Name=Folder)
            Id+=1


    return 0


# RemoveImageBackGround(Id='1',Folder_Name="",File_Name="dog2.png")

