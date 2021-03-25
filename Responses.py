from PyQt5.QtCore import QObject, pyqtSignal
import cv2
import numpy as np


class Response(QObject):
    cmd = 0
    response = bytearray()

    def __init__(self, cmd, response):
        super().__init__()
        self.cmd = cmd
        self.response = response
        self.response.insert(0, cmd)

    def handleData(self, data):
        pass

    def addBytesToByteArray(self, arraytoaddbytes, howmuch, byte):
        for i in range(0, howmuch):
            arraytoaddbytes.append(byte)

    def calcHash(self, data):
        finall = 0
        for char in data:
            if finall > 0:
                finall = finall-char
            else:
                finall = finall+char

        return finall


class ImgResponse(Response):

    splitter = bytearray()
    imgReady = pyqtSignal(np.ndarray)

    def __init__(self):
        resp = bytearray()
        self.addBytesToByteArray(resp, 7, 0xFF)
        super().__init__(0xFF, resp)
        self.splitter.append(0xFF)
        self.splitter.append(0x0B)
        self.splitter.append(0xFB)
        self.splitter.append(0x0A)

    def handleData(self, data):
        try:
            # imgInBytes = data[11:len(data)]
            decoded = cv2.imdecode(np.frombuffer(data, np.uint8), -1)
            self.imgReady.emit(decoded)
            cv2.imwrite("imgs/test.jpg", decoded)
        except Exception:
            print("Corrupted data")
        #print(data[0:len(data)])
        #print(data[len(data)-100:len(data)])


class PongResponse(Response):
    def __init__(self):
        resp = bytearray()
        self.addBytesToByteArray(resp, 7, 0x00)
        super().__init__(0, resp)

    def handleData(self, data):
        pass


class TextResponse(Response):
    def __init__(self):
        resp = bytearray()
        self.addBytesToByteArray(resp, 7, 0x00)
        super().__init__(2, resp)

    def handleData(self, data):
        pass
        # print(data[5:len(data)])


'''splitted = data.split(self.splitter)
        invalid_frames = []
        print(splitted)
        for segment in splitted:
            if(len(segment)>15):
                recv_hash = segment[5]
                calc_hash = calcHash(segment[11:len(segment)])
                if(recv_hash!=abs(calc_hash)):
                    invalid_frames.append(segment[9])

        imgInBytes = bytearray()
        if(len(invalid_frames)==0 and len(splitted)>1):
            for segment in splitted:
                imgInBytes.extend(segment[11:len(segment)])

            decoded = cv2.imdecode(np.frombuffer(imgInBytes, np.uint8),-1)
            self.imgReady.emit(decoded)
        else:
            print("zgubiono dane")
            print(invalid_frames)'''
'''
respond:
0x01        0xFF                0x01
cmd id      packet info         packet id
img         error               2-nd packet error


received:
depends on cmd (5 byte)
0xFF,   0xFA,   0x0A,   0x01,   0x01,   0x00, 0x00, 0x00, 0x00,     0x00,                0xFF,   0xFA,   0x0A,   0x01
            header              cmd     4byte hash                  data (optional)                 footer

img frame:
0xFF,   0xFA,   0x0A,   0x01,   0x01,   0x00, 0x00, 0x00, 0x00,     0x00,           0x05,                  0xFF,   0xFA,   0x0A,   0x01
            header              cmd     4byte hash                  segment id      of totall segments                 footer
'''
