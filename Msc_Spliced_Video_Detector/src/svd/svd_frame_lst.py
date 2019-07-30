'''
Created on 29 Jul 2019

@author: Niall
'''
import cv2
#Some of this code was taken and modified from
#https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames

class FrameList():
    #takes in a video file, and creates a dictionary containing frames/images
    def frame_lst(self, vidcap):    
        success, image = vidcap.read()
        # image is an array of array of [R,G,B] values
        lst1 = {}
        count = 0;
        while success:
            success, image = vidcap.read()
            lst1[str(count)] = image
            if cv2.waitKey(10) == 27:  # exit if Escape is hit
                break
            count += 1
        return lst1