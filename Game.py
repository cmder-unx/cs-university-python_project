from Client import Client
import pygame
from Board import Board
from Pawns import Pawns
from constants import *
from typing import *
from GUI import GUI
import threading

class Game:
    
    def __init__(self, server_ip: str, game_pid: int) -> None:
        pygame.init()
        
        # PID du jeu
        self.game_pid: int = game_pid
        
        # Réseau
        self.server_ip: str = server_ip
        self.client: Client = Client(self.server_ip, 6000)
        self.receive_data: bool = True
        
        # GUI
        self.GUI: GUI = GUI()
        
        # Initialisation du plateau et des pions des joueurs
        self.board: Board = Board(BOARD_SIZE, BOARD_COLUMNS)
        self.player1: Pawns = Pawns(1, self.board.board)
        self.player2: Pawns = Pawns(2, self.board.board)

        # Identifiant du joueur vainqueur
        self.winner_id: int = None
        
        # Récupération de l'identifiant du joueur, et du nombre de joueurs connectés sur le serveur
        self.player_current_id, self.number_of_players_currently_connected = self.client.receive()
        
        # Si le joueur est le premier à se connecter, il doit attendre le second joueur
        if self.number_of_players_currently_connected == 1:
            self.waiting_for_player2()
        
        self.turn: int = 0
        self.selected_pawn: tuple[dict, int] = None
        self.reachable_cells_by_pawn: dict = None 
    
    def receive_data_network(self) -> None:
        """_summary_: Réception des données du jeu du serveur
        """        
        while self.receive_data:
            data: dict = self.client.receive()
            if data:
                if len(data) > 1:
                    self.turn = data["turn"]
                    self.player1.player_pawns = data["player1_pawns"]
                    self.player2.player_pawns = data["player2_pawns"]
                    self.board.board = data["board"]
                elif len(data) == 1:
                    self.number_of_players_currently_connected: int = data["number_of_players_currently_connected"]
    
    def receive_data_clients_list(self) -> None:
        """_summary_ : Réception du nombre de clients connectés sur le serveur
        """        
        while True:
            data: int = self.client.receive()
            if data == 2:
                self.number_of_players_currently_connected: int = 2
                break
    
    def waiting_for_player2(self) -> None:
        """_summary_ : Attente du second joueur
        """
        # Création d'un thread pour récupérer le nombre de clients connectés au serveur en parallèle du message d'attente
        receive_data_clients_list: threading.Thread = threading.Thread(target=self.receive_data_clients_list)
        receive_data_clients_list.start()
        while True:
            pygame.display.set_caption(f"{GAME_NAME} - En attente du joueur 2") # Set the window title
            
            for event in pygame.event.get():
                self.GUI.event_gui_close_game(event, self.game_pid)
            
            
            self.GUI.gui_label(WINDOW, WAITING_FOR_PLAYER2_LABEL, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), None, 35, BLACK)
            
            if self.number_of_players_currently_connected == 2:
                break
            
            CLOCK.tick(FPS)
            self.GUI.gui_window_update(WINDOW, WHITE, CLOCK, False)
        receive_data_clients_list.join()
    
    def winner_check(self) -> int:
        """_summary_: Vérifie si un joueur a gagné

        Returns:
            int: Identifiant du joueur gagnant
        """        
        winner_id: int = None
        dead_pawns_player1: int = 0
        dead_pawns_player2: int = 0
        for pawn1, pawn2 in zip(self.player1.player_pawns, self.player2.player_pawns):
            if pawn1["pawn_status"] == "dead":
                dead_pawns_player1 += 1
            if pawn2["pawn_status"] == "dead":
                dead_pawns_player2 += 1
        if dead_pawns_player1 == len(self.player1.player_pawns):
            winner_id: int = 1
        elif dead_pawns_player2 == len(self.player2.player_pawns):
            winner_id: int = 0
        return winner_id
    
    def gameloop(self) -> None:
        """_summary_: Boucle de jeu
        """
        # Création d'un thread pour récupérer les données du jeu du serveur en parallèle de la boucle de jeu
        receive_data_netw: threading.Thread = threading.Thread(target=self.receive_data_network)
        receive_data_netw.start()
        game_running = True
        while game_running:
            
            # Met à jour le titre de la fenêtre
            pygame.display.set_caption(f"{GAME_NAME} - Joueur {self.player_current_id+1} - Tour n° {self.turn}")
            
            # Récupération des coordonnées de la souris
            mouse_position: tuple[int, int] = pygame.mouse.get_pos()
            
            # Récupération des évènements
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.turn%2 == self.player_current_id:
                        for cell in self.board.board:
                            if cell["cell_gui"].collidepoint(mouse_position) and not cell["cell_is_empty"] and cell["cell_owner"] == self.player_current_id+1:
                                
                                # Récupération du pion sélectionné
                                if self.player_current_id == 0:
                                    self.selected_pawn: tuple[dict, int] = self.player1.get_pawn(self.player1.player_pawns, list(cell["cell_index"]))
                                else:
                                    self.selected_pawn: tuple[dict, int] = self.player2.get_pawn(self.player2.player_pawns, list(cell["cell_index"]))
                                
                                # Récupération des cases accessibles par le pion sélectionné
                                if None not in self.selected_pawn:
                                    if self.selected_pawn[0]["pawn_status"] == "alive":
                                        if self.player_current_id == 0:
                                            self.reachable_cells_by_pawn: dict = self.player1.get_valid_moves(self.selected_pawn, self.board)
                                        else:
                                            self.reachable_cells_by_pawn: dict = self.player2.get_valid_moves(self.selected_pawn, self.board)
                                else:
                                    self.reachable_cells_by_pawn = None
                            
                            # Si le joueur clique sur une case qui appartient à l'adversaire
                            elif cell["cell_gui"].collidepoint(mouse_position) and cell["cell_owner"] != self.player_current_id+1:
                                
                                # Bouge le pion sélectionné sur la case cliquée
                                if self.reachable_cells_by_pawn != None:
                                    if self.player_current_id == 0:
                                        flag: bool = self.player1.move_pawn(self.selected_pawn, cell["cell_index"], self.reachable_cells_by_pawn, self.player2.player_pawns, self.board)
                                    else:
                                        flag: bool = self.player2.move_pawn(self.selected_pawn, cell["cell_index"], self.reachable_cells_by_pawn, self.player1.player_pawns, self.board)
                                    
                                    # Réinitialise à None la variable qui contient les cases accessible ainsi que la variable qui contient le pion sélectionné
                                    self.reachable_cells_by_pawn: dict = None
                                    self.selected_pawn: tuple[dict, int] = None
                                    
                                    # Si le pion a bougé on passe au tour suivant et on envois les données au serveur
                                    if flag:
                                        self.turn+=1
                                        data_to_send: dict = {"turn" : self.turn, "player1_pawns" : self.player1.player_pawns, "player2_pawns" : self.player2.player_pawns, "board" : self.board.board}
                                        self.client.send(data_to_send)
                self.GUI.event_gui_close_game(event, self.game_pid)
            
            self.GUI.draw_gui_board(WINDOW, self.board.board)
            self.GUI.draw_gui_pawns(WINDOW, self.player1.player_pawns)
            self.GUI.draw_gui_pawns(WINDOW, self.player2.player_pawns)
            self.GUI.draw_gui_reachable_cells(WINDOW, self.reachable_cells_by_pawn, self.selected_pawn, self.board)

            self.winner_id: int = self.winner_check()

            CLOCK.tick(FPS)
            self.GUI.gui_window_update(WINDOW, BLACK, CLOCK, False)
            
            if self.number_of_players_currently_connected == 1 or self.winner_id is not None:
                game_running = False
        
        if self.number_of_players_currently_connected == 1:
            self.GUI.gui_player_has_left_screen(self.game_pid)
        elif self.winner_id is not None:
            if self.winner_id != self.player_current_id:
                self.GUI.gui_winner_screen(f"Le joueur {self.winner_id+1} a gagné !", self.game_pid)
            else:
                self.GUI.gui_winner_screen(f"Tu as gagné !", self.game_pid)
        