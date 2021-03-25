import sys
import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
import server2
from GameMode import game
# import tensorflow as tf
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# physical_devices = tf.config.list_physical_devices('GPU')
# if(len(physical_devices)>0):
#     tf.config.experimental.set_memory_growth(physical_devices[0], True)


class Ui(QMainWindow):
    videoLabel = None
    serverThread = None

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('MainWindow.ui', self)  # Load the .ui file
        self.serverThread = server2.QTServerThread(self)
        self.centralWidget().layout().addWidget(self.serverThread)
        # self.serverThread.imgresp.imgReady.connect(self.videoLabel.setPicture)

    def closeEvent(self, event):
        event.accept()


class NullWriter(object):
    def write(self, arg):
        pass


if __name__ == "__main__":
    app = QApplication([])
    window = Ui()
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    window.show()
    # print(int(window.winId()))
    sys.stdout.flush()
    sys.exit(app.exec_())
