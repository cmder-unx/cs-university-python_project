from Client import Client
import pygame, sys
from Board import Board
from Pawns import Pawns
from constants import *
from typing import *
from GUI import GUI
import threading

class Game:
    
    def __init__(self, server_ip: str, game_pid: int) -> None:
        pygame.init() # Initialize pygame
        
        self.game_pid: int = game_pid
        
        # Network
        self.server_ip = server_ip
        self.client = Client(self.server_ip, 6000)
        self.receive_data: bool = True
        
        # Initialize the game
        self.GUI = GUI()
        
        self.board: Board = Board(BOARD_SIZE, BOARD_COLUMNS) # Initialize the checkers board
        self.player1: Pawns = Pawns(1, self.board.board) # Initialize pawns for player 1
        self.player2: Pawns = Pawns(2, self.board.board) # Initialize pawns for player 2

        self.winner_id: int = None
        
        self.player_current_id, self.number_of_players_currently_connected = self.client.receive() # Receive the current player id and the number of players currently connected
        
        if self.number_of_players_currently_connected == 1:
            self.waiting_for_player2()
        
        self.turn: int = 0 # The turn of the game when turn%2 == 0, it's player 1's turn when turn%2 == 1, it's player 2's turn
        self.selected_pawn: tuple[dict, int] = None # Will contain the pawn that is currently selected
        self.reachable_cells_by_pawn: dict = None # Will contain the reachable cells by the pawn
    
    def receive_data_network(self):
        while self.receive_data:
            data: dict = self.client.receive()
            if data:
                if len(data) > 1:
                    self.turn = data["turn"]
                    self.player1.player_pawns = data["player1_pawns"]
                    self.player2.player_pawns = data["player2_pawns"]
                    self.board.board = data["board"]
                elif len(data) == 1:
                    self.number_of_players_currently_connected = data["number_of_players_currently_connected"]
    
    def receive_data_clients_list(self) -> None:
        while True:
            data: int = self.client.receive()
            if data == 2:
                self.number_of_players_currently_connected = 2
                break
    
    def waiting_for_player2(self):
        receive_data_clients_list = threading.Thread(target=self.receive_data_clients_list)
        receive_data_clients_list.start()
        while True:
            pygame.display.set_caption(f"{GAME_NAME} - Waiting for player 2 to connect") # Set the window title
            
            for event in pygame.event.get():
                self.GUI.event_gui_close_game(event, self.game_pid)
            
            label: str = "Waiting for player 2 to connect"
            self.GUI.gui_label(WINDOW, label, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-125), None, 45, WHITE)
            
            if self.number_of_players_currently_connected == 2:
                break
            
            CLOCK.tick(FPS) # Set the framerate of the window
            self.GUI.window_update(WINDOW, BLACK, CLOCK, False) # Update the window
        receive_data_clients_list.join()
    
    def winner_check(self) -> int:
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
        """_summary_: The main loop of the game

        """
        trame: int = 0 #ONLY FOR DEBUG
        receive_data_netw = threading.Thread(target=self.receive_data_network)
        receive_data_netw.start()
        game_running = True
        while game_running:
            pygame.display.set_caption(f"{GAME_NAME} - Player {self.player_current_id+1} - Turn {self.turn}") # Set the window title
            mouse_position: tuple[int, int] = pygame.mouse.get_pos() # Get the current mouse position in a tuple (x, y)
            for event in pygame.event.get():
                #THIS IS CURRENTLY A TEST - SO IT WILL BE CLEANER LATER
                if event.type == pygame.MOUSEBUTTONDOWN: # Check if the user click on the window
                    if self.turn%2 == self.player_current_id: # Check if it's player 1's turn
                        for cell in self.board.board:
                            # For each cell in the board we check if the user click on it and if it contains a pawn
                            if cell["cell_gui"].collidepoint(mouse_position) and not cell["cell_is_empty"] and cell["cell_owner"] == self.player_current_id+1:
                                # Get informations about the pawn that is currently on cell that the user clicked
                                if self.player_current_id == 0:
                                    self.selected_pawn: tuple[dict, int] = self.player1.get_pawn(self.player1.player_pawns, list(cell["cell_index"]))
                                else:
                                    self.selected_pawn: tuple[dict, int] = self.player2.get_pawn(self.player2.player_pawns, list(cell["cell_index"]))
                                
                                if None not in self.selected_pawn: # If the pawn exists
                                    if self.selected_pawn[0]["pawn_status"] == "alive": # Check if the pawn is alive
                                        # Get the reachable cells by the pawn and store it in the variable reachable_cells_by_pawn 
                                        # that we initialized before to None
                                        if self.player_current_id == 0:
                                            self.reachable_cells_by_pawn: dict = self.player1.get_valid_moves(self.selected_pawn, self.board)
                                            print("\n", self.reachable_cells_by_pawn, "\n")
                                        else:
                                            self.reachable_cells_by_pawn: dict = self.player2.get_valid_moves(self.selected_pawn, self.board)
                                            print("\n", self.reachable_cells_by_pawn,"\n")
                                else:
                                    self.reachable_cells_by_pawn = None # If the pawn doesn't exist, the reachable cells will be reset
                            elif cell["cell_gui"].collidepoint(mouse_position) and cell["cell_owner"] != self.player_current_id+1:
                                if self.reachable_cells_by_pawn != None:
                                    if self.player_current_id == 0:
                                        self.player1.move_pawn(self.selected_pawn, cell["cell_index"], self.reachable_cells_by_pawn, self.player2.player_pawns, self.board)
                                    else:
                                        self.player2.move_pawn(self.selected_pawn, cell["cell_index"], self.reachable_cells_by_pawn, self.player1.player_pawns, self.board)
                                    self.reachable_cells_by_pawn: dict = None
                                    self.selected_pawn: tuple[dict, int] = None
                                    self.turn+=1
                                    data_to_send: dict = {"turn" : self.turn, "player1_pawns" : self.player1.player_pawns, "player2_pawns" : self.player2.player_pawns, "board" : self.board.board}
                                    self.client.send(data_to_send)
                                    trame+=1
                self.GUI.event_gui_close_game(event, self.game_pid)
            
            self.GUI.draw_gui_board(WINDOW, self.board.board) # Draw the board
            self.GUI.draw_gui_pawns(WINDOW, self.player1.player_pawns) # Draw the pawns of player 1
            self.GUI.draw_gui_pawns(WINDOW, self.player2.player_pawns) # Draw the pawns of player 2
            self.GUI.draw_gui_reachable_cells(WINDOW, self.reachable_cells_by_pawn, self.selected_pawn, self.board) # Draw the reachable cells

            self.winner_id: int = self.winner_check() # Check if there is a winner

            CLOCK.tick(FPS) # Set the framerate of the window
            self.GUI.window_update(WINDOW, BLACK, CLOCK, False) # Update the window
            
            if self.number_of_players_currently_connected == 1:
                game_running = False
            elif self.winner_id is not None:
                game_running = False
        
        if self.number_of_players_currently_connected == 1:
            self.GUI.gui_player_has_left_screen(self.game_pid)
        elif self.winner_id is not None:
            if self.winner_id != self.player_current_id:
                self.GUI.gui_winner_screen(f"Player {self.winner_id+1}", self.game_pid)
            else:
                self.GUI.gui_winner_screen(f"You", self.game_pid)
        