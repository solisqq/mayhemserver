class ServerThread(ThreadingAdapter):
    responses = []
    footer = 17496831 
    serv = None

    imgresp = ImgResponse()
    pongresp = PongResponse()

    def __init__(self):
        super().__init__()
        print("starting server...")   
        self.responses.append(self.imgresp)
        self.responses.append(self.pongresp)
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind(('', 4223))
        self.serv.listen(1)
        self.start()

    @pyqtSlot()
    def run(self):
        while True:
            conn, addr = self.serv.accept()
            try:
                print("1")
                overallData = bytearray()

                data = conn.recv(2096)
                overallData.extend(data)
                
                while int.from_bytes(data[len(data)-4:len(data)], byteorder=sys.byteorder)!=self.footer:
                    data = conn.recv(2048)
                    overallData.extend(data)
                    print("2")
                
                #print(overallData.hex())
                data = overallData
                byte = data[4]
                for resp in self.responses:
                    if(resp.cmd==byte):
                        #print(len(data))
                        #print(calcHash(data))
                        #print(data[5:len(data)-4])
                        resp.handleData(data[0:len(data)-4])
                        conn.sendall(resp.response)
                        #print(resp.response)
            finally:
                conn.close()
                print("3")
