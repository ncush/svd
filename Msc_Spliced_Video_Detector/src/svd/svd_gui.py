'''
Created on 11 Jul 2019

@author: Niall
'''
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QCoreApplication
import configparser
config = configparser.ConfigParser()
from svd.svd_gui_design import Ui_MainWindow
from svd.svd_histogram_analysis import HistogramAnalysis
from svd.svd_face_detect import FaceDetection
from svd.svd_capture import Capture
from svd.svd_file_name import FileName
from svd.svd_scene_detector import SceneDetector
from svd.svd_frame_lst import FrameList
import cv2
import os
import sys

framelist = FrameList()
hist = HistogramAnalysis()
facedetect = FaceDetection()

class mywindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super(mywindow, self).__init__()
        
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)
        
        self.ui.refresh_widgets()
        
        #recording video buttons
        self.capture = Capture()
        self.ui.record_video_button.clicked.connect(self.capture.startCapture)
        self.ui.stop_recording_button.clicked.connect(self.capture.endCapture)
        self.ui.browse_video_button.clicked.connect(self.browse_for_file)
        #Main button to begin analysis
        self.ui.pushButton.clicked.connect(self.login_button)
        
        #Menu bar
        self.ui.actionHelp.triggered.connect(self.help_menu_button)
        self.ui.actionAbout.triggered.connect(self.config_menu_button)
        self.ui.actionQuit.triggered.connect(self.quit_menu_button)
        
        ##settings
        self.ui.default_button.clicked.connect(self.default_config)
        self.ui.save_button.clicked.connect(self.save_settings)
    
        #checkboxes
        self.ui.custom_chi_checkbox.stateChanged.connect(self.custom_chi_checked)
        self.ui.opencv_checkbox.stateChanged.connect(self.opencv_checked)
        self.ui.scipy_checkbox.stateChanged.connect(self.scipy_checked)
        self.ui.check_face_checkbox.stateChanged.connect(self.check_face_checked)
        self.ui.crop_face_checkbox.stateChanged.connect(self.crop_face_checked)
        self.ui.scene_detect_checkbox.stateChanged.connect(self.scene_detect_checked)
        
    #Opens config file
    def config_menu_button(self):
        try:
            os.startfile("next.ini")
        except Exception as e:
            print(e)
    
    #opens help document
    def help_menu_button(self):
        try:
            os.startfile("svd_help_document.pdf")
        except Exception as e:
            print(e)
            
    #Quits program
    def quit_menu_button(self):
        sys.exit()
        
    #loops through checkboxes to see if they are checked or not
    def get_settings(self):
        config.read('next.ini')
        lst = [[self.ui.custom_chi_checkbox, "custom_chi_checkbox"], [self.ui.opencv_checkbox, "opencv_checkbox"], [self.ui.scipy_checkbox, "scipy_checkbox"],[self.ui.check_face_checkbox, "check_face_checkbox"],[self.ui.crop_face_checkbox,"crop_face_checkbox"],[self.ui.scene_detect_checkbox,"scene_detect_checkbox"]]
        settings = {}
        try:
            for l in lst:
                if l[0].isChecked:
                    settings[l[1]] = "True"
                else:
                    settings[l[1]] = "False"
        except Exception as e:
            print(e)
            
        #Checks spin boxes for new values values
        try:
            settings["custom_chi_spinbox"] = self.ui.custom_chi_spinbox.value()
            settings["opencv_spinbox"] = self.ui.opencv_spinbox.value()
            settings["scipy_spinbox"] = self.ui.scipy_spinbox.value()
            settings["scene_detect_spinbox"] = self.ui.scene_detect_spinbox.value()
        except Exception as e:
            print(e)
        
        #checks config file for whether the method has been changed
        try:
            settings["scipy_method"] = config.get("Methods", "scipy")
            settings["opencv_method"] = config.get("Methods", "opencv")
            settings["facial_recognition_threshold"] = config.get("Facial Recognition", "threshold")
        except Exception as e:
            print(e)
        return settings
    
    #saves new settings chosen on the GUI to config file
    def save_settings(self):
        #gets the settings, saves them to new dictionary    
        x = self.get_settings()
        print(x)
        
        #opens config file so we can write to it.
        try:
            cfgfile = open("next.ini",'w')
        except:
            print("something went wrong with open")
        #if these sections don't exist they are added
        try:
            config.add_section('Histogram Comparison')
            config.add_section('Histogram Thresholds')
            config.add_section('Facial Recognition')
            config.add_section('Scene Detect')
            config.add_section('Methods')
        except Exception as e:
            print(e)
            
        #updates the config file
        config.set('Histogram Comparison','Custom Chi', x["custom_chi_checkbox"])
        config.set('Histogram Comparison','scipy', x["scipy_checkbox"])
        config.set('Histogram Comparison','OpenCV', x["opencv_checkbox"])
        try:
            config.set('Histogram Thresholds','Custom Chi', str(x["custom_chi_spinbox"]))
        except Exception as e:
            print(e)
        config.set('Histogram Thresholds','scipy', str(x["scipy_spinbox"]))
        config.set('Histogram Thresholds','OpenCV', str(x["opencv_spinbox"]))
        config.set('Facial Recognition', 'Check For Face In Video', x['check_face_checkbox'])
        config.set('Facial Recognition', 'Crop Face', x['crop_face_checkbox'])
        config.set('Facial Recognition', 'threshold', x['facial_recognition_threshold'])
        config.set('Scene Detect', 'Scene Detect on', x['scene_detect_checkbox'])
        config.set('Scene Detect', 'Scene Detect Threshold', str(x['scene_detect_spinbox']))
        config.set('Methods', "scipy", x['scipy_method'])
        config.set('Methods', "opencv", x['opencv_method'])
        try:
            config.write(cfgfile)
        except: 
            print("something went wrong with write")
        try:
            cfgfile.close()
        except:
            print("something went wrong close")
        print('Save Settings')
        
        #refreshes the GUI to represent the new settings
        self.ui.refresh_widgets()
        
    #Applies analysis on the video
    #Checks to see if methods should be applied and then applies them
    def login_button(self):
        self.ui.info_label.setText("Please be patient, face detection \n can take up to 30 seconds")
        #gets the file name
        try:
            video = FileName.get_file_name(self)
        except Exception as e:
            self.ui.info_label.setText("no file selected")
            return
        
        #checks to make sure file is mp4 format
        if not video.endswith('.mp4'):
            self.ui.info_label.setText("please select an mp4 file")
            return 
        
        config.read("next.ini")
        threshold = config.get("Scene Detect", "scene detect threshold")
        
        #initialises video so it can be interacted with
        vidcap = cv2.VideoCapture(video)
        
        #creates dictionary of frames from video
        lst1 = framelist.frame_lst(vidcap)
        #checks that file is not too long
        if len(lst1) > 450:
            self.ui.info_label.setText("File must be 15 seconds or less")
            return
        
        try:
            #checks if check for face has been selected
            if config.get("Facial Recognition", "check for face in video") == "True":
                crop = False
                #checks if crop face has been selected
                if config.get("Facial Recognition", "crop face") == "True":
                    crop = True
                #runs the facedetection method 
                args = {"image": lst1, "threshold": float(config.get("Facial Recognition", "threshold")), "crop": crop}
                face_detected = facedetect.face_detect(args)
                #if no face is detected, user is informed and function is terminated
                if face_detected['face'] == "False":
                    self.ui.info_label.setText("No face detected")
                    return 
                #if crop face is selected, the dictionary of frames is replaced with new dictionary of cropped frames
                if crop:
                    lst1 = face_detected['crop']
                self.ui.info_label.setText("Face detection and cropping complete" )
        except Exception as e:
            print(e)
            
                    
        try:    
            success = True
            #Calls histogram comparison function
            sus = hist.get_comparison(lst1)
            self.ui.info_label.setText(" ")
            
            #if the histogram comparison function returns false
            #check to see if s
            if sus == False:
                if config.get("Scene Detect", "Scene detect on") == 'True':
                    y = SceneDetector.find_scenes(self,video, threshold)
                    if len(y) > 1:
                        success = False
                        print("Jump cuts detected")
                        self.ui.info_label.setText("Scene Detect - splice detected")
                if success:
                    self.ui.info_label.setText("Success! No splices detected.")
            if sus == True:
                self.ui.info_label.setText("Suspicious frames detected")        
        except Exception as e:
            print(e)
            
    #sets settings to default
    def default_config(self):
        # Creates config file if it doesn't exist.
        #Opens config file to be edited
        try:
            cfgfile = open("next.ini",'w')
        except:
            print("something went wrong with open")
        # adds sections to config file if they don't exist
        try:
            config.add_section('Histogram Comparison')
            config.add_section('Histogram Thresholds')
            config.add_section('Facial Recognition')
            config.add_section('Scene Detect')
            config.add_section('Methods')
        except Exception as e:
            print(e)
        config.set('Histogram Comparison','Custom Chi', 'True')
        config.set('Histogram Comparison','scipy', 'False')
        config.set('Histogram Comparison','OpenCV', 'False')
        config.set('Histogram Thresholds','Custom Chi', '0.009')
        config.set('Histogram Thresholds','scipy', '0')
        config.set('Histogram Thresholds','OpenCV', '0')
        config.set('Facial Recognition', 'Check For Face In Video', 'False')
        config.set('Facial Recognition', 'Crop Face', 'False')
        config.set('Facial Recognition', "Threshold", '0.5')
        config.set('Scene Detect', 'Scene Detect on', 'True')
        config.set('Scene Detect', 'Scene Detect Threshold', '6')
        config.set('Methods', "opencv", "hellinger")
        config.set('Methods', "scipy", "euclidean")
        try:
            config.write(cfgfile)
        except: 
            print("something went wrong with write")
        try:
            cfgfile.close()
        except:
            print("sometjing went wrong close")
        print('default settings')
        #refreshes the GUI to represent the new changes
        self.ui.refresh_widgets()
    
    #opens browser to select file.
    def browse_for_file(self):
        y = QtWidgets.QFileDialog.getOpenFileName()
        try:
            #sets property to file name
            FileName.set_file_name(self, y[0])
        except Exception as e:
            print(e)
    
    #checkbox functions     
    def custom_chi_checked(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.custom_chi_checkbox.isChecked = True
        else:
            self.ui.custom_chi_checkbox.isChecked = False
    
    def opencv_checked(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.opencv_checkbox.isChecked = True
        else:
            self.ui.opencv_checkbox.isChecked = False
        
    def scipy_checked(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.scipy_checkbox.isChecked = True
        else:
            self.ui.scipy_checkbox.isChecked = False
    
    def check_face_checked(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.check_face_checkbox.isChecked = True
        else:
            self.ui.check_face_checkbox.isChecked = False
    
    def crop_face_checked(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.crop_face_checkbox.isChecked = True
        else:
            self.ui.crop_face_checkbox.isChecked = False   
            
    def scene_detect_checked(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.scene_detect_checkbox.isChecked = True
        else:
            self.ui.scene_detect_checkbox.isChecked = False 
            
    
app = QtWidgets.QApplication([])
 
application = mywindow()
 
application.show()
 
sys.exit(app.exec())