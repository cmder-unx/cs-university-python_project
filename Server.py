import socket, pickle, threading

class Server:
    
    def __init__(self, PORT, HEADER=16384):
        #-SERVER SETTINGS
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = PORT
        self.ADDR = (self.HOST, self.PORT)
        self.HEADER = HEADER
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = self.bind()
        self.clients_list = []
    
    def bind(self):
        try:
            self.server.bind(self.ADDR)
            print("SERVER CONFIGURATED")
        except:
            print("ERROR WHILE TRY TO CONFIGURATE THE SERVER")
    
    def manage_client(self, client_socket, addr):
        connected = True
        self.clients_list.append((client_socket, addr))
        print(f"{ addr } CONNECTED")
        print(f"Number of clients connected : { len(self.clients_list) }")
        while connected:
            try:
                data = pickle.loads(client_socket.recv(self.HEADER))
                reply = pickle.dumps(data)
                if not data:
                    self.clients_list.remove(self.clients_list[self.clients_list.index((client_socket, addr))])
                    print(f"Number of waiting clients connected : { len(self.clients_list) }")
                    print("DISCONNECTED")
                    break
                else:
                    print(f"Received : {data} from : {client_socket}")
                    for client in self.clients_list:
                        client[0].sendall(reply)
                        print(f"Sending : {reply} to : {client[0]}")
            except:
                self.clients_list.remove(self.clients_list[self.clients_list.index((client_socket, addr))])
                
                #-MESSAGES DISPLAY
                print("LOST CONNECTION")
                print("ERROR WHILE TRY TO MANAGED THE CLIENT")
                print(f"Number of clients connected : { len(self.clients_list) }")
                break
        client_socket.close()
    
    def server_manage(self):
        self.server.listen(2)
        while True:
            client_socket, addr = self.server.accept()
            print(f"{ addr } TRY TO CONNECT")
            thread = threading.Thread(target=self.manage_client, args=(client_socket, addr))
            thread.start()
    
    def start(self):
        print("RUNNING THE SERVER")
        print("[INFO] HOST : "+self.HOST+" PORT : "+str(self.PORT))
        
        running = True
        while running:
            self.server_manage()

Server(6000).start()