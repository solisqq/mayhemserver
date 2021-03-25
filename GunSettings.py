import PyQt5
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSlot


class GSettings(QWidget):
    getSettingsBtn = None
    sock = None
    getSettingsArr = bytearray()
    def __init__(self, socket, _parent):
        super().__init__(_parent)
        self.getSettingsArr.append(8)
        self.getSettingsArr.append(0)
        self.getSettingsArr.append(0)
        self.getSettingsArr.append(0)

        self.setLayout(QVBoxLayout())
        self.sock = socket
        self.getSettingsBtn = QPushButton("Get settings",self)
        self.layout().addWidget(self.getSettingsBtn)

        self.getSettingsBtn.clicked.connect(self.requestSettings)

    @pyqtSlot()
    def requestSettings(self):
        self.sock.write(self.getSettingsArr)

    



