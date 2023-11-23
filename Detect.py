import torch

model  = torch.hub.load('ultralytics/yolov5','custom',path="/Users/mochizukiken/Desktop/Projects/YOTO/Models/apple2.pt")

imgPATH = "/Users/mochizukiken/Desktop/Projects/YOTO/apple2.png"

model(imgPATH).show()

# python3 detect.py --weight /Users/mochizukiken/Desktop/Projects/YOTO/Models/apple2.pt --img 640 --source 0