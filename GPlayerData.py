from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class GPlayerData(QObject):
    health = 100
    ammo = 200
    magazine = 11
    kills = []
    id = -1

    playerDied = pyqtSignal()
    outOfAmmo = pyqtSignal()
    gunReady = pyqtSignal()

    def __init__(self, _parent):
        super().__init__(_parent)
        # self.id = game.

    @pyqtSlot(int)
    def receiveDmg(self, dmg):
        self.health = self.health-dmg
        if(self.health <= 0):
            self.playerDied.emit()

    @pyqtSlot(int)
    def shot(self):
        self.magazine = self.magazine-1
        if(self.magazine <= 0):
            self.outOfAmmo.emit()
