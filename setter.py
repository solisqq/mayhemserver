from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

class Setter(QWidget):
    valueEdit : QLineEdit
    nameLabel : QLabel
    saveBtn : QPushButton

    changeAvailable = pyqtSignal(str,str)

    defVal : str

    def __init__(self, name : str, value : str,_parent : QWidget):
        QWidget.__init__(self, _parent)
        self.setLayout(QHBoxLayout())

        self.valueEdit = QLineEdit(text=value)
        self.defVal = value
        self.nameLabel = QLabel(text=name)
        self.saveBtn = QPushButton(text="set")

        self.layout().addWidget(self.nameLabel)
        self.layout().addWidget(self.valueEdit)
        self.layout().addWidget(self.saveBtn)

        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.saveBtn.clicked.connect(self.handleSave)

    @pyqtSlot()
    def handleSave(self):
        self.changeAvailable.emit(self.nameLabel.text(), self.valueEdit.text())