from Client import Client
import pygame, sys
from Board import Board
from Pawns import Pawns
from constants import *
from typing import *
from GUI import GUI
import threading

class Game:
    
    def __init__(self, server_ip: str) -> None:
        pygame.init() # Initialize pygame
        
        # Network
        self.server_ip = server_ip
        self.client = Client(self.server_ip, 6000)
        self.receive_data: bool = True
        
        # Initialize the game
        self.GUI = GUI()
        
        self.board: Board = Board(BOARD_SIZE, BOARD_COLUMNS) # Initialize the checkers board
        self.player1: Pawns = Pawns(1, self.board.board) # Initialize pawns for player 1
        self.player2: Pawns = Pawns(2, self.board.board) # Initialize pawns for player 2
        
        #self.player1.get_pawn(self.player1.player_pawns, [6, "D"])[0]["pawn_type"] = "King"
        #self.player2.move_pawn(self.player2.get_pawn(self.player2.player_pawns, [3, "G"]), (4, "F"), self.player2.get_valid_moves(self.player2.get_pawn(self.player2.player_pawns, [3, "G"]), self.board), self.player1.player_pawns, self.board)
        
        #self.player2.take_pawn(self.player2.player_pawns, [0, "J"])
        #self.board.get_cell(self.board.board, (0, "J"))[0]["cell_owner"] = 0
        #self.board.get_cell(self.board.board, (0, "J"))[0]["cell_is_empty"] = True
        
        #self.player2.take_pawn(self.player2.player_pawns, [2, "H"])
        #self.board.get_cell(self.board.board, (2, "H"))[0]["cell_owner"] = 0
        #self.board.get_cell(self.board.board, (2, "H"))[0]["cell_is_empty"] = True
        
        #self.player2.take_pawn(self.player2.player_pawns, [1, "I"])
        #self.board.get_cell(self.board.board, (1, "I"))[0]["cell_owner"] = 0
        #self.board.get_cell(self.board.board, (1, "I"))[0]["cell_is_empty"] = True
        
        self.player_current_id: int = self.client.receive()
        print(self.player_current_id)
        
        self.turn: int = 0 # The turn of the game when turn%2 == 0, it's player 1's turn when turn%2 == 1, it's player 2's turn
        self.selected_pawn: tuple[dict, int] = None # Will contain the pawn that is currently selected
        self.reachable_cells_by_pawn: dict = None # Will contain the reachable cells by the pawn
    
    def window_update(self, window: pygame.Surface, color: tuple[int, int, int], clock: pygame.time.Clock, show_fps: bool) -> None:
        """_summary_: Update the window

        Args:
            window (pygame.Surface): The window to update
            color (tuple[int, int, int]): The color used to update the window
            clock (pygame.time.Clock): The clock used to get the framerate of the window
            show_fps (bool): If True, the framerate of the window will be print in the console
        """
        pygame.display.update()
        window.fill(color)
        print(clock.get_fps()) if show_fps else None
    
    def receive_data_network(self):
        while self.receive_data:
            data: tuple[int, list[dict], list[dict]] = self.client.receive()
            if data:
                self.turn = data[0]
                self.player1.player_pawns = data[1]
                self.player2.player_pawns = data[2]
                self.board.board = data[3]
    
    def gameloop(self) -> None:
        """_summary_: The main loop of the game

        """
        trame: int = 0 #ONLY FOR DEBUG
        receive_data_netw = threading.Thread(target=self.receive_data_network)
        receive_data_netw.start()
        game_running = True
        while game_running:
            
            mouse_position: tuple[int, int] = pygame.mouse.get_pos() # Get the current mouse position in a tuple (x, y)
            for event in pygame.event.get():
                """
                ################################################################################
                --------------------------------------TEST--------------------------------------
                This code will check when the user click on the window. 
                If his click is on a cell that contains a pawn, the reachable cells will be shown by a little circle over.
                """
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
                                            #print("\n", self.reachable_cells_by_pawn[(2, "H")], "\n", self.reachable_cells_by_pawn[(0, "J")], "\n")
                                        else:
                                            self.reachable_cells_by_pawn: dict = self.player2.get_valid_moves(self.selected_pawn, self.board)
                                            #print("\n", self.reachable_cells_by_pawn,"\n")
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
                                    data_to_send: tuple = (self.turn, self.player1.player_pawns, self.player2.player_pawns, self.board.board)
                                    self.client.send(data_to_send)
                                    trame+=1
                """
                -----------------------------------END TEST-------------------------------------
                ################################################################################
                """
                self.GUI.event_gui_close_game(event)
            
            self.GUI.draw_gui_board(WINDOW, self.board.board) # Draw the board
            self.GUI.draw_gui_pawns(WINDOW, self.player1.player_pawns) # Draw the pawns of player 1
            self.GUI.draw_gui_pawns(WINDOW, self.player2.player_pawns) # Draw the pawns of player 2
            self.GUI.draw_gui_reachable_cells(WINDOW, self.reachable_cells_by_pawn, self.selected_pawn, self.board) # Draw the reachable cells

            CLOCK.tick(FPS) # Set the framerate of the window
            self.window_update(WINDOW, BLACK, CLOCK, False) # Update the window