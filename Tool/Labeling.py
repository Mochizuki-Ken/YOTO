import cv2

class LABELING:

    drawing = False 
    ix,iy = -1,-1
    FRAMES_SIZES_LIST = []
    Size={}
    New_Frame = None

    index = None 
    name = None
    video = None
    Postiton_Accuracy = None

    def Label_Object_Each_Object(self,name,frame):
        self.drawing = False
        self.ix,self.iy = -1,-1
        self.end = False
        self.New_Frame = frame.copy()
        self.Size={}


        def draw_rectanlge(event, x, y, flags, param):
            """ Draw rectangle on mouse click and drag """
            if event == cv2.EVENT_LBUTTONDOWN:
                self.New_Frame = frame.copy()
                self.drawing = True
                self.ix,self.iy = x,y
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing == True:
                    cv2.rectangle(self.New_Frame, (self.ix, self.iy), (x, y), (250,250, 250,0.2), -1)
            elif event == cv2.EVENT_LBUTTONUP:
                print(self.ix,self.iy,x,y)
                self.Size={"Top":self.iy,"Left":self.ix,"Bottom":y,"Right":x}
                self.drawing = False

        cv2.namedWindow(name) 
        cv2.setMouseCallback(name,draw_rectanlge)
        cv2.imshow(name,self.New_Frame)

        while(self.end==False):
            cv2.imshow(name,self.New_Frame)
            if cv2.waitKey(1) & 0xFF == ord('e'):
                self.FRAMES_SIZES_LIST.append(self.Size)
                self.New_Frame=None
                break      
                
        cv2.destroyAllWindows()

        return 1

    def Label_Object(self) :
        c=1

        Video = cv2.VideoCapture(self.video)

        RATE = 101-self.Postiton_Accuracy

        while Video.isOpened() :
            ret , frame = Video.read()
            if ret == True and c%RATE==0:
                self.Label_Object_Each_Object(name=f'{self.name}{c}',frame=frame)
            elif ret!=True:
                break
            c+=1

        Video.release()
        
        return self.FRAMES_SIZES_LIST
    
    def __init__(self,index,name,video,Postiton_Accuracy):
        self.drawing = False
        self.ix,self.iy = -1,-1
        self.FRAMES_SIZES_LIST = []
        self.Size={}
        self.New_Frame = None

        self.index = index
        self.name = name
        self.video = video
        self.Postiton_Accuracy = Postiton_Accuracy
