'''
Created on 2 Jul 2019

@author: Niall
'''

# import the necessary packages
#from scipy.spatial import distance as dist
#from skimage.util import img_as_uint
import matplotlib.pyplot as plt
import numpy as np
#import argparse
#import glob
import cv2
import scenedetect
import configparser

config = configparser.ConfigParser()
#takes in a video file, and creates a dictionary containing frames/images
def frame_lst(vidcap):    
    success, image = vidcap.read()
        # image is an array of array of [R,G,B] values
    lst1 = {}
    count = 0;
    while success:
        success, image = vidcap.read()
        lst1[str(count)] = image
        # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
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

def scene_detection(vidcap):
    scenedetect.ContentDetector()

# ap = argparse.ArgumentParser()
# ap.add_argument("-d", "--dataset", required = True,
#      help = "Path to the directory of images")
# args = vars(ap.parse_args())
#  
# d = glob.glob(args["dataset"])

def get_comparison(lst1):
    count = 0
    lst = []
    sus = False
    config.read("next.ini")
    while count < len(lst1):
        frame1 = count + 1 
        frame2 = count + 2
        if config.get("Histogram Comparison", "custom chi") == "True":
            try:
                sus = False
                x = create_histograms(lst1, frame1, frame2)
                y = compare_histograms_custom_chi(x['images'], x['index'], frame1, frame2, sus)
                print(y)
                if y[0] > float(config.get("Histogram Thresholds", "custom chi")):
                    sus = True
                    print("Suspicious frames detected")
                    lst.append(y)
                    compare_histograms_custom_chi(x['images'], x['index'], frame1, frame2, sus)
                    break
                lst.append(y)
                count += 1
            except:
                print('end')
                break
    return lst

# vidcap = cv2.VideoCapture('b.mp4')
# lst1 = frame_lst(vidcap)
# config = {}
# config["custom_chi"] = True
# config["chi_distance"] = 0.009
# print(get_comparison(lst1, config))
