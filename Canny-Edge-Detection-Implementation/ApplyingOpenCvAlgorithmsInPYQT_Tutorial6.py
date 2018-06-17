import cv2
import numpy as np
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
# from PyQt5.uic.properties import QtCore
from PyQt5 import QtCore


class gui(QDialog):
    def __init__(self):
        super(gui, self).__init__()  # that is the way a qDialogue of created
        loadUi('GuiQTDesigner.ui', self)
        self.image = None  # I just created a local variable to the class
        self.processedImage=None
        self.loadButton.clicked.connect(self.loadClicked)
        # here, I made a window in designer. Then I created a push button and a label,
        # then renamed it to push button,
        #  IT CREATED A CLASS IN THE GUIQTDESIGNER.UI  which  I can now reference.
        self.saveButton.clicked.connect(self.saveClicked)
        self.cannyButton.clicked.connect(self.cannyClicked)
        self.cannySlider.valueChanged.connect(self.cannyDisplay)

    @pyqtSlot()
    def cannyDisplay(self):
        gray=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY) if len(self.image.shape)>=3 else self.image
        self.processedImage=cv2.Canny(gray,self.cannySlider.value(),self.cannySlider.value()*3)
        self.displayImage(2)
    @pyqtSlot()
    def cannyClicked(self):
        # we want to apply canny to the given image
        # print('here')
        gray = 0
        if (len(self.image.shape) >= 3):
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.image

        self.processedImage = cv2.Canny(gray, 100, 200)
        self.displayImage(2)

    @pyqtSlot()  # enables the button, window function into the class, function that initialzis the class
    def loadClicked(self):
        # file dialog box whenever I click this button
        fname, filter = QFileDialog.getOpenFileName(self, 'OpenFile', 'G:\Programming\opencv\Tutorials\images', 'Image Files (*.jpg)')
        if fname:
            self.loadImage(fname)
        else:
            print('Invalid Image')

    @pyqtSlot()
    def saveClicked(self):
        fname, filter = QFileDialog.getSaveFileName(self, 'Save File', 'C:\\', 'Image Files (*.jpg)')
        if fname:
            cv2.imwrite(fname,self.processedImage)
        else:
            print('Error')

    def loadImage(self, fname):
        # print('loading')
        self.image = cv2.imread(fname)
        self.processedImage=self.image.copy()

        self.displayImage(1)

    def displayImage(self,windowName=1):
        # convert a numpy array to qimage
        # print('something please')

        qformat = QImage.Format_Indexed8

        if len(self.processedImage.shape) == 3:  # rows cols and color channel.
            if self.processedImage.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.processedImage, self.processedImage.shape[1], self.processedImage.shape[0], self.processedImage.strides[0], qformat)
        img = img.rgbSwapped()  # RGB to BGR to display(basic)
        if(windowName==1):
            self.imageLabel.setPixmap(QPixmap.fromImage(img))
            self.imageLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        else:
            self.processedLabel.setPixmap(QPixmap.fromImage(img))
            self.processedLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)



app = QApplication(sys.argv)
window = gui()
window.setWindowTitle('Python Gui Tutorial')
# print(dir(window))
# window.setGeometry(100,100,400,200)

window.show()
sys.exit(app.exec_())
