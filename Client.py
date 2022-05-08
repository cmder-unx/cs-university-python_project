import socket, pickle
from typing import Any

class Client:
    
    def __init__(self, HOST, PORT, HEADER=16384) -> None:
        # - Paramètres du client
        self.HOST: str = HOST
        self.PORT: int = PORT
        self.ADDR: tuple[str, int] = (self.HOST, self.PORT)
        self.HEADER: int = HEADER
        self.client: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = self.connect()
    
    def connect(self) -> None:
        """_summary_: Connexion au serveur
        """        
        try:
            self.client.connect(self.ADDR)
        except socket.error as e:
            return "ERROR WHILE TRY TO CONNECT TO THE SERVER", e
    
    def send(self, data) -> str:
        """_summary_ : Envoie de données au serveur

        Args:
            data: Données à envoyer

        Returns:
            str: Message d'erreur en cas d'échec
        """        
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            return "ERROR WHILE TRYING TO SEND DATA", e
    
    def receive(self) -> Any:
        """_summary_: Réception de données du serveur

        Returns:
            Any: Données reçues
        """        
        try:
            data = pickle.loads(self.client.recv(self.HEADER))
            return data
        except socket.error as e:
            return "ERROR WHILE TRYING TO RECEIVE DATA", e