import shutil
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(os.getcwd()))+"/YOTO"

def FinalDelete():
    try:
        shutil.rmtree(f"{PROJECT_PATH}/Input/BackGroundSet")
    except:
        None

    try:
        VideoList = os.listdir(f"{PROJECT_PATH}/Input/Videos")
        for video in VideoList:
            os.remove(f"{PROJECT_PATH}/Input/Videos/{video}")
    except:
        None

    try:
        InputImagesList = os.listdir(f"{PROJECT_PATH}/Input/Images")
        for image in InputImagesList:
            shutil.rmtree(f"{PROJECT_PATH}/Input/Images/{image}")
    except:
        None
    
    try:
        ObjectImagesList = os.listdir(f"{PROJECT_PATH}/ObjectImage")
        for image in ObjectImagesList:
            shutil.rmtree(f"{PROJECT_PATH}/ObjectImage/{image}")
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