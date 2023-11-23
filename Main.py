import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import shutil
import cv2
import numpy as np
from Tool.Train import Train
from Tool.Clear import ClearAll
import threading
# from tkinter.filedialog import

TARGET_OBJECTS_LIST = []
TARGET_OBJECTS_LABEL = []
OPTION_LIST = {"train epochs":"","postition accuracy":"","light accuracy":"","size accuracy":""}
BACKGROUND_OPTION_LIST = {"background":"AI","background-light":"NORMAL"}


BACKGROUND="AI"

Input_Path = "./Input"
ObjectImage = "./ObjectImage"
ProcessedImage = "./ProcessedImage"
Output = "./Output"
PROJECT_PATH = os.path.dirname(os.path.abspath(os.getcwd()))+"/YOTO"

Main = tk.Tk()
Main.title("YOTO")
Main.geometry("1100x700")
Main.resizable(width=None,height=None)
backgroundType = tk.StringVar(Main,value="AI")
background_light = tk.StringVar(Main,value="NORMAL")

Terminal_Text = tk.StringVar(Main,value="")

ClearAll()

# def START_Multi_Tasking():
    

def TrainModel():
    global backgroundType,background_light
    NEW_TARGETS_LIST = []
    for i in TARGET_OBJECTS_LIST:
        NEW_TARGETS_LIST.append(i[0])
    # global Train
    background= backgroundType.get()
    backgroundLight=background_light.get()
    # Train(NEW_TARGETS_LIST,TARGET_OBJECTS_LABEL,int(OPTION_LIST["train epochs"].get()),int(OPTION_LIST["postition accuracy"].get()),int(OPTION_LIST["light accuracy"].get()),int(OPTION_LIST["size accuracy"].get()),background=background,background_light=backgroundLight)
    t=threading.Thread(target=Train,args=(NEW_TARGETS_LIST,TARGET_OBJECTS_LABEL,int(OPTION_LIST["train epochs"].get()),int(OPTION_LIST["postition accuracy"].get()),int(OPTION_LIST["light accuracy"].get()),int(OPTION_LIST["size accuracy"].get()),background,backgroundLight,Terminal_Text))
    t.start()
    # t.join()
    


drawing = False # true if mouse is pressed
ix,iy = -1,-1
FRAMES = []
Size={}
New_Frame = None

def Label_Object_Each_Object(index,name,frame):
    global ix,iy,drawing,FRAMES,Size,New_Frame

    drawing = False # true if mouse is pressed
    ix,iy = -1,-1
    end = False
    New_Frame = frame.copy()
    Size={}
    # mouse callback function
    def draw_rectanlge(event, x, y, flags, param):
        """ Draw rectangle on mouse click and drag """
        global ix,iy,drawing,mode,end,Size,New_Frame
        # if the left mouse button was clicked, record the starting and set the drawing flag to True
        if event == cv2.EVENT_LBUTTONDOWN:
            New_Frame = frame.copy()
            drawing = True
            ix,iy = x,y
        # mouse is being moved, draw rectangle
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                # frame = cv2.imread(frame,-1)
                cv2.rectangle(New_Frame, (ix, iy), (x, y), (250,250, 250,0.2), -1)
        # if the left mouse button was released, set the drawing flag to False
        elif event == cv2.EVENT_LBUTTONUP:
            print(ix,iy,x,y)
            Size={"Top":iy,"Left":ix,"Bottom":y,"Right":x}
            # if(len(TARGET_OBJECTS_LABEL)>=index):
            #     TARGET_OBJECTS_LABEL[index]=Size
            # else:
            #     TARGET_OBJECTS_LABEL.append(Size)
            # FRAMES.append(Size)

            drawing = False
            # end=True
            # cv2.destroyWindow(name)


        # create a black image (height=360px, width=512px), a window and bind the function to window
    # f = cv2.VideoCapture(video)
    # rval, frame = f.read()
    # f.release()

    

    cv2.namedWindow(name) 
    cv2.setMouseCallback(name,draw_rectanlge)
    cv2.imshow(name,New_Frame)
    while(end==False):
        cv2.imshow(name,New_Frame)
        
        if cv2.waitKey(1) & 0xFF == ord('e'):
            FRAMES.append(Size)
            New_Frame=None
            break
        # if cv2.waitKey(20) & 0xFF == 27 or end:
        #     break
        # if cv2.getWindowProperty(name, cv2.WND_PROP_VISIBLE) <1:
        #     break
    
    
            
    cv2.destroyAllWindows()

    return 1

