import socket, pickle

class Client:
    
    def __init__(self, HOST, PORT, HEADER=16384):
        self.HOST = HOST
        self.PORT = PORT
        self.ADDR = (self.HOST, self.PORT)
        self.HEADER = HEADER
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = self.connect()
    
    def connect(self):
        try:
            self.client.connect(self.ADDR)
        except socket.error as e:
            return "ERROR WHILE TRY TO CONNECT TO THE SERVER", e
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            return "ERROR WHILE TRYING TO SEND DATA", e
    
    def receive(self):
        try:
            data = pickle.loads(self.client.recv(self.HEADER))
            return data
        except socket.error as e:
            return "ERROR WHILE TRYING TO RECEIVE DATA", e