import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.20.10.2"
        self.port = 5552
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode("utf-8")
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data, "utf-8"))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
