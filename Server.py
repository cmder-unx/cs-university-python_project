import socket, pickle, threading

class Server:
    
    def __init__(self, PORT: int, HEADER: int = 16384) -> None:
        #- Paramètres du serveur
        self.HOST: str = socket.gethostbyname(socket.gethostname())
        self.PORT: int = PORT
        self.ADDR: tuple[str, int] = (self.HOST, self.PORT)
        self.HEADER: int = HEADER
        self.server: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = self.bind()
        self.clients_list: list = []
    
    def bind(self) -> None:
        """_summary_: Attribution d'une IP et d'un port au serveur
        """        
        try:
            self.server.bind(self.ADDR)
            print("SERVER CONFIGURATED")
        except:
            print("ERROR WHILE TRY TO CONFIGURATE THE SERVER")
    
    def handle_client(self, client_socket: socket, addr: tuple[str, int]) -> None:
        """_summary_ : Traitement des données reçues par le client

        Args:
            client_socket (socket): Socket du client
            addr (tuple[str, int]): Adresse du client (IP, PORT)
        """        
        connected: bool = True
        client_id: int = len(self.clients_list)
        self.clients_list.append((client_id, client_socket, addr))
        client_socket.sendall(pickle.dumps((client_id, len(self.clients_list))))
        print(f"{addr} CONNECTED")
        print(f"Number of clients connected : {len(self.clients_list)}")
        for client in self.clients_list:
            if client[0] != client_id:
                client[1].sendall(pickle.dumps(len(self.clients_list)))
        while connected:
            try:
                data = pickle.loads(client_socket.recv(self.HEADER))
                reply = pickle.dumps(data)
                if not data:
                    self.clients_list.remove(self.clients_list[self.clients_list.index((client_id, client_socket, addr))])
                    print(f"Number of waiting clients connected : { len(self.clients_list) }")
                    print("DISCONNECTED")
                    break
                else:
                    print(f"Received data from : {client_socket}")
                    for client in self.clients_list:
                        client[1].sendall(reply)
                        print(f"Sending to : {client[1]}")
            except:
                self.clients_list.remove(self.clients_list[self.clients_list.index((client_id, client_socket, addr))])

                print("LOST CONNECTION")
                print("ERROR WHILE TRY TO MANAGED THE CLIENT")
                print(f"Number of clients connected : { len(self.clients_list) }")
                for client in self.clients_list:
                    client[1].sendall(pickle.dumps({"number_of_players_currently_connected" : len(self.clients_list)}))
                break
        client_socket.close()
    
    def server_handle_connection(self) -> None:
        """_summary_ : Traitement des connexions entrantes
        """        
        self.server.listen(2)
        while True:
            client_socket, addr = self.server.accept()
            print(f"{addr} TRY TO CONNECT")
            thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            thread.start()
    
    def start(self) -> None:
        """_summary_ : Démarrage du serveur
        """        
        print("RUNNING THE SERVER")
        print(f"[INFO] HOST : {self.HOST} PORT : {str(self.PORT)}")
        
        running = True
        while running:
            self.server_handle_connection()

if __name__ == "__main__":
    Server(6000).start()