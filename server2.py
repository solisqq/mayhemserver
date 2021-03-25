from PyQt5.QtCore import pyqtSlot
from PyQt5.QtNetwork import QTcpServer
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from Player import GPlayer

class QTServerThread(QWidget):
    server = None
    players = []

    def __init__(self, _parent):
        super().__init__(_parent)
        self.setLayout(QHBoxLayout())
        self.server = QTcpServer(self)
        if self.server.listen(port=4223) is False:
            print("Error starting the server!")
            return
        self.server.newConnection.connect(self.handleNewConnection)

    def getIDFromSocket(self, socket):
        ipadd = socket.peerAddress().toString()
        splited = ipadd.split(".")
        return int(splited[len(splited)-1])

    @pyqtSlot()
    def handleNewConnection(self):
        newSock = self.server.nextPendingConnection()
        if(newSock is not None):
            newID = self.getIDFromSocket(newSock)
            for player in self.players:
                if self.getIDFromSocket(player.client.sock) == newID:
                    player.client.attachSock(newSock)
                    return

            newPlayer = GPlayer(newSock, newID)
            self.players.append(newPlayer)
            self.layout().addWidget(newPlayer)
