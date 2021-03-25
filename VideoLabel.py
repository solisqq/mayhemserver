from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import (Qt, pyqtSlot)
import numpy as np
import cv2


class VideoLabel(QWidget):
    videoLabel = None

    def __init__(self, _parent):
        super(VideoLabel, self).__init__(_parent)
        self.setLayout(QVBoxLayout())
        self.videoLabel = QLabel(text="")
        self.videoLabel.setSizePolicy(
            QSizePolicy(
                QSizePolicy.MinimumExpanding,
                QSizePolicy.MinimumExpanding
            )
        )
        self.layout().addWidget(self.videoLabel)

    def closeEvent(self, event):
        event.accept()

    @pyqtSlot(np.ndarray)
    def setPicture(self, picture):
        newimg = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)
        h, w, ch = newimg.shape
        convertedQImage = QImage(newimg, w, h, ch*w, QImage.Format_RGB888)
        self.videoLabel.setPixmap(
            QPixmap.fromImage(
                convertedQImage.scaled(320, 240, Qt.IgnoreAspectRatio)
            )
        )


class NullWriter(object):
    def write(self, arg):
        pass
