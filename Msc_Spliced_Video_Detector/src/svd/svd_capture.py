'''
Created on 4 Jul 2019

@author: Niall
'''
from __future__ import print_function
import os
import cv2

#Some of this code is taken and modified from
#https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html

#This class deals with capturing and saving of video
class Capture():
    def __init__(self):
        self.capturing = False
        self.c = cv2.VideoCapture(0)
        
    #starts capture
    def startCapture(self):
        self.capturing = True
        vid_cod = cv2.VideoWriter_fourcc(*'XVID')
        output = cv2.VideoWriter("cam_video.mp4", vid_cod, 20.0, (640,480))
        
        while self.capturing == True:
            # Capture each frame of webcam video
            ret,frame = self.c.read()
            cv2.imshow("My cam video", frame)
            output.write(frame)
            # Close and break the loop after pressing "x" key
            if cv2.waitKey(1) &0XFF == ord('x'):
                break
        self.capturing = False
        output.release()
        cv2.destroyAllWindows()
    #ends capture
    def endCapture(self):
        self.capturing = False
        cv2.destroyAllWindows()
        
#property called upon for video file name
class P:

    def __init__(self,x):
        self.__x = x

    def get_x(self):
        return self.__x

    def set_x(self, x):
        self.__x = x