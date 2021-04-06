import PyQt5
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from numpy import byte
from Responses import Response 
from setter import Setter


class GSettings(QWidget, Response):
    getSettingsBtn = None
    sock = None
    getSettingsArr = bytearray()
    reqSettings = pyqtSignal(bytearray)
    settingsContentWidget : QWidget
    def __init__(self, socket, _parent=None):
        QWidget.__init__(self, _parent)
        arr = bytearray()
        Response.__init__(self, 8)
        self.getSettingsArr.append(8)
        self.getSettingsArr.append(0)
        self.getSettingsArr.append(0)
        self.getSettingsArr.append(0)

        self.setLayout(QVBoxLayout())
        self.sock = socket
        self.getSettingsBtn = QPushButton("Get settings",self)
        self.layout().addWidget(self.getSettingsBtn)
        self.getSettingsBtn.clicked.connect(self.requestSettings)

        self.settingsContentWidget = QWidget()
        lay = QVBoxLayout()
        lay.setContentsMargins(0,0,0,0)
        lay.setSpacing(5)
        self.settingsContentWidget.setLayout(lay)
        self.layout().addWidget(self.settingsContentWidget)

    @pyqtSlot()
    def requestSettings(self):
        self.reqSettings.emit(self.getSettingsArr)

    @pyqtSlot(str,str)
    def requestChange(self, name : str, value : str):
        toSend = bytearray()
        toSend.append(9)
        toSend.extend(map(ord,str(name+"|"+value)))
        self.reqSettings.emit(toSend)

    def handleData(self, data : bytearray):
        text = data[1:len(data)-5].decode(encoding="utf-8", errors='ignore')
        splitted = text.split("|",)
        name = True
        currName = ""
        for i in reversed(range(self.settingsContentWidget.layout().count())): #clear layout from previous settings
            self.settingsContentWidget.layout().itemAt(i).widget().setParent(None)

        for item in splitted:
            if(len(item)>0):
                if(name):
                    name=False
                    currName = item
                else:
                    name = True
                    setter = Setter(currName, item, None)
                    self.settingsContentWidget.layout().addWidget(setter)
                    setter.changeAvailable.connect(self.requestChange)


        '''if(len(data)<6): return
        preparedData = data[1:len(data)-4]
        i=0
        id = 0
        values = []
        while(True):
            count = preparedData[i]-1
            if(i+count<len(preparedData)):
                i=i+1
                var_type = preparedData[i]
                if(var_type==7):
                    i=i+1
                    value = preparedData[i]
                    values.append([id, var_type, value])
                id = id+1
            i=i+1
            if i>=len(preparedData): break'''

        #print(values)
                    



    