def Label_Object(index,name,video):
    global FRAMES

    c=1

    Video = cv2.VideoCapture(video)

    RATE = 101-int(OPTION_LIST["postition accuracy"].get())

    while Video.isOpened() :
        ret , frame = Video.read()
        if ret == True and c%RATE==0:
            Label_Object_Each_Object(index=index,name=f'{name}{c}',frame=frame)
        elif ret!=True:
            break
        c+=1

    if(len(TARGET_OBJECTS_LABEL)>=index):
        TARGET_OBJECTS_LABEL[index]=FRAMES
    else:
        TARGET_OBJECTS_LABEL.append(FRAMES)
    
    Video.release()
    
    print(FRAMES)
    FRAMES=[]
    print(FRAMES)

    return 1




    
    

def Add_Target_Object():
    global TARGET_OBJECTS_LIST
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (
                                              ('MPEG-4 movie', '*.mp4'),
                                              ('All files', '*.*')))
    print(filename)
    shutil.copyfile(filename, PROJECT_PATH+"/Input/Videos/"+Add_Target_Objects_Entry.get()+".mp4")
    FileList:list = os.listdir(f"{PROJECT_PATH}/Input/Videos/")
    TARGET_OBJECTS_LIST=[]
    for File in FileList:
        TARGET_OBJECTS_LIST.append([File[:len(File)-4],[]])

    TARGET_OBJECTS_DISPLAY()#FileList[-1][:len(FileList[-1])-4]
    Label_Object(len(FileList),Add_Target_Objects_Entry.get(),PROJECT_PATH+"/Input/Videos/"+Add_Target_Objects_Entry.get()+".mp4")
    # LabelWindow.mainloop()

    

def Delete_Object(Object_file):
    global TARGET_OBJECTS_LIST
    try : 
        os.remove(PROJECT_PATH+"/Input/Videos/"+Object_file+".mp4")
        FileList:list = os.listdir(f"{PROJECT_PATH}/Input/Videos/")
        for i,j in enumerate(TARGET_OBJECTS_LIST):
            TARGET_OBJECTS_LIST[i][1][0].destroy()
            TARGET_OBJECTS_LIST[i][1][1].destroy()
        TARGET_OBJECTS_LIST=[]
        for File in FileList:
            TARGET_OBJECTS_LIST.append([File[:len(File)-4],[]])
        TARGET_OBJECTS_DISPLAY()
    except:pass
    FileList:list = os.listdir(f"{PROJECT_PATH}/Input/Videos/")
    for i,j in enumerate(TARGET_OBJECTS_LIST):
        TARGET_OBJECTS_LIST[i][1][0].destroy()
        TARGET_OBJECTS_LIST[i][1][1].destroy()
    TARGET_OBJECTS_LIST=[]
    for File in FileList:
        TARGET_OBJECTS_LIST.append([File[:len(File)-4],[]])

    print("*",TARGET_OBJECTS_LIST)
    TARGET_OBJECTS_DISPLAY()


def Add_Custom_Background():
    global BACKGROUND,backgroundType
    foldername = filedialog.askdirectory()
    BACKGROUND=foldername
    backgroundType.set(foldername)
    
    # LabelWindow.mainloop()




TITLE = tk.Label(Main,text="YOTO",font=("Arial", 30) ,padx=550,pady=20)
TITLE.pack()

Target_Objects_Title = tk.Label(Main,text="TARGET OBJECTS",font=("Arial", 20) )
Target_Objects_Title.pack()
Target_Objects_Title.place(x=20,y=100)

Add_Target_Objects_Entry = tk.Entry(Main,width=16,font=("Arial", 15) )
Add_Target_Objects_Entry.pack()
Add_Target_Objects_Entry.place(x=20,y=140)

Add_Target_Objects_Btn = tk.Button(Main,text="+",width=16,font=("Arial", 15) ,command=Add_Target_Object)
Add_Target_Objects_Btn.pack()
Add_Target_Objects_Btn.place(x=20,y=170)

