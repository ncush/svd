'''
Created on 2 Jul 2019

@author: Niall
'''

# import the necessary packages
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
import cv2
import configparser

config = configparser.ConfigParser()

class HistogramAnalysis():        
    #takes in a list of images, creates histograms for images
    def create_histograms(self, lst1, frame1, frame2):
        
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
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                [0, 256, 0, 256, 0, 256])
            
            hist = cv2.normalize(hist, hist).flatten()
            index[filename] = hist
        return {'images':images, 'index': index}
    
    # Uses histograms to calculate image similarity
    
    def chi2_distance(self, histA, histB, eps=1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])
    
        # return the chi-squared distance
        return d
    
    def get_method_opencv(self):
        config.read("next.ini")
        if config.get("Methods", "opencv") == "correlation":
            OPENCV_METHODS = ("Correlation", cv2.HISTCMP_CORREL)
            
        if config.get("Methods", "opencv") == "chi-squared":
            OPENCV_METHODS = ("Chi-Squared", cv2.HISTCMP_CHISQR)
            
        if config.get("Methods", "opencv") == "intersection":
            OPENCV_METHODS = ("Intersection", cv2.HISTCMP_INTERSECT)
        
        if config.get("Methods", "opencv") == "hellinger":
            OPENCV_METHODS = ("Hellinger", cv2.HISTCMP_BHATTACHARYYA),
            
        else:
            OPENCV_METHODS = ("Hellinger", cv2.HISTCMP_BHATTACHARYYA),
            
        return OPENCV_METHODS
    
    def get_method_scipy(self):
        config.read('next.ini')
        if config.get("Methods", "scipy") == "euclidean":
            SCIPY_METHODS = ("Euclidean", dist.euclidean),
            
        if config.get("Methods", "scipy") == "manhattan":
            SCIPY_METHODS = ("Manhattan", dist.cityblock),
            
        if config.get("Methods", "scipy") == "chebysev":
            SCIPY_METHODS = ("Chebysev", dist.chebyshev),
        
        else:
            SCIPY_METHODS = ("Euclidean", dist.euclidean),
        
        return SCIPY_METHODS
            
    def compare_histograms_opencv(self, images, index, frame1, frame2, sus):
        OPENCV_METHODS = self.get_method_opencv()
        # loop over the comparison methods
        for (methodName, method) in OPENCV_METHODS:
            # initialize the results dictionary and the sort
            # direction
            try:
                results = {}
                reverse = False
            except Exception as e:
                print(1)
                print(e)
            # if we are using the correlation or intersection
            # method, then sort the results in reverse order
            try:
                if methodName in ("Correlation", "Intersection"):
                    reverse = True
            except Exception as e:
                print(2)
                print(e)
         
            # loop over the index
            try:
                for (k, hist) in index.items():
                    # compute the distance between the two histograms
                    # using the method and update the results dictionary
                    try:
                        d = cv2.compareHist(index[str(frame1)], hist, method)
                        results[k] = d
                    except Exception as e:
                        print(4)
                        print(e)
            except Exception as e:
                print(3)
                print(e)
            # sort the results
            results = sorted([(v, k) for (k, v) in results.items()], reverse = reverse)
        
            
            # initialize the results figure
        fig = plt.figure("Results: %s" % (methodName))
        fig.suptitle("Login Failed " + methodName, fontsize = 20)
            
            # loop over the resultss
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
    
    def compare_histograms_scipy(self, images, index, frame1, frame2, sus):
        
        SCIPY_METHODS = self.get_method_scipy()
         
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
        fig.suptitle("Login Failed " + methodName, fontsize = 20)
            
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
    
    def compare_histograms_custom_chi(self, images, index, frame1, frame2, sus):
        # initialize the results dictionary
        results = {}
        
        # loop over the index
        
        for (k, hist) in index.items():
            # compute the distance between the two histograms
            # using the custom chi-squared method, then update
            # the results dictionary
            d = self.chi2_distance(index[str(frame1)], index[str(frame2)])
            results[k] = d
            
        # sort the results
        results = sorted([(v, k) for (k, v) in results.items()])
            
            # initialize the results figure
        fig = plt.figure("Results: Custom Chi-Squared")
        fig.suptitle("Login Failed - Custom Chi-Squared", fontsize=20)
            
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
    
    def get_custom_chi(self, lst1, frame1, frame2):
        sus = False
        x = self.create_histograms(lst1, frame1, frame2)
        y = self.compare_histograms_custom_chi(x['images'], x['index'], frame1, frame2, sus)
        print(y)
        if y[0] > float(config.get("Histogram Thresholds", "custom chi")):
            sus = True
            print("Suspicious frames detected")
            self.compare_histograms_custom_chi(x['images'], x['index'], frame1, frame2, sus)
        return sus
    
    def get_opencv(self, lst1, frame1, frame2):
        sus = False
        x = self.create_histograms(lst1, frame1, frame2)
        y = self.compare_histograms_opencv(x['images'], x['index'], frame1, frame2, sus)
        print(y)
        if y[0] > float(config.get("Histogram Thresholds", "opencv")):
            sus = True
            print("Suspicious frames detected")
            self.compare_histograms_opencv(x['images'], x['index'], frame1, frame2, sus)
        return sus
    
    def get_scipy(self, lst1, frame1, frame2):
        sus = False
        x = self.create_histograms(lst1, frame1, frame2)
        y = self.compare_histograms_scipy(x['images'], x['index'], frame1, frame2, sus)
        print(y)
        if y[0] > float(config.get("Histogram Thresholds", "scipy")):
            sus = True
            print("Suspicious frames detected")
            self.compare_histograms_scipy(x['images'], x['index'], frame1, frame2, sus)
        return sus
    
        
    
    #Gets histogram comparisons depending on what has been selected in settings.
    
    def get_comparison(self, lst1):
        count = 0
        config.read("next.ini")
        x = {}
        if config.get("Histogram Comparison", "custom chi") == "True":
            while count + 2 < len(lst1):
                frame1 = count + 1 
                frame2 = count + 2
                try:
                    x["custom_chi"] = self.get_custom_chi(lst1, frame1, frame2)
                except Exception as e:
                    print(e)
                    break
                if x["custom_chi"] == True:
                    return True
                count += 1 
        
        count = 0
        if config.get("Histogram Comparison", "opencv") == "True":
            while count < len(lst1):
                frame1 = count + 1 
                frame2 = count + 2
                try:
                    x["opencv"] = self.get_opencv(lst1, frame1, frame2)   
                except Exception as e:
                    print(e)
                    break
                if x["custom_chi"] == True:
                    return True
                count += 1 
        
        count = 0    
        if config.get("Histogram Comparison", "scipy") == "True":
            while count < len(lst1):
                frame1 = count + 1 
                frame2 = count + 2
                try:
                    x["scipy"] = self.get_scipy(lst1, frame1, frame2)   
                except Exception as e:
                    print(e)
                    break
                if x["scipy"] == True:
                    return True
                count += 1 
    
        return False
    
