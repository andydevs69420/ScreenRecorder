
import numpy as np
import cv2
from tkinter import *
from tkinter import filedialog,simpledialog
from tkinter.messagebox import showerror
import os
import threading
import datetime
import getpass
import mss
import time


user=getpass.getuser()

class Timer:
    def __init__(self,hour,min,sec):
        self.sec=sec
        self.min=min
        self.hour=hour
        self.running=False
        self.pause_=False

    def start(self,component):
        self.run()

        while self.running:

            self.sec+=1
            time.sleep(1)
            if self.sec>59:
                self.min+=1
                self.sec=0
            if self.min>59:
                self.hour+=1
                self.min=0
            while self.pause_:
                action=None
            component.configure(text=str(self.getTime()),font=["TimesNewRoman",15,"bold"])

    def pause(self):
        self.pause_=True
    def unpause(self):
        self.pause_=False
    def run(self):
        self.running=True
    def stop(self):
        self.running=False
    def reset(self):
        self.sec=0
        self.min=0
        self.hour=0
    def getTime(self):
        strsec=""
        strmin=""
        strhr=""

        if self.sec<10:
            strsec="0"+str(self.sec)
        else:
            strsec=str(self.sec)

        if self.min<10:
            strmin="0"+str(self.min)
        else:
            strmin=str(self.min)

        if self.hour<10:
            strhr="0"+str(self.hour)
        else:
            strhr=str(self.hour)
        time_final=strhr+" : "+strmin+" : "+strsec


        return time_final

class Recorder:
    def __init__(self,geometry):
       # timer=Timer(0,0,0)
        self.recording=False
        self.pause_=False
        self.dimension=geometry
        self.location=None

    def rec(self):
        self.recording=True
    def stop(self):
        self.recording=False
        self.pause_=False
    def pause(self):
        self.pause_=True
    def unpause(self):
        self.pause_=False
    def setLoc(self,location):
        self.location=location
    def run(self,filename):

        previous_time = 0
        self.sct=mss.mss()
        self.rec()
        forruc=cv2.VideoWriter_fourcc(*"XVID")
        mp4=0x7634706d
        out=cv2.VideoWriter(self.location+"Rec_"+str(datetime.date.today())+"_"+filename+".mp4",mp4,16.1,(self.dimension[0],self.dimension[1]))
        monitor={'left':0,'top':0,'width':self.dimension[0],'height':self.dimension[1]}
        while self.recording:

            img=self.sct.grab(monitor)
            img=np.array(img)
            img = np.flip(img[:, :, :3], 2)  # 1
            frame=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            out.write(frame)
            while self.pause_:
                action=None

        out.release()

        cv2.destroyAllWindows()
    def isRecording(self):
        return self.recording
    def isPaused(self):
        return self.pause_
def fileExist(path,file):
    vid=os.listdir(path)
    if file in vid:
        return True
    else:
        return False


def screenRecorder(root):
    recorder=Recorder([root.winfo_screenwidth(),root.winfo_screenheight()])
    timer=Timer(0,0,0)


    def askdist():
        file=filedialog.askdirectory(title="Select folder")
        if file is not None:
            text.delete(0,END)
            text.insert(0,str(file)+"/")
        else:
             showerror("error","Invalid directory!")

    def record():
        if recorder.isRecording() is True:
            recorder.stop()
            button_rec.configure(text="l",fg="red",font=["wingdings",15,"bold"])
            timer.reset()
            label_time.configure(text=str(timer.getTime()),font=["TimesNewRoman",15,"bold"])
            timer.stop()

        else:

            file=str(text.get())
            file=os.path.isdir(file)
            if file is True:
                filename=None
                while filename is None or filename is "":
                    filename=simpledialog.askstring("Window","Enter file name.")
                file_="Rec_"+str(datetime.date.today())+"_"+filename+".mp4"
                path=text.get()
                if fileExist(path,file_):
                    simpledialog.messagebox.showerror("window",str(file_)+" already exist!")
                else:
                    recorder.setLoc(text.get())
                    recorder.rec()
                    recording=threading.Thread(target=recorder.run,name="t1",args=(filename,))
                    recording.start()
                    timer_=threading.Thread(target=timer.start,name="t1",args=(label_time,))
                    timer_.start()
                    button_rec.configure(text="n",fg="red",font=["wingdings",15,"bold"])

    def pause():
        if recorder.isRecording() is True:
            if recorder.isPaused() is True:
                recorder.unpause()
                timer.unpause()
                button_pause.configure(font=["TimesNewRoman",15,"bold"],text="||")#change to pause

            elif recorder.isPaused() is False:
                time.sleep(1)
                recorder.pause()
                timer.pause()
                button_pause.configure(font=["webdings",15,"bold"],text="4")#change to play
    #Frame
    root.title("PyRecorder by: Philipp Redondo")
    root.resizable(0,0)
    root.geometry("{0}x{1}".format(400,100))
    frame=Frame(root,bg="Gray19")
    frame.place(relx=0.0,rely=0.0,relwidth=1.0,relheight=1.0)

    label=Label(frame,text="Location:",font=["TimesNewRoman",10,"bold"],bg="gray19",fg="white")
    label.place(relx=-0.070,rely=0.020,relwidth=0.300,relheight=0.300)

    text=Entry(frame,bg="gray19",fg="white")
    text.place(relx=0.160,rely=0.070,relwidth=0.650,relheight=0.200)


    file=os.path.exists("C:/Users/"+user+"/Documents/PyScreenRecorder_Video")
    if file is not True:
        os.makedirs("C:/Users/"+user+"/Documents/PyScreenRecorder_Video",mode=1)
    text.insert(0,"C:/Users/"+user+"/Documents/PyScreenRecorder_Video/")

    label_time=Label(frame,text=str(timer.getTime()),bg="gray19",fg="white",font=["TimesNewRoman",15,"bold"])
    label_time.place(relx=0.500,rely=0.460,relwidth=0.300,relheight=0.340)

    button=Button(frame,text="1",font=["wingdings",12,"bold"],fg="white",bg="gray19",highlightthickness=1,command=askdist)
    button.place(relx=0.830,rely=0.070,relwidth=0.090,relheight=0.200)

    button_rec=Button(frame,bg="gray19",text="l",fg="red",font=["wingdings",15,"bold"],command=record)
    button_rec.place(relx=0.200,rely=0.460,relwidth=0.100,relheight=0.340)

    button_pause=Button(frame,bg="gray19",text="||",fg="red",font=["TimesNewRoman",15,"bold"],command=pause)
    button_pause.place(relx=0.330,rely=0.460,relwidth=0.100,relheight=0.340)









app=Tk()
screenRecorder(app)
app.mainloop()
