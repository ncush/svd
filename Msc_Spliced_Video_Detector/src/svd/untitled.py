from PyQt5 import QtCore, QtGui, QtWidgets
    
class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 200, 75, 23))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuyo = QtWidgets.QMenu(self.menubar)
        self.menuyo.setObjectName("menuyo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionsup = QtWidgets.QAction(MainWindow)
        self.actionsup.setObjectName("actionsup")
        self.actionfaggit = QtWidgets.QAction(MainWindow)
        self.actionfaggit.setObjectName("actionfaggit")
        self.menuyo.addAction(self.actionsup)
        self.menuyo.addAction(self.actionfaggit)
        self.menubar.addAction(self.menuyo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "ok"))
        self.menuyo.setTitle(_translate("MainWindow", "yo"))
        self.actionsup.setText(_translate("MainWindow", "sup"))
        self.actionfaggit.setText(_translate("MainWindow", "faggit"))

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     w = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(w)
#     w.show()
#     sys.exit(app.exec_())