from PyQt5.QtCore import (QObject, QThread, pyqtSignal, pyqtSlot)


class ThreadingAdapter(QObject):
    finished = pyqtSignal()
    objThread = None
    source = None

    def __init__(self):
        super().__init__()
        self.objThread = QThread()
        self.moveToThread(self.objThread)
        self.finished.connect(self.objThread.quit)
        self.objThread.started.connect(self.run)

    @pyqtSlot()
    def run(self):
        pass

    def start(self):
        self.objThread.start()

    def isRunning(self):
        return self.objThread.isRunning()

    def wait(self):
        self.objThread.wait()
