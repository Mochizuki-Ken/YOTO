# from PIL import Image

# BackGroundImage=Image.open('/Users/mochizukiken/Desktop/Projects/YOTO/Input/BackGroundSet/train/mountains-8379756_1280.png')
# image = Image.open('/Users/mochizukiken/Desktop/Projects/YOTO/ObjectImage/Apple/9.png')
# BackGroundImageCopy = Image.new("RGBA",BackGroundImage.size)

# BackGroundImageCopy.paste(BackGroundImage,(0,0))
# _, _, _, mask = image.split()

# BackGroundImageCopy.paste(image,(0,0),mask=mask)

#             # NewBackGround_Light(Image=BackGroundImageCopy,light_accuracy=light_accuracy,background_light=background_light,X=X,Y=Y)
            
# BackGroundImageCopy.save(f"/Users/mochizukiken/Desktop/Projects/YOTO/Test/a.png")

# BackGroundImage.close()
# BackGroundImageCopy.close()
# image.close()

# import comet_ml

# comet_ml.config.save(api_key="axY1952fz4f3ULxbNWJEKVJg3")

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
    os.remove(f"{PROJECT_PATH}/Output/TrainData.zip")
    os.remove(f"{PROJECT_PATH}/Output/custom.yaml")
    shutil.rmtree(f"{PROJECT_PATH}/Output/TrainData")


FinalDelete()
Delete()