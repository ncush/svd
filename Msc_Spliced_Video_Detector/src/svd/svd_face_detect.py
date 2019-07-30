'''
Created on 26 Jul 2019

@author: Niall
'''
import numpy as np
import cv2
class FaceDetection():
    #detects face in video
    #Much of the code here was taken and altered from pyimagesearch.com 
    #https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/
    def face_detect(self, args):
        #Loads serialised model
        print("loading serialised model")
        net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")
        #gets the dictionary of frames and assigns it to images variable
        images = args["image"]
        count = 0
        x = {}
        #loops through frames and checks them for faces
        while count + 1 < len(images):
            
            # load the input image and construct an input blob for the image
            # by resizing to a fixed 300x300 pixels and then normalizing it
            image = images[str(count)]
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
               (300, 300), (104.0, 177.0, 123.0))
            
            # pass the blob through the network and obtain the detections and
            # predictions
            print("[INFO] computing object detections...")
            net.setInput(blob)
            detections = net.forward()
            x["face"] = "False"
            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]
            
                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > args["threshold"]:
                    # compute the (x, y)-coordinates for where to crop
                    if args["crop"]:
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                        print(box)
                        
                        #crop image using slicing
                        crop_img = image[startY: endY, startX: endX]
                        
                        #replaces original image with cropped image
                        images[str(count)] = crop_img
                        #adds updated dictionary to return dictionary
                        x["crop"] = images
                    #if a face is found in frame this is updated to true
                    x["face"] = "True"
                    count += 1 
            #if a face wasn't found, and this isn't updated to true
            #it ends the function and returns         
            if x["face"] == "False":
                return x
        #once all the frames have been looped through it returns
        return x               
