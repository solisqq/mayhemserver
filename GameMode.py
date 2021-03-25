from PyQt5.QtCore import QObject


class TheGame(QObject):
    players = []
    playersLayout = None

    def __init__(self, _parent=None):
        super().__init__(_parent)

    def addPlayer(self, playerToAdd):
        if self.playersLayout is None:
            return
        for player in self.players:
            if(player.playerData.id == playerToAdd.playerData.id):
                print("reconnecting (id: "+str(player.playerData.id)+")...")
                player.reconnect(playerToAdd.sock)
                return
                #
                # playerToAdd.setPlayerData(player.playerData)
                # self.removePlayer(player)

        self.players.append(playerToAdd)
        self.playersLayout.addWidget(playerToAdd)

    def setMainLayout(self, layout):
        self.playersLayout = layout

    def removePlayer(self, playerToRemove):
        if self.playersLayout is None:
            return
        self.players.remove(playerToRemove)
        self.playersLayout.removeWidget(playerToRemove)

    def getLowestPlayerID(self):
        lowestId = 0
        for player in self.players:
            for player in self.players:
                if(player.playerData.id == lowestId):
                    lowestId = lowestId+1
        return lowestId


game = TheGame()
