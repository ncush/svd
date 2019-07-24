'''
Created on 11 Jul 2019

@author: Niall
'''
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QCoreApplication
import configparser
from svd.svd_gui_design import Ui_Dialog
config = configparser.ConfigParser()
from svd.svd_gui_design import Ui_MainWindow, Ui_Dialog as Form, Ui_Dialog2 as Form2   # importing our generated file
from svd.svd_functions import *
from svd.svd_main import *
import cv2

import sys
 
class mywindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super(mywindow, self).__init__()
        
        self.dialog = Ui_Dialog()
        
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
        
        
    def open_success_dialog(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Form()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()
    
    def open_unsuccessful_dialog(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Form2()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()
        
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
        
        try:
            settings["custom_chi_spinbox"] = self.ui.custom_chi_spinbox.value()
            settings["opencv_spinbox"] = self.ui.opencv_spinbox.value()
            settings["scipy_spinbox"] = self.ui.scipy_spinbox.value()
            settings["scene_detect_spinbox"] = self.ui.scene_detect_spinbox.value()
        except Exception as e:
            print(e)
        try:
            settings["scipy_method"] = config.get("Methods", "scipy")
            settings["opencv_method"] = config.get("Methods", "opencv")
            settings["facial_recognition_threshold"] = config.get("Facial Recognition", "threshold")
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
            config.add_section('Methods')
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
        self.ui.refresh_widgets()
        
    def btnClicked(self):
        print('button clicked')
    
    def login_button(self):
        try:
            video = P.get_x(self)
        except Exception as e:
            print(e)
        config.read("next.ini")
        threshold = config.get("Scene Detect", "scene detect threshold") 
        
        vidcap = cv2.VideoCapture(video)
        lst1 = frame_lst(vidcap)
        try:
            if config.get("Facial Recognition", "check for face in video") == "True":
                crop = False
                count = 0
                while count + 1 < len(lst1):
                    args = {"image": lst1[str(count)], "threshold": float(config.get("Facial Recognition", "threshold")), "crop": crop}
                    face_detected = detect_face(args)
                    if face_detected == False:
                        print("No face detected")
                        return 
                    count += 1
                if config.get("Facial Recognition", "crop face") == "True":
                    crop = True
                    count = 0
                    while count + 1 < len(lst1):
                        args = {"image": lst1[str(count)], "threshold": 0.5, "crop": crop}
                        lst1[str(count)] = detect_face(args)
                        count += 1
                    
        except Exception as e:
            print(e)
                    
        try:    
            success = True
            x = get_comparison(lst1)
            if x == False:
                if config.get("Scene Detect", "Scene detect on") == 'True':
                    y = scene_detector.find_scenes(self,video, threshold)
                    if len(y) > 1:
                        success = False
                        print("Jump cuts detected")
                        self.open_unsuccessful_dialog()
                if success:
                    self.open_success_dialog()
                    
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
        self.ui.refresh_widgets()
    
    #opens browser to select file.
    def browse_for_file(self):
        y = QtWidgets.QFileDialog.getOpenFileName()
        try:
            P.set_x(self, y[0])
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