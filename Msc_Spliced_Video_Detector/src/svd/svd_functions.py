'''
Created on 2 Jul 2019

@author: Niall
'''

# import the necessary packages
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
#import argparse
#import glob
import cv2
import scenedetect
import configparser

config = configparser.ConfigParser()


def detect_face(args):
    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe("C:/Users/Niall/git/Msc_Spliced_Video_Detector/Msc_Spliced_Video_Detector/src/svd/deploy.prototxt.txt", "C:/Users/Niall/git/Msc_Spliced_Video_Detector/Msc_Spliced_Video_Detector/src/svd/res10_300x300_ssd_iter_140000.caffemodel")
    
    # load the input image and construct an input blob for the image
    # by resizing to a fixed 300x300 pixels and then normalizing it
    image = args["image"]
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
       (300, 300), (104.0, 177.0, 123.0))
    
    # pass the blob through the network and obtain the detections and
    # predictions
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()
    
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
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            print(box)
            
            
            crop_img = image[startY: endY, startX: endX]
            #cv2.imshow("cropped", crop_img)
            #cv2.waitKey(0)
            return crop_img





#takes in a video file, and creates a dictionary containing frames/images
def frame_lst(vidcap):    
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
    
#takes in a list of images, creates histograms for images
def create_histograms(lst1, frame1, frame2):
    
    # initialize the index dictionary to store the image name
    # and corresponding histograms and the images dictionary
    # to store the images themselves
    lst = {}
    lst[str(frame1)] = lst1[str(frame1)]
    lst[str(frame2)] = lst1[str(frame2)]
    index = {}
    images = {}
    
    # loop over the image paths
    
    count = (frame1 - 1)
    while count < frame2:
        # extract the image filename (assumed to be unique) and
        # load the image, updating the images dictionary
        #
        count += 1
        filename = str(count)
        image = lst[str(count)]
        try:
            images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except:
            print("no image")
            break
        # extract a 3D RGB color histogram from the image,
        # using 8 bins per channel, normalize, and update
        # the index
        #print('success')
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
            [0, 256, 0, 256, 0, 256])
        
        hist = cv2.normalize(hist, hist).flatten()
        index[filename] = hist
    return {'images':images, 'index': index}

# Uses histograms to calculate image similarity
def chi2_distance(histA, histB, eps=1e-10):
    # compute the chi-squared distance
    d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
        for (a, b) in zip(histA, histB)])

    # return the chi-squared distance
    return d

def compare_histograms_opencv(images, index, frame1, frame2, sus):
    
    OPENCV_METHODS = (
    ("Correlation", cv2.HISTCMP_CORREL),
    ("Chi-Squared", cv2.HISTCMP_CHISQR),
    ("Intersection", cv2.HISTCMP_INTERSECT),
    ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))
     
    # loop over the comparison methods
    for (methodName, method) in OPENCV_METHODS:
        # initialize the results dictionary and the sort
        # direction
        results = {}
        reverse = False
     
        # if we are using the correlation or intersection
        # method, then sort the results in reverse order
        if methodName in ("Correlation", "Intersection"):
            reverse = True
     
        # loop over the index
        for (k, hist) in index.items():
            # compute the distance between the two histograms
            # using the method and update the results dictionary
            d = cv2.compareHist(index[str(frame1)], hist, method)
            results[k] = d
     
        # sort the results
        results = sorted([(v, k) for (k, v) in results.items()], reverse = reverse)
    
        
        # initialize the results figure
    fig = plt.figure("Results: %s" % (methodName))
    fig.suptitle(methodName, fontsize = 20)
        
        # loop over the results
    if sus:
        for (i, (v, k)) in enumerate(results):
                # show the result
            ax = fig.add_subplot(1, len(results), i + 1)
            ax.set_title("%s: %.2f" % (k, v))
            plt.imshow(images[k])
            plt.axis("off")
                
            
        # show the custom method
    if sus:
        plt.show()
    return results[1]

