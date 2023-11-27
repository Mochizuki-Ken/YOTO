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
from Tool.Labeling import LABELING
import copy
Input_Path = "./Input"
ObjectImage = "./ObjectImage"
ProcessedImage = "./ProcessedImage"
Output = "./Output"
PROJECT_PATH = os.path.dirname(os.path.abspath(os.getcwd()))+"/YOTO"



class YOTO:
    First_Column_X = 20
    Second_Column_X = 300
    Third_Column_X = 800
    Forth_Column_X = 1150

    TARGET_OBJECTS_LIST = []
    TARGET_OBJECTS_LABEL = []

    INTERFERENCE_OBJECTS_LIST = []
    INTERFERENCE_OBJECTS_LABEL = [] # {Top:int,Left:int,Bottom:int,Right:int,Label:bool}

    OBJECTS_OPTION_DETAILS_LIST = []

    OPTION_LIST = {"object-accuracy":"","position-accuracy":"","light-accuracy":"","size-accuracy":""}
    BACKGROUND_OPTION_LIST = {"background":"AI","background-light":"NORMAL"}

    ObjectType = ["Human","Animals","Frult","Building","Sign/Logo","Human Position","Cell","Other"]

    Main = None

    Background_Type_Str_Var = None
    Background_light_Str_Var = None
    Terminal_Text_Str_Var = None
    InterferenceObjects_Type_Str_Var = None
    Auto_Interference_Hepler_State_Str_Var = None
    Currect_Object_Str_Var = None
    Objects_Zip_Mode_Str_Var = None

    Current_Target_Object_Index = 0
    Current_Target_Object_Change_State = True

    ##### Element display State Var #####

    Add_Interference_Entry = None
    Add_Interference_Btn = None

    ##### GUI Element #####
    Add_Target_Objects_Entry = None
    Add_Interference_Entry = None
    Add_Interference_Btn = None
    Auto_Interference_Hepler_Text = None
    Auto_Interference_Hepler_Btn = None
    AI_InterferenceObject_Text = None
    AI_InterferenceObject_Btn = None
    Default_Interference_Datas_Text = None
    Default_Interference_Datas_Btn = None

    ##### Labeling Var #####
    drawing = False 
    ix,iy = -1,-1
    FRAMES = []
    Size={}
    New_Frame = None

    ##### Functions #####

    ##### on Change #####
    def OnInputChange(self,_1,_2,_3):
        if(self.Current_Target_Object_Change_State):
            try:
                self.Save_Current_Option()
            except:
                None


    def Save_Current_Option(self):

        ObjectAccuracy = int(self.OPTION_LIST["object-accuracy"].get())
        PostitionAccuracy = int(self.OPTION_LIST["position-accuracy"].get())
        LightAccuracy = int(self.OPTION_LIST["light-accuracy"].get())
        SizeAccuracy = int(self.OPTION_LIST["size-accuracy"].get())
        BackgroundMode = str(self.Background_Type_Str_Var.get())
        BackgroundLight = str(self.Background_light_Str_Var.get())
        InterferenceObjects_Mode = str(self.InterferenceObjects_Type_Str_Var.get())
        Auto_Interference_Hepler = str(self.Auto_Interference_Hepler_State_Str_Var.get())
        Option_Detail = {
            "object-accuracy":ObjectAccuracy,
            "position-accuracy":PostitionAccuracy,
            "light-accuracy":LightAccuracy,
            "size-accuracy":SizeAccuracy,
            "Interference-mode":InterferenceObjects_Mode,
            "Interference-helper":Auto_Interference_Hepler,
            "Background-mode":BackgroundMode,
            "Background-light":BackgroundLight
        }

        if(self.Current_Target_Object_Index == len(self.OBJECTS_OPTION_DETAILS_LIST)):
            self.OBJECTS_OPTION_DETAILS_LIST.append(Option_Detail)
        else:
            self.OBJECTS_OPTION_DETAILS_LIST[self.Current_Target_Object_Index] = Option_Detail

        self.Current_Target_Object_Change_State = True

        print(self.Current_Target_Object_Index)
        print(self.OBJECTS_OPTION_DETAILS_LIST)

        return

    ##### Button Functions #####

    def DataSet_Size_Mode(self):
        if(self.Objects_Zip_Mode_Str_Var.get() == "Auto"):
            self.Objects_Zip_Mode_Str_Var.set("Zip")
        elif(self.Objects_Zip_Mode_Str_Var.get() ==  'Zip'):
            self.Objects_Zip_Mode_Str_Var.set("No Zip")
        else:
            self.Objects_Zip_Mode_Str_Var.set("Auto")
    def Add_Custom_Background(self):
        FolderPath = filedialog.askdirectory()
        # os.mkdir(PROJECT_PATH+f"/Input/BackGroundSets/{self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]}")
        try:
            shutil.copytree(FolderPath,PROJECT_PATH+f"/Input/BackGroundSets/{self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]}")
            self.Background_Type_Str_Var.set(FolderPath)
            self.Save_Current_Option()
        except:
            try:
                shutil.copytree(FolderPath,PROJECT_PATH+f"/Input/BackGroundSets/{self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index-1][0]}")
                self.Background_Type_Str_Var.set(FolderPath)
                self.Save_Current_Option()
            except:
                self.Terminal_Text_Str_Var.set("Pls Selete/Add a Object First")
       

    def Auto_Interference_Hepler_Mode(self):
        if(self.Auto_Interference_Hepler_State_Str_Var.get() == "None"):
            self.Auto_Interference_Hepler_State_Str_Var.set("Active")
        else:
            self.Auto_Interference_Hepler_State_Str_Var.set("None")
        self.Save_Current_Option()

    def DeleteInterferenceElement(self):
        if(self.Add_Interference_Btn!=None):self.Add_Interference_Btn.destroy()
        if(self.Add_Interference_Entry!=None):self.Add_Interference_Entry.destroy()
        if(self.Auto_Interference_Hepler_Text!=None):self.Auto_Interference_Hepler_Text.destroy()
        if(self.Auto_Interference_Hepler_Btn!=None):self.Auto_Interference_Hepler_Btn.destroy()
        if(self.Default_Interference_Datas_Text!=None):self.Default_Interference_Datas_Text.destroy()
        if(self.Default_Interference_Datas_Btn!=None):self.Default_Interference_Datas_Btn.destroy()

    def Interference_Mode(self,mode="Change"):

        self.DeleteInterferenceElement()

        if(self.InterferenceObjects_Type_Str_Var.get()=="Auto"):

            if(mode=="Change"):
                self.InterferenceObjects_Type_Str_Var.set("Custom")
                self.Add_Interference_Entry = tk.Entry(self.Main,width=16,font=("Arial", 15) )
                self.Add_Interference_Entry.pack()
                self.Add_Interference_Entry.place(x=self.Second_Column_X,y=180)

                self.Add_Interference_Btn = tk.Button(self.Main,text="+",width=13,font=("Arial", 16) ,command=self.Add_Custom_Interference_Object)
                self.Add_Interference_Btn.pack()
                self.Add_Interference_Btn.place(x=self.Second_Column_X,y=210)

                self.Auto_Interference_Hepler_Text = tk.Label(self.Main,text="Interference Hepler",font=("Arial", 15))
                self.Auto_Interference_Hepler_Text.pack()
                self.Auto_Interference_Hepler_Text.place(x=self.Second_Column_X+205,y=140)

                self.Auto_Interference_Hepler_Btn = tk.Button(self.Main,textvariable=self.Auto_Interference_Hepler_State_Str_Var,width=8,font=("Arial", 15) ,command=self.Auto_Interference_Hepler_Mode)
                self.Auto_Interference_Hepler_Btn.pack()
                self.Auto_Interference_Hepler_Btn.place(x=self.Second_Column_X+215,y=170)

                self.Default_Interference_Datas_Text = tk.Label(self.Main,text="Default Objects",font=("Arial", 15))
                self.Default_Interference_Datas_Text.pack()
                self.Default_Interference_Datas_Text.place(x=self.Second_Column_X+205,y=210)

                self.Default_Interference_Datas_Btn = tk.Button(self.Main,text="+",width=8,font=("Arial", 15) ,command=self.Add_Default_Interference_Object)
                self.Default_Interference_Datas_Btn.pack()
                self.Default_Interference_Datas_Btn.place(x=self.Second_Column_X+215,y=240)
            else:
                self.DeleteInterferenceElement()

        elif(self.InterferenceObjects_Type_Str_Var.get()=="Custom"):
            if(mode=="Change"):
                self.InterferenceObjects_Type_Str_Var.set("None")
                self.DeleteInterferenceElement()
            else:
                self.DeleteInterferenceElement()
                self.InterferenceObjects_Type_Str_Var.set("Custom")
                self.Add_Interference_Entry = tk.Entry(self.Main,width=16,font=("Arial", 15) )
                self.Add_Interference_Entry.pack()
                self.Add_Interference_Entry.place(x=self.Second_Column_X,y=180)

                self.Add_Interference_Btn = tk.Button(self.Main,text="+",width=13,font=("Arial", 16) ,command=self.Add_Custom_Interference_Object)
                self.Add_Interference_Btn.pack()
                self.Add_Interference_Btn.place(x=self.Second_Column_X,y=210)

                self.Auto_Interference_Hepler_Text = tk.Label(self.Main,text="Interference Hepler",font=("Arial", 15))
                self.Auto_Interference_Hepler_Text.pack()
                self.Auto_Interference_Hepler_Text.place(x=self.Second_Column_X+220,y=140)

                self.Auto_Interference_Hepler_Btn = tk.Button(self.Main,textvariable=self.Auto_Interference_Hepler_State_Str_Var,width=8,font=("Arial", 15) ,command=self.Auto_Interference_Hepler_Mode)
                self.Auto_Interference_Hepler_Btn.pack()
                self.Auto_Interference_Hepler_Btn.place(x=self.Second_Column_X+230,y=170)

                self.Default_Interference_Datas_Text = tk.Label(self.Main,text="Default Objects",font=("Arial", 15))
                self.Default_Interference_Datas_Text.pack()
                self.Default_Interference_Datas_Text.place(x=self.Second_Column_X+220,y=210)

                self.Default_Interference_Datas_Btn = tk.Button(self.Main,text="+",width=8,font=("Arial", 15) ,command=self.Add_Default_Interference_Object)
                self.Default_Interference_Datas_Btn.pack()
                self.Default_Interference_Datas_Btn.place(x=self.Second_Column_X+230,y=240)
        else:
            if(mode=="Change"):self.InterferenceObjects_Type_Str_Var.set("Auto")
            else:
                self.DeleteInterferenceElement()

        if(mode!="Change"):self.Save_Current_Option()

        return

    def SetBackGroundType(self):
        self.Background_Type_Str_Var.set("Auto")

        self.Save_Current_Option()
            
    def SetBackGroundLight(self):
        if(self.Background_light_Str_Var.get()=="NORMAL"):
            self.Background_light_Str_Var.set("LIGHT")
        elif(self.Background_light_Str_Var.get()=="LIGHT"):
            self.Background_light_Str_Var.set("DARK")
        else:
            self.Background_light_Str_Var.set("NORMAL")
        self.Save_Current_Option()

    ##### Setting Functions #####

    def Setting(self):
        Setting_Page = tk.Toplevel(self.Main)
        Setting_Page.geometry("500x300")
        Setting_Page.title("Setting")

        Setting = tk.Label(Setting_Page,text="Setting",height=2,font=("Arial", 20))
        Setting.pack()

        Setting_Yaml_Path_Text = tk.Label(Setting_Page,text="Yaml Path",font=("Arial", 15))
        Setting_Yaml_Path_Text.pack()

        Setting_Yaml_Path_Btn = tk.Entry(Setting_Page)
        Setting_Yaml_Path_Btn.pack()

        Setting_Yolov5_Path_Text = tk.Label(Setting_Page,text="Yolov5 Path",font=("Arial", 15))
        Setting_Yolov5_Path_Text.pack()

        Setting_Yolov5_Path_Btn = tk.Entry(Setting_Page)
        Setting_Yolov5_Path_Btn.pack()

        Setting_Save_Btn = tk.Button(Setting_Page,text="Save",font=("Arial", 15))
        Setting_Save_Btn.pack()
        

    ##### Train Functions #####

    def TrainModel(self,mode="GenDataSet"):
        NEW_TARGETS_LIST = []
        for i in self.TARGET_OBJECTS_LIST:
            NEW_TARGETS_LIST.append(i[0])
            print(i[0])
        NEW_INTERFERENCE_OBJECTS_LIST = []
        for i in self.INTERFERENCE_OBJECTS_LIST:
            arr = []
            for j in i:
                arr.append(j[0])
            NEW_INTERFERENCE_OBJECTS_LIST.append(arr)
        print("------------------------")
        print("TARGET_OBJECTS_LIST")
        print(NEW_TARGETS_LIST)
        print("TARGET_OBJECTS_LABEL")
        print(self.TARGET_OBJECTS_LABEL)
        print("INTERFERENCE_OBJECTS_LIST")
        print(self.INTERFERENCE_OBJECTS_LIST)
        print("INTERFERENCE_OBJECTS_LABEL")
        print(self.INTERFERENCE_OBJECTS_LABEL)
        print("OBJECTS_OPTION_DETAILS_LIST")
        print(self.OBJECTS_OPTION_DETAILS_LIST)
        # background= self.Background_Type_Str_Var.get()
        # backgroundLight=self.Background_light_Str_Var.get()
        # t=threading.Thread(target=Train,args=(NEW_TARGETS_LIST,self.TARGET_OBJECTS_LABEL,int(self.OPTION_LIST["postition-accuracy"].get()),int(self.OPTION_LIST["light-accuracy"].get()),int(self.OPTION_LIST["size-accuracy"].get()),background,backgroundLight,self.Terminal_Text_Str_Var,mode))
        # t.start()

    def TrainSetup(self):

        def StartTrain():
            self.TrainModel("Train")

        Option = ["epochs","img","batch","workers","Other"]

        TrainWindow = tk.Toplevel(self.Main)
        TrainWindow.geometry("500x300")
        TrainWindow.title("Train Data")

        Training_Option_text = tk.Label(TrainWindow,text="Training Option",font=("Arial", 18))
        Training_Option_text.pack()
        Training_Option_text.place(x=180,y=20)

        for i,e in enumerate(Option):
            Training_Option_Text = tk.Label(TrainWindow,text=e,font=("Arial", 17))
            Training_Option_Text.pack()
            Training_Option_Text.place(x=90,y=80+(i*30))

            Training_Option_Entry = tk.Entry(TrainWindow,width=20,font=("Arial", 15))
            Training_Option_Entry.pack()
            Training_Option_Entry.place(x=270,y=80+(i*30))

        Train_Btn=tk.Button(TrainWindow,text="TRAIN",width=15,font=("Arial", 17), command=StartTrain)
        Train_Btn.pack()
        Train_Btn.place(x=170,y=260)

    ##### Labeling Functions #####

    def Start_Labeling(self,index,name,video,type):
        Postition_Accuracy = int(self.OPTION_LIST["position-accuracy"].get())
        try:
            Postition_Accuracy = self.OBJECTS_OPTION_DETAILS_LIST[self.Current_Target_Object_Index]["position"]
        except:
            None

        Labeling = LABELING(index=index,name=name,video=video,Postiton_Accuracy=Postition_Accuracy)
        FRAMES_SIZES_LIST = Labeling.Label_Object()
        del Labeling
        # print(FRAMES_SIZES_LIST)

        if (type == "Target"):
            if(index=="ADD"):
                self.TARGET_OBJECTS_LABEL.append(FRAMES_SIZES_LIST)
            else:
                self.TARGET_OBJECTS_LABEL[index]=FRAMES_SIZES_LIST
        elif (type == "Interference"):
            if(len(self.INTERFERENCE_OBJECTS_LABEL[self.Current_Target_Object_Index])-1>=index):

                self.INTERFERENCE_OBJECTS_LABEL[self.Current_Target_Object_Index][index]=FRAMES_SIZES_LIST
            else:
                try:
                    self.INTERFERENCE_OBJECTS_LABEL[self.Current_Target_Object_Index].append(FRAMES_SIZES_LIST)
                except:
                    self.INTERFERENCE_OBJECTS_LABEL.append([FRAMES_SIZES_LIST])

        print("TARGET_OBJECTS_LABEL")
        print(self.TARGET_OBJECTS_LABEL)

        print("INTERFERENCE_OBJECTS_LABEL")
        print(self.INTERFERENCE_OBJECTS_LABEL)
        
        return
    
    ##### Display Page Element #####

    def TARGET_OBJECTS_DISPLAY(self):
        print(self.TARGET_OBJECTS_LIST)
        
        i=0
        for j in self.TARGET_OBJECTS_LIST:
            print("TARGET OBJECT DISPLAY")
            Object_Name = j[0]
            index = i

            def Delete_Object(indexCopy,Object_Name_Copy):
                self.Delete_Target_Object(Object_Name_Copy,indexCopy)

            def Label_Object(indexCopy,Object_Name_Copy):
                self.Start_Labeling(indexCopy,Object_Name_Copy,PROJECT_PATH+"/Input/Target_Objects_Videos/"+Object_Name+".mp4","Target")

            def Update_Current_Target_Object(indexCopy):
                if(indexCopy == self.Current_Target_Object_Index):return
                print(indexCopy)
                self.Current_Target_Object_Change_State = False
                self.Current_Target_Object_Index = indexCopy
                self.Currect_Object_Str_Var.set(str(self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]))

                self.Background_Type_Str_Var.set(self.OBJECTS_OPTION_DETAILS_LIST[indexCopy]["Background-mode"])
                self.Background_light_Str_Var.set(self.OBJECTS_OPTION_DETAILS_LIST[indexCopy]["Background-light"])
                self.InterferenceObjects_Type_Str_Var.set(self.OBJECTS_OPTION_DETAILS_LIST[indexCopy]["Interference-mode"])
                self.Auto_Interference_Hepler_State_Str_Var.set(self.OBJECTS_OPTION_DETAILS_LIST[indexCopy]["Interference-helper"])
                self.OPTION_LIST["object-accuracy"].set(str(self.OBJECTS_OPTION_DETAILS_LIST[indexCopy]["object-accuracy"]))
                self.OPTION_LIST["position-accuracy"].set(str(self.OBJECTS_OPTION_DETAILS_LIST[indexCopy]["position-accuracy"]))
                self.OPTION_LIST["light-accuracy"].set(self.OBJECTS_OPTION_DETAILS_LIST[indexCopy]["light-accuracy"])
                self.OPTION_LIST["size-accuracy"].set(self.OBJECTS_OPTION_DETAILS_LIST[indexCopy]["size-accuracy"])

                print(self.Current_Target_Object_Index)
                self.INTERFERENCE_OBJECTS_DISPLAY(mode="display")
                self.Interference_Mode(mode="display")
                self.Current_Target_Object_Change_State = True

            btn=tk.Button(self.Main,text=str(Object_Name),width=10,font=("Arial", 15), command=lambda indexCopy=index : Update_Current_Target_Object(indexCopy) )
            btn.pack()
            btn.place(x=self.First_Column_X,y=(210+(30*i)))

            btn2=tk.Button(self.Main,text="Label",width=2,font=("Arial", 12) ,command=lambda indexCopy=index,Object_Name_Copy=Object_Name : Label_Object(indexCopy,Object_Name_Copy) )
            btn2.pack()
            btn2.place(x=self.First_Column_X+130,y=(210+(30*i)))

            btn3=tk.Button(self.Main,text="Delete",width=2,font=("Arial", 12) ,command=lambda indexCopy=index,Object_Name_Copy=Object_Name : Delete_Object(indexCopy,Object_Name_Copy) )
            btn3.pack()
            btn3.place(x=self.First_Column_X+180,y=(210+(30*i)))

            self.TARGET_OBJECTS_LIST[i][1]=[btn,btn2,btn3]
            i+=1

            print(self.TARGET_OBJECTS_LIST)
    
    def KILL_OTHER_INTERFERENCE_OBJECTS(self):
        for i,e in enumerate(self.INTERFERENCE_OBJECTS_LIST):
            if(i!=self.Current_Target_Object_Index):
                for i2,e2 in enumerate(e):
                    print(e2)
                    e2[1][0].destroy()
                    e2[1][1].destroy()
                    e2[1][2].destroy()

    def INTERFERENCE_OBJECTS_DISPLAY(self,mode="change"):
        if(mode=="display"):self.KILL_OTHER_INTERFERENCE_OBJECTS()
        print("INTERFERENCE_OBJECTS_LIST")
        print(self.INTERFERENCE_OBJECTS_LIST)
        i=0

        print("index",self.Current_Target_Object_Index)
        for j in self.INTERFERENCE_OBJECTS_LIST[self.Current_Target_Object_Index]:

            Object_Name = j[0]
            index = i

            def Delete_Object(indexCopy,Object_Name_Copy):
                self.Delete_Interference_Object(Object_Name_Copy,indexCopy)

            def Label_Object(indexCopy,Object_Name_Copy):
                self.Start_Labeling(indexCopy,Object_Name_Copy,PROJECT_PATH+f"/Input/Interference_Objects_Videos/{self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]}/"+Object_Name+".mp4","Interference")

            btn=tk.Button(self.Main,text=str(Object_Name),width=10,font=("Arial", 15) )
            btn.pack()
            btn.place(x=self.Second_Column_X-20,y=(250+(30*i)))

            btn2=tk.Button(self.Main,text="Label",width=2,font=("Arial", 12) ,command=lambda indexCopy=index,Object_Name_Copy = Object_Name : Label_Object(indexCopy,Object_Name_Copy) )
            btn2.pack()
            btn2.place(x=self.Second_Column_X+110,y=(250+(30*i)))

            btn3=tk.Button(self.Main,text="Delete",width=2,font=("Arial", 12) ,command=lambda indexCopy=index,Object_Name_Copy = Object_Name : Delete_Object(indexCopy,Object_Name_Copy) )
            btn3.pack()
            btn3.place(x=self.Second_Column_X+160,y=(250+(30*i)))

            self.INTERFERENCE_OBJECTS_LIST[self.Current_Target_Object_Index][i][1]=[btn,btn2,btn3]
            i+=1

            print(self.INTERFERENCE_OBJECTS_LIST)
            print(self.INTERFERENCE_OBJECTS_LABEL)

    ##### Update Page/Objects Functions #####

    def Add_Target_Object(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (
                                                ('MPEG-4 movie', '*.mp4'),
                                                ('All files', '*.*')))
        print(filename)
        shutil.copyfile(filename, PROJECT_PATH+"/Input/Target_Objects_Videos/"+self.Add_Target_Objects_Entry.get()+".mp4")
        FileList:list = os.listdir(f"{PROJECT_PATH}/Input/Target_Objects_Videos")
        self.TARGET_OBJECTS_LIST=[]
        for File in FileList:
            self.TARGET_OBJECTS_LIST.append([File[:len(File)-4],[]])

        self.INTERFERENCE_OBJECTS_LIST.append([])
        self.INTERFERENCE_OBJECTS_LABEL.append([])

        self.TARGET_OBJECTS_DISPLAY()#FileList[-1][:len(FileList[-1])-4]
        self.Start_Labeling("ADD",self.Add_Target_Objects_Entry.get(),PROJECT_PATH+"/Input/Target_Objects_Videos/"+self.Add_Target_Objects_Entry.get()+".mp4","Target")
        
        try:
            self.Currect_Object_Str_Var.set(str(self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]))
        except:
            self.Currect_Object_Str_Var.set("Next")
        self.Current_Target_Object_Index+=1
        self.Currect_Object_Str_Var.set("Next")
        

        if(self.Current_Target_Object_Index>=1):
            
            self.OBJECTS_OPTION_DETAILS_LIST.append(self.OBJECTS_OPTION_DETAILS_LIST[len(self.OBJECTS_OPTION_DETAILS_LIST)-1])
        print("TARGET_OBJECTS_LIST")
        print(self.TARGET_OBJECTS_LIST)

        

    def Delete_Target_Object(self,Object_file,index):
        print("DEL OBJECT FILE",Object_file,"index",index)
        try : 
            os.remove(PROJECT_PATH+"/Input/Target_Objects_Videos/"+Object_file+".mp4")
        except:None
        try:
            shutil.rmtree(PROJECT_PATH+f"/Input/BackGroundSets/{Object_file}")
        except:
            None
        FileList:list = os.listdir(f"{PROJECT_PATH}/Input/Target_Objects_Videos")
        print("FileLIST")
        print(FileList)
        if(len(self.TARGET_OBJECTS_LIST)==1):
            print(self.TARGET_OBJECTS_LIST[0][1][0].destroy())
            self.TARGET_OBJECTS_LIST[0][1][0].destroy()
            self.TARGET_OBJECTS_LIST[0][1][1].destroy()
            self.TARGET_OBJECTS_LIST[0][1][2].destroy()
            for widget in self.Main.winfo_children():
                widget.destroy()
            self.GUI()
        else:
            for i,j in enumerate(self.TARGET_OBJECTS_LIST):
                print("DEL INSIDE",self.TARGET_OBJECTS_LIST[i][0])
                self.TARGET_OBJECTS_LIST[i][1][0].destroy()
                self.TARGET_OBJECTS_LIST[i][1][1].destroy()
                self.TARGET_OBJECTS_LIST[i][1][2].destroy()
        self.TARGET_OBJECTS_LIST=[]
        for File in FileList:
            self.TARGET_OBJECTS_LIST.append([File[:len(File)-4],[]])
        try:
            self.TARGET_OBJECTS_LABEL.pop(index)
        except:
            None
        print("TARGET_OBJECTS_LABEL")
        print(self.TARGET_OBJECTS_LABEL)
        try:
            self.INTERFERENCE_OBJECTS_LIST.pop(index)
        except:
            None
        try:
            self.INTERFERENCE_OBJECTS_LABEL.pop(index)
        except:
            None
        try:
            self.OBJECTS_OPTION_DETAILS_LIST.pop(index)
        except:
            None

        print("*",self.TARGET_OBJECTS_LIST)
        if(self.Current_Target_Object_Index>=len(self.TARGET_OBJECTS_LIST)):
            if(len(self.TARGET_OBJECTS_LIST)==0):
                self.Current_Target_Object_Index = 0
                try:
                    self.Currect_Object_Str_Var.set(str(self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]))
                except:
                    self.Currect_Object_Str_Var.set("Next")
            else:
                self.Current_Target_Object_Index = len(self.TARGET_OBJECTS_LIST)-1
                try:
                    self.Currect_Object_Str_Var.set(str(self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]))
                except:
                    self.Currect_Object_Str_Var.set("Next")

        if len(self.TARGET_OBJECTS_LIST)>0:self.TARGET_OBJECTS_DISPLAY()

    def Add_Custom_Interference_Object(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (
                                                ('MPEG-4 movie', '*.mp4'),
                                                ('All files', '*.*')))
        
        OBJECT_NAME = self.Add_Interference_Entry.get()
        print(filename)
        if(self.Current_Target_Object_Index>=len(self.TARGET_OBJECTS_LIST)):
            self.Current_Target_Object_Index = len(self.TARGET_OBJECTS_LIST) - 1
            try:
                self.Currect_Object_Str_Var.set(str(self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]))
            except:
                self.Currect_Object_Str_Var.set("Next")
        try:
            os.mkdir(PROJECT_PATH+f"/Input/Interference_Objects_Videos/{self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]}/")
        except:
            None
        shutil.copyfile(filename, PROJECT_PATH+f"/Input/Interference_Objects_Videos/{self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]}/"+OBJECT_NAME+".mp4")
        FileList:list = os.listdir(f"{PROJECT_PATH}/Input/Interference_Objects_Videos/{self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]}")
        self.INTERFERENCE_OBJECTS_LIST[self.Current_Target_Object_Index]=[]
        for File in FileList:
            try:
                self.INTERFERENCE_OBJECTS_LIST[self.Current_Target_Object_Index].append([File[:len(File)-4],[]])
            except:
                self.INTERFERENCE_OBJECTS_LIST.append([[File[:len(File)-4],[]]])
            # try:
            #     self.INTERFERENCE_OBJECTS_LABEL.append([])
            # except:
            #     self.INTERFERENCE_OBJECTS_LABEL.append([])
        self.INTERFERENCE_OBJECTS_DISPLAY()
        self.Start_Labeling(len(FileList),OBJECT_NAME,PROJECT_PATH+f"/Input/Interference_Objects_Videos/{self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]}/"+OBJECT_NAME+".mp4","Interference")

    def Add_Default_Interference_Object(self):
        Window = tk.Toplevel(self.Main)
        Window.geometry("500x300")
        Window.title("Default Interference Objects")

        Default_Interference_Objects_Code_Text = tk.Label(Window,height=2,text="Interference Objects Code",font=("Arial", 15))
        Default_Interference_Objects_Code_Text.pack()

        Default_Interference_Objects_Code_Entry = tk.Entry(Window,width=25,font=("Arial", 15))
        Default_Interference_Objects_Code_Entry.pack()

        Default_Interference_Objects_Btn = tk.Button(Window,text="Choose",width=16,font=("Arial", 15))
        Default_Interference_Objects_Btn.pack()




    def Delete_Interference_Object(self,Object_file,index):
        try : 
            os.remove(PROJECT_PATH+f"/Input/Interference_Objects_Videos/{self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]}/"+Object_file+".mp4")
        except:pass
        print("INdex")
        print(self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0])
        print("IO LIST")
        print(self.INTERFERENCE_OBJECTS_LIST)
        FileList:list = os.listdir(f"{PROJECT_PATH}/Input/Interference_Objects_Videos/{self.TARGET_OBJECTS_LIST[self.Current_Target_Object_Index][0]}")
        for i,j in enumerate(self.INTERFERENCE_OBJECTS_LIST[self.Current_Target_Object_Index]):
            self.INTERFERENCE_OBJECTS_LIST[self.Current_Target_Object_Index][i][1][0].destroy()
            self.INTERFERENCE_OBJECTS_LIST[self.Current_Target_Object_Index][i][1][1].destroy()
            self.INTERFERENCE_OBJECTS_LIST[self.Current_Target_Object_Index][i][1][2].destroy()
        try:
            self.INTERFERENCE_OBJECTS_LIST[self.Current_Target_Object_Index].pop(index)
        except:
            None
        try:
            self.INTERFERENCE_OBJECTS_LABEL[self.Current_Target_Object_Index].pop(index)
        except:
            None
        print("*",self.INTERFERENCE_OBJECTS_LIST)
        if(len(self.INTERFERENCE_OBJECTS_LIST[self.Current_Target_Object_Index]) > 0):self.INTERFERENCE_OBJECTS_DISPLAY()

    

    def GUI (self):
        #######GUI element#######

        TITLE = tk.Label(self.Main,text="YOTO",font=("Arial", 30) ,padx=550,pady=20)
        TITLE.pack()

        



        Currect_Object_Text = tk.Label(self.Main,textvariable=self.Currect_Object_Str_Var,font=("Arial", 20) )
        Currect_Object_Text.pack()
        Currect_Object_Text.place(x=self.First_Column_X,y=20)

        Setting_Btn = tk.Button(self.Main,text="Setting",font=("Arial", 15),command=self.Setting)
        Setting_Btn.pack()
        Setting_Btn.place(x=1250,y=20)

        Target_Objects_Title = tk.Label(self.Main,text="TARGET OBJECTS",font=("Arial", 20) )
        Target_Objects_Title.pack()
        Target_Objects_Title.place(x=self.First_Column_X,y=100)

        self.Add_Target_Objects_Entry = tk.Entry(self.Main,width=16,font=("Arial", 15) )
        self.Add_Target_Objects_Entry.pack()
        self.Add_Target_Objects_Entry.place(x=self.First_Column_X,y=140)

        Add_Target_Objects_Btn = tk.Button(self.Main,text="+",width=13,font=("Arial", 15) ,command=self.Add_Target_Object)
        Add_Target_Objects_Btn.pack()
        Add_Target_Objects_Btn.place(x=self.First_Column_X,y=170)

        Interference_Title = tk.Label(self.Main,text="INTERFERENCE OBJECTS",font=("Arial", 20) )
        Interference_Title.pack()
        Interference_Title.place(x=self.Second_Column_X,y=100)

        Interference_Btn = tk.Button(self.Main,textvariable=self.InterferenceObjects_Type_Str_Var,width=12,font=("Arial", 15) ,command=self.Interference_Mode)
        Interference_Btn.pack()
        Interference_Btn.place(x=self.Second_Column_X,y=140)

        Option_Title = tk.Label(self.Main,text="OBJECT OPTION",font=("Arial", 20) )
        Option_Title.pack()
        Option_Title.place(x=self.Third_Column_X,y=100)

        for i,j in enumerate(self.OPTION_LIST.keys()):
            Option_Text = tk.Label(self.Main,text=j,font=("Arial", 20) )
            Option_Text.pack()
            Option_Text.place(x=self.Third_Column_X-110,y=140+(i*30))

            Option_Entry = tk.Entry(self.Main,font=("Arial", 15) ,width=5,textvariable=self.OPTION_LIST[j])
            Option_Entry.pack()
            Option_Entry.place(x=self.Third_Column_X+60,y=140+(i*30))

            # self.OPTION_LIST[j]=Option_Entry
            # self.OPTION_LIST[j]=

            Option_Text = tk.Label(self.Main,text="(1-100)",font=("Arial", 12),fg="gray" )
            Option_Text.pack()
            Option_Text.place(x=self.Third_Column_X+140,y=140+(i*30))

        DataSet_Option_Title = tk.Label(self.Main,text="DATASET OPTION",font=("Arial", 20) )
        DataSet_Option_Title.pack()
        DataSet_Option_Title.place(x=self.Third_Column_X,y=300)
        
        DataSet_Size_Mode_Text = tk.Label(self.Main,text="dataset size",font=("Arial", 20))
        DataSet_Size_Mode_Text.pack()
        DataSet_Size_Mode_Text.place(x=self.Third_Column_X-20,y=340)

        DataSet_Size_Mode_Btn = tk.Button(self.Main,textvariable=self.Objects_Zip_Mode_Str_Var,font=("Arial", 15),command=self.DataSet_Size_Mode)
        DataSet_Size_Mode_Btn.pack()
        DataSet_Size_Mode_Btn.place(x=self.Third_Column_X+100,y=340)

        ##### BackGround Option #####

        Background_Title = tk.Label(self.Main,text="BACKGROUND",font=("Arial", 20) )
        Background_Title.pack()
        Background_Title.place(x=self.Forth_Column_X,y=100)

        for i,j in enumerate(self.BACKGROUND_OPTION_LIST.keys()):
    
            Option_Text = tk.Label(self.Main,text=j,font=("Arial", 20) )
            Option_Text.pack()
            Option_Text.place(x=self.Forth_Column_X-70,y=140+(i*30))

            if(j=="background"): Option_Entry = tk.Button(self.Main,textvariable=self.Background_Type_Str_Var,font=("Arial", 15) ,width=5,command=self.SetBackGroundType)#if(j=="background")
            else:Option_Entry = tk.Button(self.Main,textvariable=self.Background_light_Str_Var,font=("Arial", 15) ,width=5,command=self.SetBackGroundLight)
            Option_Entry.pack()
            Option_Entry.place(x=self.Forth_Column_X+110,y=140+(i*30))


        Default_Background_Title = tk.Label(self.Main,text="DAULT BACKGROUND",font=("Arial", 20) )
        Default_Background_Title.pack()
        Default_Background_Title.place(x=self.Forth_Column_X-30,y=250)

        Add_Default_Background_Entry = tk.Entry(self.Main,width=16,font=("Arial", 15) ,command=None)
        Add_Default_Background_Entry.pack()
        Add_Default_Background_Entry.place(x=self.Forth_Column_X-30,y=290)

        Add_Default_Background_Btn = tk.Button(self.Main,text="Search",width=3,font=("Arial", 15) ,command=None)
        Add_Default_Background_Btn.pack()
        Add_Default_Background_Btn.place(x=self.Forth_Column_X+130,y=290)

        Custom_Background_Title = tk.Label(self.Main,text="CUSTOM BACKGROUND",font=("Arial", 20) )
        Custom_Background_Title.pack()
        Custom_Background_Title.place(x=self.Forth_Column_X-40,y=340)

        Add_Custom_Background_Btn = tk.Button(self.Main,text="Choose Floder",width=16,font=("Arial", 15) ,command=self.Add_Custom_Background)
        Add_Custom_Background_Btn.pack()
        Add_Custom_Background_Btn.place(x=self.Forth_Column_X-10,y=380)



        Train_Btn=tk.Button(self.Main,text="GEN DATASET",width=15,font=("Arial", 18), command=self.TrainModel)
        Train_Btn.pack()
        Train_Btn.place(x=480,y=650)

        Train_Btn=tk.Button(self.Main,text="TRAIN",width=15,font=("Arial", 18), command=self.TrainSetup)
        Train_Btn.pack()
        Train_Btn.place(x=730,y=650)

        Terminal = tk.Label(self.Main,textvariable=self.Terminal_Text_Str_Var,font=("Arial", 20) )
        Terminal.pack()
        Terminal.place(x=190,y=550)

    def __init__(self) -> None:

        ClearAll()

        self.Main = tk.Tk()
        self.Main.title("YOTO")
        self.Main.geometry("1400x700")
        self.Main.resizable(width=None,height=None)

        #######Tkinter String Var#######

        self.OPTION_LIST = {"object-accuracy":tk.StringVar(self.Main),"position-accuracy":tk.StringVar(self.Main),"light-accuracy":tk.StringVar(self.Main),"size-accuracy":tk.StringVar(self.Main)}

        self.Background_Type_Str_Var = tk.StringVar(self.Main,value="Auto")
        self.Background_light_Str_Var = tk.StringVar(self.Main,value="NORMAL")
        self.Terminal_Text_Str_Var = tk.StringVar(self.Main,value="")
        self.InterferenceObjects_Type_Str_Var = tk.StringVar(self.Main,value="Auto")
        self.Auto_Interference_Hepler_State_Str_Var = tk.StringVar(self.Main,value="None")
        self.Currect_Object_Str_Var = tk.StringVar(self.Main,value="Next")
        self.Objects_Zip_Mode_Str_Var = tk.StringVar(self.Main,value="Auto")
        self.OPTION_LIST["object-accuracy"].trace("w",self.OnInputChange)
        self.OPTION_LIST["position-accuracy"].trace("w",self.OnInputChange)
        self.OPTION_LIST["light-accuracy"].trace("w",self.OnInputChange)
        self.OPTION_LIST["size-accuracy"].trace("w",self.OnInputChange)

        self.Background_Type_Str_Var.trace("w",self.OnInputChange)
        self.Background_light_Str_Var.trace("w",self.OnInputChange)
        self.InterferenceObjects_Type_Str_Var.trace("w",self.OnInputChange) 
        self.Auto_Interference_Hepler_State_Str_Var.trace("w",self.OnInputChange) 

        self.GUI()

        self.Main.mainloop()
    
yoto = YOTO()





# def Add_AI_Interference_Object(self):
    #     Window = tk.Toplevel(self.Main)
    #     Window.geometry("800x500")
    #     Window.title("AI Interference Object")

    #     AI_Description_Input = tk.Text(Window,width=800,height=10,font=("Arial", 18))
    #     AI_Description_Input.pack()

    #     AI_Generate_Btn = tk.Button(Window,text="Generate",width=20,font=("Arial", 20))
    #     AI_Generate_Btn.pack()


# self.AI_InterferenceObject_Text = tk.Label(self.Main,text="AI Objects",font=("Arial", 15))
# self.AI_InterferenceObject_Text.pack()
# self.AI_InterferenceObject_Text.place(x=self.Second_Column_X+185,y=210)

# self.AI_InterferenceObject_Btn = tk.Button(self.Main,text="+",width=8,font=("Arial", 15) ,command=self.Add_AI_Interference_Object)
# self.AI_InterferenceObject_Btn.pack()
# self.AI_InterferenceObject_Btn.place(x=self.Second_Column_X+195,y=240)