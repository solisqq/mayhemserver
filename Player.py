from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy
from PyQt5.QtCore import pyqtSlot
import Responses as rsp
from GameMode import game
import VideoLabel
from GunSettings import GSettings
from hclient import HClient

def printLong(self, buffor):
    count = 1
    if(len(buffor) > 1000):
        count = len(buffor)/1000
        count = int(count)+1
    else:
        print(buffor)
        return
    for i in range(0, count):
        print(buffor[i*1000:(i+1)*1000])


class GPlayer(QWidget):
    imgresp = rsp.ImgResponse()
    pongresp = rsp.PongResponse()
    textresp = rsp.TextResponse()
    responses = []

    client = None
    id = -1

    def __init__(self, socket, id):
        super().__init__()
        self.client = HClient(socket)
        self.client.requestRdy.connect(self.handleRequest)

        self.setupLayout()
        self.setID(id)

        self.responses.extend([self.pongresp, self.imgresp, self.textresp])
        self.imgresp.imgReady.connect(self.vlabel.setPicture)

    def setID(self, id):
        self.idLabel.setText("Player id: "+str(id))

    @pyqtSlot(bytearray)
    def handleRequest(self, request):
        cmd = request[0]
        for resp in self.responses:
            if(resp.cmd == cmd):
                resp.handleData(request)
                self.client.respond(resp)

    def setupLayout(self):
        self.setLayout(QVBoxLayout())
        self.setSizePolicy(
            QSizePolicy(
                QSizePolicy.MinimumExpanding,
                QSizePolicy.MinimumExpanding
            )
        )
        self.idLabel = QLabel()
        self.layout().addWidget(self.idLabel)
        self.vlabel = VideoLabel.VideoLabel(self)
        self.layout().addWidget(self.vlabel)
