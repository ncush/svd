'''
Created on 11 Jul 2019

@author: Niall
'''
from PyQt5 import QtWidgets
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
        
        #recording video buttons
        self.capture = Capture()
        self.ui.record_video_button.clicked.connect(self.capture.startCapture)
        
        self.ui.pushButton.clicked.connect(self.login_button)
        
        self.ui.histogram_comparison_set_button.clicked.connect(self.default_config)
               
        
    def btnClicked(self):
        print('button clicked')
    
    def login_button(self):
        config('next.ini')
        vidcap = cv2.VideoCapture('a.mp4')
        lst1 = frame_lst(vidcap)
#         config = {}
#         config["custom_chi"] = True
#         config["chi_distance"] = 0.009
        print(get_comparison(lst1, config))
    
    def default_config(self):
        # lets create that config file for next time...
        cfgfile = open("next.ini",'w')
        # add the settings to the structure of the file, and lets write it out...
        config.add_section('Histogram Comparison')
        config.set('Histogram Comparison','Custom Chi', 'True')
        config.set('Histogram Comparison','Numpy', 'False')
        config.set('Histogram Comparison','OpenCV', 'False')
        config.add_section('Histogram Thresholds')
        config.set('Histogram Thresholds','Custom Chi', '0.009')
        config.set('Histogram Thresholds','Numpy', '0')
        config.set('Histogram Thresholds','OpenCV', '0')
        config.add_section('Facial Recognition')
        config.set('Facial Recognition', 'Check For Face In Video', 'False')
        config.set('Facial Recognition', 'Crop Face', 'False')
        config.write(cfgfile)
        cfgfile.close()
        print('default settings')
    
 
app = QtWidgets.QApplication([])
 
application = mywindow()
 
application.show()
 
sys.exit(app.exec())