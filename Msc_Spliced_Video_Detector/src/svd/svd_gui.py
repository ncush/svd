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
        self.ui.custom_chi_checkbox.stateChanged.connect(self.custom_chi_checked)
        self.ui.default_button.clicked.connect(self.default_config)
        self.ui.save_button.clicked.connect(self.save_settings)

    def custom_chi_checked(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.custom_chi_checkbox.isChecked = True
        else:
            self.ui.custom_chi_checkbox.isChecked = False
    
    def get_settings(self):
        settings = {}
        if self.ui.custom_chi_checkbox.isChecked:
            settings["chi_box"] = "True"
        else:
            settings["chi_box"] = "False"
            
        if self.ui.opencv_checkbox.isChecked:
            settings["opencv_box"] = "True"
        else:
            settings["opencv_box"] = "False"
        
        if self.ui.numpy_checkbox.isChecked:
            settings["numpy_box"] = "True"
        else:
            settings["numpy_box"] = "False"  
        
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
        except Exception as e:
            print(e)
        config.set('Histogram Comparison','Custom Chi', x["chi_box"])
        config.set('Histogram Comparison','Numpy', x["numpy_box"])
        config.set('Histogram Comparison','OpenCV', x["opencv_box"])
        config.set('Histogram Thresholds','Custom Chi', '0.009')
        config.set('Histogram Thresholds','Numpy', '0')
        config.set('Histogram Thresholds','OpenCV', '0')
        config.set('Facial Recognition', 'Check For Face In Video', 'False')
        config.set('Facial Recognition', 'Crop Face', 'False')
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
        vidcap = cv2.VideoCapture('b.mp4')
        lst1 = frame_lst(vidcap)
#         config = {}
#         config["custom_chi"] = True
#         config["chi_distance"] = 0.009
        print(get_comparison(lst1))
    
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
        except Exception as e:
            print(e)
        config.set('Histogram Comparison','Custom Chi', 'True')
        config.set('Histogram Comparison','Numpy', 'False')
        config.set('Histogram Comparison','OpenCV', 'False')
        config.set('Histogram Thresholds','Custom Chi', '0.009')
        config.set('Histogram Thresholds','Numpy', '0')
        config.set('Histogram Thresholds','OpenCV', '0')
        config.set('Facial Recognition', 'Check For Face In Video', 'False')
        config.set('Facial Recognition', 'Crop Face', 'False')
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
        
    def browse_for_file(self):
        x = QtWidgets.QFileDialog.getOpenFileName()
        print(x[0])
        
app = QtWidgets.QApplication([])
 
application = mywindow()
 
application.show()
 
sys.exit(app.exec())