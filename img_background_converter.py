
from PyQt5.QtGui import (QImage, QPixmap)
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot)
import cv2

from QThreading import ThreadingAdapter

class ImgBackgroundConverter(ThreadingAdapter):

    imageReady = pyqtSignal(QPixmap)
    conversionType = 0
    width = 0
    height = 0

    def __init__(self):
        super().__init__()
    
    def convert(self, image_np, swidth, sheight, ctype=0):
        self.conversionType = ctype
        self.source = image_np
        self.width = swidth
        self.height = sheight
        self.start()

    #@pyqtSlot(np.ndarray, int, int)
    def fromNpToQPixmap(self):
        return cv2.cvtColor(self.source, cv2.COLOR_BGR2RGB)
    
    def fromGrayToQPixmap(self):
        return cv2.cvtColor(self.source, cv2.COLOR_GRAY2RGB)

    @pyqtSlot()
    def run(self):
        newimg = None
        if(self.conversionType==0):
            newimg = self.fromNpToQPixmap()
            
        if(self.conversionType==1):
            newimg = self.fromGrayToQPixmap()
            
        h, w, ch = newimg.shape
        convertedQImage = QImage(newimg, w, h, ch*w, QImage.Format_RGB888)
        
        self.imageReady.emit(QPixmap.fromImage(convertedQImage.scaled(self.width, self.height, Qt.IgnoreAspectRatio)))
        self.finished.emit()
