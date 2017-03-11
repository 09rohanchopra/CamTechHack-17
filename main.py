from PyQt4 import QtGui,uic 
import sys 
import cv2
import os

# get the directory of this script
path = os.path.dirname(os.path.abspath(__file__))

MainWindowUI, MainWindowBase = uic.loadUiType(
    os.path.join(path, 'gui.ui'))



class VeSeeApp(MainWindowBase, MainWindowUI):
    def __init__(self):
        
        super(self.__class__, self).__init__()
        self.setupUi(self)
        
        self.startProg.clicked.connect(self.start_video)  
                                                            
    def start_video(self):
        print('Clicked!')
        camera = cv2.VideoCapture(1)
        while True:
           f,img = camera.read()
           cv2.imshow("webcam",img)
           if (cv2.waitKey(5) != -1):
               break
        video.release()


def main():
    app = QtGui.QApplication(sys.argv)  
    detector = VeSeeApp()  
    detector.show()  
    app.exec_()  


if __name__ == '__main__':  
    main()  
