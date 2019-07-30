'''
Created on 26 Jul 2019

@author: Niall
'''
import numpy as np
import cv2
class FaceDetection():
    #detects face in 
    def face_detect(self, args):
        #Loads serialised model
        net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")
        images = args["image"]
        count = 0
        x = {}
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
                    # compute the (x, y)-coordinates of the bounding box for the
                    # object
                    if args["crop"]:
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                        print(box)
                        
                        
                        crop_img = image[startY: endY, startX: endX]
                        #cv2.imshow("cropped", crop_img)
                        #cv2.waitKey(0)
                        images[str(count)] = crop_img
                        x["crop"] = images
                    x["face"] = "True"
                    count += 1 
            if not x["face"]:
                return x
        return True               
