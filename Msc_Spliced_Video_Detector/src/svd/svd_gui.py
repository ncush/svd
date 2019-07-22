'''
Created on 11 Jul 2019

@author: Niall
'''
from PyQt5 import QtCore, QtWidgets
import configparser
config = configparser.ConfigParser()
from svd_gui_design import Ui_MainWindow  # importing our generated file
from svd_functions import *
from svd_main import *
import cv2

import sys
 
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
        
        self.ui.pushButton.clicked.connect(self.login_button)
        
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
        
        
    #loops through checkboxes to see if they are checked or not
    def get_settings(self):
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
        
        try:
            settings["custom_chi_spinbox"] = self.ui.custom_chi_spinbox.value()
            settings["opencv_spinbox"] = self.ui.opencv_spinbox.value()
            settings["scipy_spinbox"] = self.ui.scipy_spinbox.value()
            settings["scene_detect_spinbox"] = self.ui.scene_detect_spinbox.value()
        except Exception as e:
            print(e)
        
        return settings
    def save_settings(self):
              
        x = self.get_settings()
        print(x)
        
        try:
            cfgfile = open("next.ini",'w')
        except:
            print("something went wrong with open")
        # add the settings to the structure of the file, and lets write it out...
        try:
            config.add_section('Histogram Comparison')
            config.add_section('Histogram Thresholds')
            config.add_section('Facial Recognition')
            config.add_section('Scene Detect')
        except Exception as e:
            print(e)
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
        config.set('Scene Detect', 'Scene Detect on', x['scene_detect_checkbox'])
        config.set('Scene Detect', 'Scene Detect Threshold', str(x['scene_detect_spinbox']))
        try:
            config.write(cfgfile)
        except: 
            print("something went wrong with write")
        try:
            cfgfile.close()
        except:
            print("sometjing went wrong close")
        print('Save Settings')
        self.ui.refresh_widgets()
        
    def btnClicked(self):
        print('button clicked')
    
    def login_button(self):
        config.read("next.ini")
        video = P.get_x(self)
        threshold = config.get("Scene Detect", "scene detect threshold") 
        vidcap = cv2.VideoCapture(video)
        lst1 = frame_lst(vidcap)
        try:
            if config.get("Facial Recognition", "check for face in video"):
                count = 0
                while count < len(lst1):
                    args = {"image": lst1[str(count)], "threshold": 0.5}
                    lst1[str(count)] = detect_face(args)
                    count += 1
        except Exception as e:
            print(e)
                    
        try:    
            print(get_comparison(lst1))
            if config.get("Scene Detect", "Scene detect on") == 'True':
                x = scene_detector.find_scenes(self,video, threshold)
                if len(x) > 1:
                    print("Jump cuts detected")
                    
        except Exception as e:
            print(e)
            
    def default_config(self):
        # lets create that config file for next time...
        try:
            cfgfile = open("next.ini",'w')
        except:
            print("something went wrong with open")
        # add the settings to the structure of the file, and lets write it out...
        try:
            config.add_section('Histogram Comparison')
            config.add_section('Histogram Thresholds')
            config.add_section('Facial Recognition')
            config.add_section('Scene Detect')
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
        config.set('Scene Detect', 'Scene Detect on', 'True')
        config.set('Scene Detect', 'Scene Detect Threshold', '6')
        try:
            config.write(cfgfile)
        except: 
            print("something went wrong with write")
        try:
            cfgfile.close()
        except:
            print("sometjing went wrong close")
        print('default settings')
        self.ui.refresh_widgets()
    
    #opens browser to select file.
    def browse_for_file(self):
        y = QtWidgets.QFileDialog.getOpenFileName()
        print(y[0])
        try:
            P.set_x(self, y[0])
        except Exception as e:
            print(e)
        print(y[0])
    
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