def compare_histograms_scipy(images, index, frame1, frame2, sus):
    
    SCIPY_METHODS = (
        ("Euclidean", dist.euclidean),
        ("Manhattan", dist.cityblock),
        ("Chebysev", dist.chebyshev))
     
    # loop over the comparison methods
    for (methodName, method) in SCIPY_METHODS:
        # initialize the results dictionary and the sort
        # direction
        results = {}
     
        # loop over the index
        for (k, hist) in index.items():
    #         # compute the distance between the two histograms
    #         # using the method and update the results dictionary
            d = method(index[str(frame1)], hist)
            results[k] = d
            
        # sort the results
        results = sorted([(v, k) for (k, v) in results.items()])
    
        
        # initialize the results figure
    fig = plt.figure("Results: %s" % (methodName))
    fig.suptitle(methodName, fontsize = 20)
        
        # loop over the results
    if sus:
        for (i, (v, k)) in enumerate(results):
                # show the result
            ax = fig.add_subplot(1, len(results), i + 1)
            ax.set_title("%s: %.2f" % (k, v))
            plt.imshow(images[k])
            plt.axis("off")
                
            
        # show the custom method
    if sus:
        plt.show()
    return results[1]
    
#takes in histograms, and compares them using chi2_distance, and then sorts and prints results. 
def compare_histograms_custom_chi(images, index, frame1, frame2, sus):
    # initialize the results dictionary
    results = {}
    
    # loop over the index
    
    for (k, hist) in index.items():
        # compute the distance between the two histograms
        # using the custom chi-squared method, then update
        # the results dictionary
        d = chi2_distance(index[str(frame1)], index[str(frame2)])
        results[k] = d
        
    # sort the results
    results = sorted([(v, k) for (k, v) in results.items()])
        
        # initialize the results figure
    fig = plt.figure("Results: Custom Chi-Squared")
    fig.suptitle("Custom Chi-Squared", fontsize=20)
        
        # loop over the results
    if sus:
        for (i, (v, k)) in enumerate(results):
                # show the result
            ax = fig.add_subplot(1, len(results), i + 1)
            ax.set_title("%s: %.2f" % (k, v))
            plt.imshow(images[k])
            plt.axis("off")
                
            
        # show the custom method
    if sus:
        plt.show()
    return results[1]

def get_custom_chi(lst1, frame1, frame2):
    sus = False
    x = create_histograms(lst1, frame1, frame2)
    y = compare_histograms_custom_chi(x['images'], x['index'], frame1, frame2, sus)
    print(y)
    if y[0] > float(config.get("Histogram Thresholds", "custom chi")):
        sus = True
        print("Suspicious frames detected")
        compare_histograms_custom_chi(x['images'], x['index'], frame1, frame2, sus)
    return sus

def get_opencv(lst1, frame1, frame2):
    sus = False
    x = create_histograms(lst1, frame1, frame2)
    y = compare_histograms_opencv(x['images'], x['index'], frame1, frame2, sus)
    print(y)
    if y[0] > float(config.get("Histogram Thresholds", "opencv")):
        sus = True
        print("Suspicious frames detected")
        compare_histograms_opencv(x['images'], x['index'], frame1, frame2, sus)
    return sus

def get_scipy(lst1, frame1, frame2):
    sus = False
    x = create_histograms(lst1, frame1, frame2)
    y = compare_histograms_scipy(x['images'], x['index'], frame1, frame2, sus)
    print(y)
    if y[0] > float(config.get("Histogram Thresholds", "scipy")):
        sus = True
        print("Suspicious frames detected")
        compare_histograms_scipy(x['images'], x['index'], frame1, frame2, sus)
    return sus

    

#Gets histogram comparisons depending on what has been selected in settings.
def get_comparison(lst1):
    count = 0
    config.read("next.ini")
    x = {}
    print(len(lst1))
    if config.get("Histogram Comparison", "custom chi") == "True":
        while count + 2 < len(lst1):
            frame1 = count + 1 
            frame2 = count + 2
            try:
                x["custom_chi"] = get_custom_chi(lst1, frame1, frame2)
            except Exception as e:
                print(e)
                break
            count += 1 
    
    count = 0
    if config.get("Histogram Comparison", "opencv") == "True":
        while count < len(lst1):
            frame1 = count + 1 
            frame2 = count + 2
            try:
                x["opencv"] = get_opencv(lst1, frame1, frame2)   
            except:
                print('end')
                break
            count += 1 
    
        count = 0
        
    if config.get("Histogram Comparison", "scipy") == "True":
        while count < len(lst1):
            frame1 = count + 1 
            frame2 = count + 2
            try:
                x["scipy"] = get_scipy(lst1, frame1, frame2)   
            except:
                print('end')
                break
            count += 1 

    return x

