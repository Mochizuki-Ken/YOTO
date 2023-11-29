import shutil
import os

Target_ObjectImage_Path = "ObjectImages/Target_Classes"
Interference_ObjectImage_Path = "ObjectImages/Interference_Objects"
PROJECT_PATH = os.path.dirname(os.path.abspath(os.getcwd()))+"/YOTO"

def FinalDelete():
    try:
        shutil.rmtree(f"{PROJECT_PATH}/Input/BackGroundSet")
    except:
        None

    try:
        TargetVideoList = os.listdir(f"{PROJECT_PATH}/Input/Target_Classes_Videos")
        for video in TargetVideoList:
            shutil.rmtree(f"{PROJECT_PATH}/Input/Target_Classes_Videos/{video}")
    except:
        None

    try:
        InterferenceVideoList = os.listdir(f"{PROJECT_PATH}/Input/Interference_Objects_Videos")
        for video in InterferenceVideoList:
            shutil.rmtree(f"{PROJECT_PATH}/Input/Interference_Objects_Videos/{video}")
    except:
        None

    try:
        TargetInputImagesList = os.listdir(f"{PROJECT_PATH}/Input/Target_Classes_Images")
        for image in TargetInputImagesList:
            shutil.rmtree(f"{PROJECT_PATH}/Input/Target_Classes_Images/{image}")
    except:
        None
    
    try:
        TargetObjectImagesList = os.listdir(f"{PROJECT_PATH}/{Target_ObjectImage_Path}")
        for image in TargetObjectImagesList:
            shutil.rmtree(f"{PROJECT_PATH}/{Target_ObjectImage_Path}/{image}")
    except:
        None

    try:
        InterferenceInputImagesList = os.listdir(f"{PROJECT_PATH}/Input/Interference_Objects_Images")
        for image in InterferenceInputImagesList:
            shutil.rmtree(f"{PROJECT_PATH}/Input/Interference_Objects_Images/{image}")
    except:
        None
    
    try:
        InterferenceObjectImagesList = os.listdir(f"{PROJECT_PATH}/{Interference_ObjectImage_Path}")
        for image in InterferenceObjectImagesList:
            shutil.rmtree(f"{PROJECT_PATH}/{Interference_ObjectImage_Path}/{image}")
    except:
        None
    
    try:
        TrainImagesTrainList = os.listdir(f"{PROJECT_PATH}/Train/images/train")
        for i in range(1,len(TrainImagesTrainList)+1):
            os.remove(f"{PROJECT_PATH}/Train/images/train/{i}.png")
            os.remove(f"{PROJECT_PATH}/Train/labels/train/{i}.txt")
    except:
        None

    try:
        TrainLabelsTrainList = os.listdir(f"{PROJECT_PATH}/Train/images/val")
        for i in range(1,len(TrainLabelsTrainList)+1):
            os.remove(f"{PROJECT_PATH}/Train/images/val/{i}.png")
            os.remove(f"{PROJECT_PATH}/Train/labels/val/{i}.txt")
    except:
        None
    
    
def Delete():
    try:
        os.remove(f"{PROJECT_PATH}/Output/TrainData.zip")
    except:
        None
    
    try:
        os.remove(f"{PROJECT_PATH}/Output/custom.yaml")
    except:
        None

    try:
        shutil.rmtree(f"{PROJECT_PATH}/Output/TrainData")
    except:
        None
    
    
    




def ClearAll():
    FinalDelete()
    Delete()