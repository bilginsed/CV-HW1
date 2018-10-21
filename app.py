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
        self.left = 20
        self.top = 30
        self.width = 1500
        self.height = 700
        self.targetLoaded = False
        self.inputLoaded = False
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.box_style = "{ border: 1px solid grey}"
        # You can define other things in here
        self.initUI()

    def openInputImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.input_file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Png Images (*.png)", options=options)
        if self.input_file_name:
            self.load_input()

    def openTargetImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.target_file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Png Images (*.png)", options=options)
        if self.target_file_name:
            self.load_target()



    def initUI(self):
        # Write GUI initialization code
        self.setWindowTitle(self.title)

        open_input_act = QAction('&Open Input', self)
        open_input_act.triggered.connect(self.openInputImage)
        open_target_act = QAction('&Open Target', self)
        open_target_act.triggered.connect(self.openTargetImage)
        exit_act = QAction('&Exit', self)
        exit_act.triggered.connect(self.close)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(open_input_act)
        fileMenu.addAction(open_target_act)
        fileMenu.addAction(exit_act)

        top_lay = QVBoxLayout(self.central_widget)
        equalize_button = QPushButton("Equalize Histogram",self)
        equalize_button.setStyleSheet("Text-align:left")
        equalize_button.clicked.connect(self.histogramButtonClicked)
        equalize_button.move(100,70)
        top_lay.addWidget(equalize_button)

        lay = QHBoxLayout()
        top_lay.addLayout(lay)
        self.box_left = QGroupBox('Input')
        self.box_left.setStyleSheet(self.box_style)
        self.box_left.setFixedWidth(400)
        self.box_middle = QGroupBox('Target')
        self.box_middle.setStyleSheet(self.box_style)
        self.box_middle.setFixedWidth(400)
        self.box_right = QGroupBox('Result')
        self.box_right.setStyleSheet(self.box_style)
        self.box_right.setFixedWidth(400)

        lay.addWidget(self.box_left)
        lay.addWidget(self.box_middle)
        lay.addWidget(self.box_right)

        self.statusBar().showMessage('Ready')
        self.resize(self.width, self.height)
        self.show()

    def load_input(self):
        if not self.inputLoaded:
            lay = QVBoxLayout(self.box_left)

            label = QLabel(self)
            pixmap = QPixmap(self.input_file_name)
            label.setPixmap(pixmap.scaled(pixmap.width()/2,pixmap.height()/2,Qt.KeepAspectRatioByExpanding))
            self.input_img = mpimg.imread(self.input_file_name)* 255
            self.hist_input = self.calcHistogram(self.input_img)
            canvas_red = PlotCanvas(self.hist_input[0],color='r')
            canvas_green = PlotCanvas(self.hist_input[1],color='g')
            canvas_blue = PlotCanvas(self.hist_input[2],color='b')
            lay.addWidget(label,alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_red,alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_green,alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_blue,alignment=Qt.AlignHCenter)
            self.statusBar().showMessage('Load input')
            self.inputLoaded = True

    def load_target(self):
        if not self.targetLoaded:
            lay = QVBoxLayout(self.box_middle)
            label = QLabel(self)
            pixmap = QPixmap(self.target_file_name)
            label.setPixmap(pixmap.scaled(pixmap.width() / 2, pixmap.height() / 2, Qt.KeepAspectRatioByExpanding))
            self.target_img = mpimg.imread(self.target_file_name) * 255
            self.hist_target = self.calcHistogram(self.target_img)
            canvas_red = PlotCanvas(self.hist_target[0], color='r')
            canvas_green = PlotCanvas(self.hist_target[1], color='g')
            canvas_blue = PlotCanvas(self.hist_target[2], color='b')
            lay.addWidget(label, alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_red, alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_green, alignment=Qt.AlignHCenter)
            lay.addWidget(canvas_blue, alignment=Qt.AlignHCenter)
            self.statusBar().showMessage('Load target')
            self.targetLoaded = True

    def histogramButtonClicked(self):
        self.statusBar().showMessage('cal')
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
        else:
            try:
                input_p = self.calcP(self.hist_input)
                target_p = self.calcP(self.hist_target)
                lut = self.calcLut(input_p,target_p)
                remap_img = self.remap(self.input_img,lut)
                file_name = str(random.randint(100,500))+'.png'
                plt.imsave(file_name,remap_img)
                lay = QVBoxLayout(self.box_right)
                label = QLabel(self)
                pixmap = QPixmap(file_name)
                os.remove(file_name)
                label.setPixmap(pixmap.scaled(pixmap.width() / 2, pixmap.height() / 2, Qt.KeepAspectRatioByExpanding))
                hist = self.calcHistogram(remap_img*255)
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
    def __init__(self, hist,color, width=5, height=50, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)

        FigureCanvas.updateGeometry(self)
        self.plotHistogram(hist,color)

    def plotHistogram(self, hist,color):
        self.axes.bar(np.arange(len(hist)),hist,1,color=color)
        #self.axes.plot(hist,color=color)
        self.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
