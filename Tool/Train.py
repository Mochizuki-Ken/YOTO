from Tool.VideoToImage import VideoToImage
from Tool.RemoveBackGround import RemoveAllImagesBackGround
from Tool.AutoBackGround import AutoBackGround
import os
import shutil
import yaml

Target_ObjectImage_Path = "ObjectImages/Target_Objects"
Interference_ObjectImage_Path = "ObjectImages/Interference_Objects"
PROJECT_PATH = os.path.dirname(os.path.abspath(os.getcwd()))+"/YOTO"

def FinalDelete():
    try:
        shutil.rmtree(f"{PROJECT_PATH}/Input/BackGroundSet")
    except:
        pass
    try:
        VideoList = os.listdir(f"{PROJECT_PATH}/Input/Target_Objects_Videos")
        for video in VideoList:
            os.remove(f"{PROJECT_PATH}/Input/Target_Objects_Videos/{video}")
    except:
        pass

    try:
        TargetInputImagesList = os.listdir(f"{PROJECT_PATH}/Input/Target_Objects_Images")
        for image in TargetInputImagesList:
            shutil.rmtree(f"{PROJECT_PATH}/Input/Target_Objects_Images/{image}")
    except:
        pass
    
    try:
        TargetObjectImagesList = os.listdir(f"{PROJECT_PATH}/{Target_ObjectImage_Path}")
        for image in TargetObjectImagesList:
            shutil.rmtree(f"{PROJECT_PATH}/{Target_ObjectImage_Path}/{image}")
    except:
        pass

    try:
        InterferenceInputImagesList = os.listdir(f"{PROJECT_PATH}/Input/Interference_Objects_Images")
        for image in InterferenceInputImagesList:
            shutil.rmtree(f"{PROJECT_PATH}/Input/Interference_Objects_Images/{image}")
    except:
        pass
    
    try:
        InterferenceObjectImagesList = os.listdir(f"{PROJECT_PATH}/{Interference_ObjectImage_Path}")
        for image in InterferenceObjectImagesList:
            shutil.rmtree(f"{PROJECT_PATH}/{Interference_ObjectImage_Path}/{image}")
    except:
        pass
    
    try:
        TrainImagesTrainList = os.listdir(f"{PROJECT_PATH}/Train/images/train")
        for i in range(1,len(TrainImagesTrainList)+1):
            os.remove(f"{PROJECT_PATH}/Train/images/train/{i}.png")
            os.remove(f"{PROJECT_PATH}/Train/labels/train/{i}.txt")
    except:
        pass

    try:
        TrainLabelsTrainList = os.listdir(f"{PROJECT_PATH}/Train/images/val")
        for i in range(1,len(TrainLabelsTrainList)+1):
            os.remove(f"{PROJECT_PATH}/Train/images/val/{i}.png")
            os.remove(f"{PROJECT_PATH}/Train/labels/val/{i}.txt")
    except:
        pass
    
    


def EditYaml(Target_Objects):
    names = {}
    for i,j in enumerate(Target_Objects):
        names[i]=j
    with open(f'{PROJECT_PATH}/Input/custom.yaml', 'w') as f:
        data = {
            'names':names,
            'test':None,
            'train': f'/content/Train/images/train/',
            'val': f'/content/Train/images/val/',
            # 'train': f'{PROJECT_PATH}/Train/images/train/',
            # 'val': f'{PROJECT_PATH}/Train/images/val/',
            
        }
        yaml.dump(data, f)

def Train(Target_Objects:list,Target_Objects_Area:list[list[dict]],position_accuracy:int,light_accuracy:int,size_accuracy:int,background,background_light,Terminal_Text,mode):
    # FinalDelete()
    EditYaml(Target_Objects=Target_Objects)
    if background!="AI":
        shutil.copytree(background,f"{PROJECT_PATH}/Input/BackGroundSet")

    # BackgroundTrainList:list = os.listdir(f"{PROJECT_PATH}/Input/BackGroundSet/train")
    # for i,j in enumerate(BackgroundTrainList) :
    #     os.rename(f"{PROJECT_PATH}/Input/BackGroundSet/train/{j}", f"{PROJECT_PATH}/Input/BackGroundSet/train/{i}.png")
    
    # BackgroundValList:list = os.listdir(f"{PROJECT_PATH}/Input/BackGroundSet/val")
    # for i,j in enumerate(BackgroundValList) :
    #     os.rename(f"{PROJECT_PATH}/Input/BackGroundSet/val/{j}", f"{PROJECT_PATH}/Input/BackGroundSet/val/{i}.png")

    RATE=101-int(position_accuracy)
    for i,Object in enumerate(Target_Objects):
        VideoToImage(Video_Name=f"{Object}.mp4",RATE=RATE,Size=Target_Objects_Area[i])
        Terminal_Text.set(f"Object[{str(i)}] Video To Image Processing ...")
    RemoveAllImagesBackGround()
    AutoBackGround(ObjectFolderList=Target_Objects,light_accuracy=light_accuracy,size_accuracy=size_accuracy,background_light=background_light,Terminal_Text=Terminal_Text,background=background)

    path_to_dir = f'{PROJECT_PATH}/Train'

    output_filename = f'{PROJECT_PATH}/Output/TrainData'

    shutil.make_archive(output_filename, 'zip', path_to_dir)

    # shutil.make_archive(f'{PROJECT_PATH}/Output/TrainDataZIP', 'zip', f'{PROJECT_PATH}/Train')
    
    shutil.copytree(f"{PROJECT_PATH}/Train",f'{PROJECT_PATH}/Output/TrainData')

    shutil.copyfile( f'{PROJECT_PATH}/Input/custom.yaml',f'{PROJECT_PATH}/Output/custom.yaml')

    FinalDelete()

    Terminal_Text.set(f"DONE!")

    return 0