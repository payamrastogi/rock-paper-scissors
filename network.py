import socket
import pickle
from config import Config

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        config = Config()
        server = config.get_host()
        port = config.get_port()
        self.addr = (server, port)
        self.player = self.connect()

    def get_player(self):
        return self.player

    # the first time we connect to the server
    # we are getting the player number
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            # sending string data to the server
            self.client.send(str.encode(data))
            # receiving object data from the server
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)