def TARGET_OBJECTS_DISPLAY():
    print(TARGET_OBJECTS_LIST)
    i=0
    for j in TARGET_OBJECTS_LIST:
        def Delete_Object2():
            Delete_Object(j[0])

        btn=tk.Button(Main,text=str(j[0]),width=10,font=("Arial", 15) )
        btn.pack()
        btn.place(x=20,y=(210+(30*i)))

        btn2=tk.Button(Main,text="Delete",width=2,font=("Arial", 12) ,command=Delete_Object2 )
        btn2.pack()
        btn2.place(x=150,y=(210+(30*i)))

        TARGET_OBJECTS_LIST[i][1]=[btn,btn2]
        i+=1

        print(TARGET_OBJECTS_LIST)

TARGET_OBJECTS_DISPLAY()

Option_Title = tk.Label(Main,text="OPTION",font=("Arial", 20) )
Option_Title.pack()
Option_Title.place(x=510,y=100)

for i,j in enumerate(OPTION_LIST.keys()):
    Option_Text = tk.Label(Main,text=j,font=("Arial", 20) )
    Option_Text.pack()
    Option_Text.place(x=400,y=140+(i*30))

    Option_Entry = tk.Entry(Main,font=("Arial", 15) ,width=5)
    Option_Entry.pack()
    Option_Entry.place(x=570,y=140+(i*30))

    OPTION_LIST[j]=Option_Entry

    Option_Text = tk.Label(Main,text="(1-100)",font=("Arial", 12),fg="gray" )
    if(i==0):
        Option_Text = tk.Label(Main,text="",font=("Arial", 12),fg="gray" )
    Option_Text.pack()
    Option_Text.place(x=650,y=140+(i*30))


Background_Title = tk.Label(Main,text="BACKGROUND",font=("Arial", 20) )
Background_Title.pack()
Background_Title.place(x=880,y=100)

def Click1():
        global backgroundType
        backgroundType.set("AI")
        
def Click2():
        global background_light
        
        if(background_light.get()=="NORMAL"):
            background_light.set("LIGHT")
        elif(background_light.get()=="LIGHT"):
            background_light.set("DARK")
        else:
            background_light.set("NORMAL")

for i,j in enumerate(BACKGROUND_OPTION_LIST.keys()):
    

    Option_Text = tk.Label(Main,text=j,font=("Arial", 20) )
    Option_Text.pack()
    Option_Text.place(x=820,y=140+(i*30))

    if(j=="background"): Option_Entry = tk.Button(Main,textvariable=backgroundType,font=("Arial", 15) ,width=5,command=Click1)#if(j=="background")
    else:Option_Entry = tk.Button(Main,textvariable=background_light,font=("Arial", 15) ,width=5,command=Click2)
    Option_Entry.pack()
    Option_Entry.place(x=990,y=140+(i*30))

Custom_Background_Title = tk.Label(Main,text="CUSTOM BACKGROUND",font=("Arial", 20) )
Custom_Background_Title.pack()
Custom_Background_Title.place(x=830,y=250)

Add_Custom_Background_Btn = tk.Button(Main,text="Choose Floder",width=16,font=("Arial", 15) ,command=Add_Custom_Background)
Add_Custom_Background_Btn.pack()
Add_Custom_Background_Btn.place(x=870,y=290)


for i,j in enumerate(TARGET_OBJECTS_LIST):
    Custom_Background_Btn=tk.Button(Main,text=str(j),width=12,font=("Arial", 15) )
    Custom_Background_Btn.pack()
    Custom_Background_Btn.place(x=820,y=(320+(30*i)))

    Open_Custom_Background_Btn=tk.Button(Main,text="Open",width=3,font=("Arial", 12) )
    Open_Custom_Background_Btn.pack()
    Open_Custom_Background_Btn.place(x=965,y=(320+(30*i)))

    Delete_Custom_Background_Btn=tk.Button(Main,text="Delete",width=4,font=("Arial", 12) )
    Delete_Custom_Background_Btn.pack()
    Delete_Custom_Background_Btn.place(x=1020,y=(320+(30*i)))

# def p():
#     print(OPTION_LIST['train epochs'].get())

Train_Btn=tk.Button(Main,text="TRAIN",width=15,font=("Arial", 18), command=TrainModel)
Train_Btn.pack()
Train_Btn.place(x=460,y=650)

Terminal = tk.Label(Main,textvariable=Terminal_Text,font=("Arial", 20) )
Terminal.pack()
Terminal.place(x=190,y=550)



Main.mainloop()