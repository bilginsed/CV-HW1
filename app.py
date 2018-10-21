import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cv2

##########################################
## Do not forget to delete "return NotImplementedError"
## while implementing a function
########################################

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        return NotImplementedError


        self.title = 'Histogram Equalization'
        # You can define other things in here
        self.initUI()

    def openInputImage(self):
        # This function is called when the user clicks File->Input Image.
        return NotImplementedError

    def openTargetImage(self):
        # This function is called when the user clicks File->Target Image.
        return NotImplementedError

    def initUI(self):
        return NotImplementedError
        # Write GUI initialization code

        self.show()

    def histogramButtonClicked(self):
        if not self.inputLoaded and not self.targetLoaded:
            # Error: "First load input and target images" in MessageBox
            return NotImplementedError
        if not self.inputLoaded:
            # Error: "Load input image" in MessageBox
            return NotImplementedError
        elif not self.targetLoaded:
            # Error: "Load target image" in MessageBox
            return NotImplementedError
    
    def calcHistogram(self,I):
        hist = [[0] * 256, [0] * 256, [0] * 256]
        for H in I:
            for V in H:
                hist[0][int(V[0])] += 1
                hist[1][int(V[1])] += 1
                hist[2][int(V[2])] += 1
        return hist

    def calcP(self,hist):
        totalR = sum(hist[0])
        totalG = sum(hist[1])
        totalB = sum(hist[2])
        P = [[0] * 256, [0] * 256, [0] * 256]
        for i in range(256):
            if i != 0:
                P[0][i] = P[0][i-1] + (hist[0][i]/totalR)
                P[1][i] = P[1][i-1] + (hist[1][i]/totalG)
                P[2][i] = P[2][i-1] + (hist[2][i]/totalB)
            else:
                P[0][i] = (hist[0][i] / totalR)
                P[1][i] = (hist[1][i] / totalG)
                P[2][i] = (hist[2][i] / totalB)
        return P

    def calcLut(self,input_p,target_p):
        lut = [[0] * 256, [0] * 256, [0] * 256]
        gj = [0,0,0]
        for gi in range(255):
            for i in range(3):
                while input_p[i][gi] > target_p[i][gj[i]] and gj[i]<255:
                    gj[i]+=1
                lut[i][gi] = gj[i]
        return lut

    def remap(self,image,lut):
        h,w = len(image),len(image[0])
        re_img = np.zeros([h, w, 4], np.float32)
        for i in range(h):
            for j in range(w):
                re_img[i][j][0] = np.float32(lut[0][int(image[i][j][0])] / 255.0)
                re_img[i][j][1] = np.float32(lut[1][int(image[i][j][1])] / 255.0)
                re_img[i][j][2] = np.float32(lut[2][int(image[i][j][2])] / 255.0)
                re_img[i][j][3] = np.float32(int(image[i][j][3]) / 255.0)
        return re_img

class PlotCanvas(FigureCanvas):
    def __init__(self, hist, parent=None, width=5, height=4, dpi=100):
        return NotImplementedError
        # Init Canvas
        self.plotHistogram(hist)

    def plotHistogram(self, hist):
        return NotImplementedError
        # Plot histogram

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
