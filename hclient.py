from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtNetwork import QTcpSocket
import Responses as rsp
from GameMode import game
import VideoLabel
from GPlayerData import GPlayerData
from GunSettings import GSettings


def printLong(buffor):
    count = 1
    if(len(buffor) > 1000):
        count = len(buffor)/1000
        count = int(count)+1
    else:
        print(buffor)
        return
    for i in range(0, count):
        print(buffor[i*1000:(i+1)*1000])

class HClient(QWidget):
    sock = None
    buffor = bytearray()
    requestRdy = pyqtSignal(bytearray)

    def __init__(self, socket):
        super().__init__()
        self.attachSock(socket)

    def attachSock(self,socket):
        if self.sock is None:
            print("connected")
        else:
            self.sock.close()
            print("reconnected")

        self.sock = socket
        self.sock.readyRead.connect(self.handleData)
        self.sock.disconnected.connect(self.handleDisconnect)

    @pyqtSlot()
    def handleDisconnect(self):
        print("disconnected")

    def respond(self, responseObject):
        if(len(responseObject.response)>0):
            # print(responseObject.response)
            self.sock.write(responseObject.response)

    @pyqtSlot(bytearray)
    def sendData(self, data):
        # print(data)
        self.sock.write(data)

    @pyqtSlot()
    def handleData(self):
        self.sock.waitForReadyRead(10)
        self.buffor.extend(self.sock.readAll())
        if len(self.buffor)<4: return

        end = self.buffor[len(self.buffor)-4:len(self.buffor)]
        if end == b"\xff\xfa\n\x01":
            self.requestRdy.emit(self.buffor)
            # printLong(self.buffor)
            # print(self.buffor)
            self.buffor.clear()
