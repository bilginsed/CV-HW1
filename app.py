import sys,random,os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog,QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Histogram Equalization'
        # app position info
        self.left = 20
        self.top = 30
        self.width = 1500
        self.height = 700
        self.targetLoaded = False
        self.inputLoaded = False
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.box_style = "{ border: 1px solid grey}"
        self.initUI()

    def openInputImage(self):
        # action of menu File -> Open input
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # desired input image file dir
        self.input_file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Png Images (*.png)", options=options)
        if self.input_file_name:
            self.load_input()

    def openTargetImage(self):
        # action of menu File -> Open target
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # desired target image file dir
        self.target_file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Png Images (*.png)", options=options)
        if self.target_file_name:
            self.load_target()



    def initUI(self):
        self.setWindowTitle(self.title)
        #menu actions
        open_input_act = QAction('&Open Input', self)
        open_input_act.triggered.connect(self.openInputImage)
        open_target_act = QAction('&Open Target', self)
        open_target_act.triggered.connect(self.openTargetImage)
        exit_act = QAction('&Exit', self)
        exit_act.triggered.connect(self.close)
        #/menu actions
        menubar = self.menuBar()            #create menu bar
        fileMenu = menubar.addMenu('&File') #create file menu and add actions
        fileMenu.addAction(open_input_act)
        fileMenu.addAction(open_target_act)
        fileMenu.addAction(exit_act)

        top_lay = QVBoxLayout(self.central_widget)                  #Base Vertical layout
        # Button configurations
        equalize_button = QPushButton("Equalize Histogram",self)
        equalize_button.setStyleSheet("Text-align:left")
        equalize_button.clicked.connect(self.histogramButtonClicked)
        equalize_button.move(100,70)
        # Button configurations
        top_lay.addWidget(equalize_button)          # Button add the top

        lay = QHBoxLayout()     # vertical layout
        top_lay.addLayout(lay)
        # add three boxes for image visualization
        self.box_left = QGroupBox('Input')
        self.box_left.setStyleSheet(self.box_style)
        self.box_left.setFixedWidth(400)
        self.box_middle = QGroupBox('Target')
        self.box_middle.setStyleSheet(self.box_style)
        self.box_middle.setFixedWidth(400)
        self.box_right = QGroupBox('Result')
        self.box_right.setStyleSheet(self.box_style)
        self.box_right.setFixedWidth(400)
        #/ add three boxes for image visualization

        lay.addWidget(self.box_left)        #add box to Horizontal Layout
        lay.addWidget(self.box_middle)
        lay.addWidget(self.box_right)

        self.statusBar().showMessage('Ready')
        self.resize(self.width, self.height)
        self.show()

    def load_input(self):
        #input file processing
        if not self.inputLoaded:
            lay = QVBoxLayout(self.box_left)
            label = QLabel(self)
            pixmap = QPixmap(self.input_file_name)      #import image from image file_path
            label.setPixmap(pixmap.scaled(pixmap.width()/2,pixmap.height()/2,Qt.KeepAspectRatioByExpanding)) # because resolution image resize to %50
            self.input_img = mpimg.imread(self.input_file_name)* 255        #image as a np.array
            self.hist_input = self.calcHistogram(self.input_img)            #histogram calc
            canvas_red = PlotCanvas(self.hist_input[0],color='r')
            canvas_green = PlotCanvas(self.hist_input[1],color='g')
            canvas_blue = PlotCanvas(self.hist_input[2],color='b')
            # box add items
            lay.addWidget(label,alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_red,alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_green,alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_blue,alignment=Qt.AlignHCenter)
            #/ box add items
            self.statusBar().showMessage('Load input')
            self.inputLoaded = True

    def load_target(self):
        #target file processing
        if not self.targetLoaded:
            lay = QVBoxLayout(self.box_middle)
            label = QLabel(self)
            pixmap = QPixmap(self.target_file_name)     #import image from image file_path
            label.setPixmap(pixmap.scaled(pixmap.width() / 2, pixmap.height() / 2, Qt.KeepAspectRatioByExpanding))  # because resolution image resize to %50
            self.target_img = mpimg.imread(self.target_file_name) * 255     #image as a np.array
            self.hist_target = self.calcHistogram(self.target_img)          #histogram calc
            canvas_red = PlotCanvas(self.hist_target[0], color='r')
            canvas_green = PlotCanvas(self.hist_target[1], color='g')
            canvas_blue = PlotCanvas(self.hist_target[2], color='b')
            # box add items
            lay.addWidget(label, alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_red, alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_green, alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_blue, alignment=Qt.AlignHCenter)
            #/ box add items
            self.statusBar().showMessage('Load target')
            self.targetLoaded = True

    def histogramButtonClicked(self):
        self.statusBar().showMessage('cal')
        #errors
        if not self.inputLoaded and not self.targetLoaded:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("First load input and target images")
            msg.setWindowTitle("Missing Image")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif not self.inputLoaded:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Load input image")
            msg.setWindowTitle("Missing Image")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif not self.targetLoaded:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Load target image")
            msg.setWindowTitle("Missing Image")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        #/errors
        else:
            try:
                input_p = self.calcP(self.hist_input)       #calculate P of input image
                target_p = self.calcP(self.hist_target)     #calculate P of target image
                lut = self.calcLut(input_p,target_p)        #calculate lut
                remap_img = self.remap(self.input_img,lut)  #remapping
                file_name = str(random.randint(100,500))+'.png'     #temp file
                plt.imsave(file_name,remap_img)
                lay = QVBoxLayout(self.box_right)
                label = QLabel(self)
                pixmap = QPixmap(file_name)
                os.remove(file_name)    #temp file remove
                label.setPixmap(pixmap.scaled(pixmap.width() / 2, pixmap.height() / 2, Qt.KeepAspectRatioByExpanding))
                hist = self.calcHistogram(remap_img*255)        #remap image histogram
                canvas_red = PlotCanvas(hist[0], color='r')
                canvas_green = PlotCanvas(hist[1], color='g')
                canvas_blue = PlotCanvas(hist[2], color='b')
                lay.addWidget(label, alignment=Qt.AlignHCenter)
                lay.addWidget(canvas_red, alignment=Qt.AlignHCenter)
                lay.addWidget(canvas_green, alignment=Qt.AlignHCenter)
                lay.addWidget(canvas_blue, alignment=Qt.AlignHCenter)
            except Exception as e:
                print(e)

    def calcHistogram(self,I):
        hist = [[0] * 256, [0] * 256, [0] * 256]
        # R G B array
        for H in I:
            for V in H:
                hist[0][int(V[0])] += 1 # Red       counting
                hist[1][int(V[1])] += 1 # Green     counting
                hist[2][int(V[2])] += 1 # Blue      counting
        return hist

    def calcP(self,hist):
        # Probability of R,G,B
        totalR = sum(hist[0])
        totalG = sum(hist[1])
        totalB = sum(hist[2])
        P = [[0] * 256, [0] * 256, [0] * 256]
        for i in range(256):
            if i != 0:
                P[0][i] = P[0][i-1] + (hist[0][i]/totalR)   #   P of R is (hist[0][i]/totalR) + itself
                P[1][i] = P[1][i-1] + (hist[1][i]/totalG)
                P[2][i] = P[2][i-1] + (hist[2][i]/totalB)
            else:
                P[0][i] = (hist[0][i] / totalR)             #   (hist[0][i]/totalR) is P of R
                P[1][i] = (hist[1][i] / totalG)
                P[2][i] = (hist[2][i] / totalB)
        return P

    def calcLut(self,input_p,target_p):
        lut = [[0] * 256, [0] * 256, [0] * 256]
        gj = [0,0,0]
        for gi in range(255):
            for i in range(3):
                while input_p[i][gi] > target_p[i][gj[i]] and gj[i]<255:  # pseudo code by slides
                    gj[i]+=1
                lut[i][gi] = gj[i]
        return lut

    def remap(self,image,lut):
        h,w = len(image),len(image[0])
        re_img = np.zeros([h, w, 4], np.float32)
        for i in range(h):
            for j in range(w):
                re_img[i][j][0] = np.float32(lut[0][int(image[i][j][0])] / 255.0)       # remap for R
                re_img[i][j][1] = np.float32(lut[1][int(image[i][j][1])] / 255.0)       # remap for G
                re_img[i][j][2] = np.float32(lut[2][int(image[i][j][2])] / 255.0)       # remap for B
                re_img[i][j][3] = np.float32(int(image[i][j][3]) / 255.0)               # remap for A
        return re_img

class PlotCanvas(FigureCanvas):
    def __init__(self, hist,color, width=5, height=50, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)

        FigureCanvas.updateGeometry(self)
        self.plotHistogram(hist,color)

    def plotHistogram(self, hist,color):
        self.axes.bar(np.arange(len(hist)),hist,1,color=color)  # variable 1 can be lower for higher resolutions display
        self.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
