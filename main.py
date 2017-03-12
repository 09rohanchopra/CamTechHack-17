from PyQt4 import QtGui,uic,QtCore
import sys, os, time
import cv2
import ctypes

# get the directory of this script
path = os.path.dirname(os.path.abspath(__file__))

MainWindowUI, MainWindowBase = uic.loadUiType(
    os.path.join(path, 'gui.ui'))

ReportPageUI, ReportPageBase = uic.loadUiType(
    os.path.join(path, 'report.ui'))

myappid = 'VSee.scanner.0.01' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class VeSeeApp(MainWindowBase, MainWindowUI):
    def __init__(self):
        
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.startButton.clicked.connect(self.start_video)

        self.analysingLabel.setVisible(False)
        self.logoLabel.setPixmap(QtGui.QPixmap("logo.png"))
        self.logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.logoLabel.resize(50,50)
                                                            
    def start_video(self):
        print('Clicked!')
        self.startButton.setVisible(False)
        self.buttonFrame.setVisible(False)
        self.analysingLabel.setVisible(True)
        #Function for camera
        #Function for IR
        time.sleep(3)
        self.report = ReportPage()
        self.report.show()
        
class ReportPage(ReportPageBase, ReportPageUI):
    def __init__(self, parent=None):
        ReportPageBase.__init__(self, parent)
        self.setupUi(self)

def main():
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('logo.png'))
    detector = VeSeeApp()  
    detector.show()  
    app.exec_()  


if __name__ == '__main__':  
    main()  
