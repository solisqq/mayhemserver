from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy
from PyQt5.QtCore import pyqtSlot
import Responses as rsp
from GameMode import game
import VideoLabel
from GunSettings import GSettings
from hclient import HClient


class GPlayer(QWidget):
    imgresp = rsp.ImgResponse()
    pongresp = rsp.PongResponse()
    textresp = rsp.TextResponse()
    settings = None
    responses = []

    client = None
    id = -1

    def __init__(self, socket, id):
        super().__init__()
        self.client = HClient(socket)
        self.client.requestRdy.connect(self.handleRequest)
        self.setupLayout()
        self.setID(id)

        self.responses.extend([self.pongresp, self.imgresp, self.textresp, self.settings])
        self.imgresp.imgReady.connect(self.vlabel.setPicture)

    def setID(self, id):
        self.idLabel.setText("Player id: "+str(id))

    @pyqtSlot(bytearray)
    def handleRequest(self, request):
        cmd = request[0]
        for resp in self.responses:
            if(resp.cmd == cmd):
                self.client.respond(resp)
                resp.handleData(request)

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
        self.settings = GSettings(self.client.sock)
        self.settings.reqSettings.connect(self.client.sendData)
        self.layout().addWidget(self.settings)
