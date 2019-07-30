# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'svd_gui_design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
import random
import configparser
from svd.svd_capture import P
config = configparser.ConfigParser()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(682, 518)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 681, 481))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")
        self.login_tab = QtWidgets.QWidget()
        self.login_tab.setObjectName("login_tab")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.main_title_label = QtWidgets.QLabel(self.login_tab)
        self.main_title_label.setGeometry(QtCore.QRect(250, 20, 201, 41))
        self.main_title_label.setObjectName("main_title_label")
        self.main_title_label.setFont(font)
        self.frame_4 = QtWidgets.QFrame(self.login_tab)
        self.frame_4.setGeometry(QtCore.QRect(10, 80, 301, 271))
        self.frame_4.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.frame_4)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, 271, 251))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.pixmap = QtGui.QPixmap('SVD_LOGO.PNG')
        self.label.setPixmap(self.pixmap)
        self.verticalLayout_4.addWidget(self.label)
        #self.resize(pixmap.width(),pixmap.height())
        self.frame_5 = QtWidgets.QFrame(self.login_tab)
        self.frame_5.setGeometry(QtCore.QRect(350, 80, 301, 271))
        self.frame_5.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.frame_5)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 10, 271, 251))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.video_confirmation_label = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.video_confirmation_label.setObjectName("video_confirmation_label")
        self.verticalLayout_5.addWidget(self.video_confirmation_label)
        self.random_sequence_lcd_number = QtWidgets.QLCDNumber(self.verticalLayoutWidget_5)
        self.random_sequence_lcd_number.setDigitCount(8)
        self.random_sequence_lcd_number.setProperty("value", random.randint(10000000,99999999))
        self.random_sequence_lcd_number.setObjectName("random_sequence_lcd_number")
        self.verticalLayout_5.addWidget(self.random_sequence_lcd_number)
        self.record_video_button = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.record_video_button.setObjectName("record_video_button")
        self.verticalLayout_5.addWidget(self.record_video_button)
        self.stop_recording_button = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.stop_recording_button.setObjectName("stop_recording_button")
        self.verticalLayout_5.addWidget(self.stop_recording_button)
        self.browse_video_button = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.browse_video_button.setObjectName("browse_video_button")
        self.verticalLayout_5.addWidget(self.browse_video_button)
        self.pushButton = QtWidgets.QPushButton(self.login_tab)
        self.pushButton.setGeometry(QtCore.QRect(290, 400, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.info_label = QtWidgets.QLabel(self.login_tab)
        self.info_label.setGeometry(QtCore.QRect(230, 353, 191, 41))
        self.info_label.setObjectName("info_label")
        self.tabWidget.addTab(self.login_tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.frame = QtWidgets.QFrame(self.tab_2)
        self.frame.setGeometry(QtCore.QRect(10, 10, 311, 191))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 291, 171))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.histogram__comparison_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.histogram__comparison_label.setObjectName("histogram__comparison_label")
        self.verticalLayout_2.addWidget(self.histogram__comparison_label)
        self.custom_chi_checkbox = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.custom_chi_checkbox.setChecked(False)
        self.custom_chi_checkbox.setObjectName("custom_chi_checkbox")
        self.verticalLayout_2.addWidget(self.custom_chi_checkbox)
        self.opencv_checkbox = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.opencv_checkbox.setObjectName("opencv_checkbox")
        self.verticalLayout_2.addWidget(self.opencv_checkbox)
        self.scipy_checkbox = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.scipy_checkbox.setObjectName("scipy_checkbox")
        self.verticalLayout_2.addWidget(self.scipy_checkbox)
        self.frame_2 = QtWidgets.QFrame(self.tab_2)
        self.frame_2.setGeometry(QtCore.QRect(10, 210, 311, 211))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setMidLineWidth(0)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 291, 204))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.histogram_similarity_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.histogram_similarity_label.setObjectName("histogram_similarity_label")
        self.verticalLayout.addWidget(self.histogram_similarity_label)
        self.hs_custom_chi_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.hs_custom_chi_label.setObjectName("hs_custom_chi_label")
        self.verticalLayout.addWidget(self.hs_custom_chi_label)
        self.custom_chi_spinbox = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        self.custom_chi_spinbox.setDecimals(3)
        self.custom_chi_spinbox.setMaximum(5.0)
        self.custom_chi_spinbox.setSingleStep(0.001)
        self.custom_chi_spinbox.setObjectName("custom_chi_spinbox")
        self.verticalLayout.addWidget(self.custom_chi_spinbox)
        self.hs_opencv_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.hs_opencv_label.setObjectName("hs_opencv_label")
        self.verticalLayout.addWidget(self.hs_opencv_label)
        self.opencv_spinbox = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        self.opencv_spinbox.setDecimals(3)
        self.opencv_spinbox.setMaximum(5.0)
        self.opencv_spinbox.setSingleStep(0.001)
        self.opencv_spinbox.setObjectName("opencv_spinbox")
        self.verticalLayout.addWidget(self.opencv_spinbox)
        self.hs_scipy_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.hs_scipy_label.setObjectName("hs_scipy_label")
        self.verticalLayout.addWidget(self.hs_scipy_label)
        self.scipy_spinbox = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        self.scipy_spinbox.setDecimals(3)
        self.scipy_spinbox.setMaximum(5.0)
        self.scipy_spinbox.setSingleStep(0.001)
        self.scipy_spinbox.setObjectName("scipy_spinbox")
        self.verticalLayout.addWidget(self.scipy_spinbox)
        self.frame_3 = QtWidgets.QFrame(self.tab_2)
        self.frame_3.setGeometry(QtCore.QRect(340, 10, 321, 191))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(1)
        self.frame_3.setMidLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.frame_3)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 291, 171))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.facial_recognition_label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.facial_recognition_label.setObjectName("facial_recognition_label")
        self.verticalLayout_3.addWidget(self.facial_recognition_label)
        self.check_face_checkbox = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.check_face_checkbox.setObjectName("check_face_checkbox")
        self.verticalLayout_3.addWidget(self.check_face_checkbox)
        self.crop_face_checkbox = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.crop_face_checkbox.setObjectName("crop_face_checkbox")
        self.verticalLayout_3.addWidget(self.crop_face_checkbox)
        self.frame_6 = QtWidgets.QFrame(self.tab_2)
        self.frame_6.setGeometry(QtCore.QRect(340, 210, 321, 211))
        self.frame_6.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setLineWidth(1)
        self.frame_6.setMidLineWidth(0)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.frame_6)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 10, 291, 171))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.scene_detect_label = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.scene_detect_label.setObjectName("scene_detect_label")
        self.verticalLayout_6.addWidget(self.scene_detect_label)
        self.scene_detect_checkbox = QtWidgets.QCheckBox(self.verticalLayoutWidget_6)
        self.scene_detect_checkbox.setEnabled(True)
        self.scene_detect_checkbox.setObjectName("scene_detect_checkbox")
        self.verticalLayout_6.addWidget(self.scene_detect_checkbox)
        self.scene_detect_threshold_label = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.scene_detect_threshold_label.setObjectName("scene_detect_threshold_label")
        self.verticalLayout_6.addWidget(self.scene_detect_threshold_label)
        self.scene_detect_spinbox = QtWidgets.QSpinBox(self.verticalLayoutWidget_6)
        self.scene_detect_spinbox.setObjectName("scene_detect_spinbox")
        self.verticalLayout_6.addWidget(self.scene_detect_spinbox)
        self.save_button = QtWidgets.QPushButton(self.tab_2)
        self.save_button.setGeometry(QtCore.QRect(90, 430, 131, 21))
        self.save_button.setObjectName("save_button")
        self.default_button = QtWidgets.QPushButton(self.tab_2)
        self.default_button.setGeometry(QtCore.QRect(420, 430, 131, 21))
        self.default_button.setObjectName("default_button")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 682, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    #refreshes widgets.
    def refresh_widgets(self):
        config.read("next.ini")
        
        try:
            #Checkboxes
            if config.get("Histogram Comparison", "custom chi") == "True":
                self.custom_chi_checkbox.setChecked(True)
            else:
                self.custom_chi_checkbox.setChecked(False)
                
            if config.get("Histogram Comparison", "scipy") == "True":
                self.scipy_checkbox.setChecked(True)
            else:
                self.scipy_checkbox.setChecked(False)
                
            if config.get("Histogram Comparison", "opencv") == "True":
                self.opencv_checkbox.setChecked(True)
            else:
                self.opencv_checkbox.setChecked(False)
            
            if config.get("Facial Recognition", "Check For Face In Video") == "True":
                self.check_face_checkbox.setChecked(True)
            else:
                self.check_face_checkbox.setChecked(False)
                
            if config.get("Facial Recognition", "Crop Face") == "True":
                self.crop_face_checkbox.setChecked(True)
            else:
                self.crop_face_checkbox.setChecked(False)
            
            if config.get("Scene Detect", "Scene Detect On") == "True":
                self.scene_detect_checkbox.setChecked(True)
            else:
                self.scene_detect_checkbox.setChecked(False)
                
        except:
            print("no config found")
        try:
            self.custom_chi_spinbox.setValue(float(config.get("Histogram Thresholds", "Custom Chi")))
            self.scipy_spinbox.setValue(float(config.get("Histogram Thresholds", "scipy")))
            self.opencv_spinbox.setValue(float(config.get("Histogram Thresholds", "opencv")))
            self.scene_detect_spinbox.setValue(float(config.get("Scene Detect", "Scene detect threshold")))
            
        except Exception as e:
            print(e)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spliced Video Detector"))
        self.main_title_label.setText(_translate("MainWindow", "Spliced Video Detector"))
        self.video_confirmation_label.setText(_translate("MainWindow", "Video Confirmation"))
        self.record_video_button.setText(_translate("MainWindow", "Record video"))
        self.stop_recording_button.setText(_translate("MainWindow", "Stop Recording"))
        self.browse_video_button.setText(_translate("MainWindow", "Browse for video"))
        self.pushButton.setText(_translate("MainWindow", "Analyse Video"))
        self.info_label.setText(_translate("MainWindow", ""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.login_tab), _translate("MainWindow", "Home"))
        self.histogram__comparison_label.setText(_translate("MainWindow", "Histogram Comparison"))
        self.custom_chi_checkbox.setText(_translate("MainWindow", "Custom Chi"))
        self.opencv_checkbox.setText(_translate("MainWindow", "OpenCV"))
        self.scipy_checkbox.setText(_translate("MainWindow", "scipy"))
        self.histogram_similarity_label.setText(_translate("MainWindow", "Histogram similarity threshold"))
        self.hs_custom_chi_label.setText(_translate("MainWindow", "Custom Chi"))
        self.hs_opencv_label.setText(_translate("MainWindow", "OpenCV"))
        self.hs_scipy_label.setText(_translate("MainWindow", "scipy"))
        self.facial_recognition_label.setText(_translate("MainWindow", "Facial Recognition"))
        self.check_face_checkbox.setText(_translate("MainWindow", "Check for face in video"))
        self.crop_face_checkbox.setText(_translate("MainWindow", "Crop Face"))
        self.scene_detect_label.setText(_translate("MainWindow", "SceneDetect"))
        self.scene_detect_checkbox.setText(_translate("MainWindow", "Use SceneDetect"))
        self.scene_detect_threshold_label.setText(_translate("MainWindow", "SceneDetect Threshold"))
        self.save_button.setText(_translate("MainWindow", "Save Settings"))
        self.default_button.setText(_translate("MainWindow", "Default Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Settings"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "Config"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        