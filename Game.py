from Client import Client
import pygame, sys
from Board import Board
from Pawns import Pawns
from constants import *
from typing import *
import pickle
import threading

class Game:
    
    def __init__(self, server_ip: str) -> None:
        pygame.init() # Initialize pygame
        
        # Network
        self.server_ip = server_ip
        self.client = Client(self.server_ip, 6000)
        self.receive_data: bool = True
        
        # Initialize the game
        self.board: Board = Board(BOARD_SIZE, BOARD_COLUMNS) # Initialize the checkers board
        self.player1: Pawns = Pawns(1, self.board.board) # Initialize pawns for player 1
        self.player2: Pawns = Pawns(2, self.board.board) # Initialize pawns for player 2
        
        self.turn: int = 0 # The turn of the game when turn%2 == 0, it's player 1's turn when turn%2 == 1, it's player 2's turn
        self.selected_pawn: tuple[dict, int] = None # Will contain the pawn that is currently selected
        self.reachable_cells_by_pawn: list[tuple[dict, int]] = None # Will contain the reachable cells by the pawn
    
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
    
    def gameloop(self) -> None:
        """_summary_: The main loop of the game

        """
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
                    if self.turn%2 == 0: # Check if it's player 1's turn
                        for cell in self.board.board:
                            # For each cell in the board we check if the user click on it and if it contains a pawn
                            if cell["cell_gui"].collidepoint(mouse_position) and not cell["cell_is_empty"] and cell["cell_owner"] == 1:
                                # Get informations about the pawn that is currently on cell that the user clicked
                                self.selected_pawn: tuple[dict, int] = self.player1.get_pawn(self.player1.player_pawns, list(cell["cell_index"]))
                                if None not in self.selected_pawn: # If the pawn exists
                                    if self.selected_pawn[0]["pawn_status"] == "alive": # Check if the pawn is alive
                                        # Get the reachable cells by the pawn and store it in the variable reachable_cells_by_pawn 
                                        # that we initialized before to None
                                        self.reachable_cells_by_pawn: list[tuple[dict, int]] = self.player1.is_reachable(self.selected_pawn, self.board)
                                else:
                                    self.reachable_cells_by_pawn = None # If the pawn doesn't exist, the reachable cells will be reset
                            elif cell["cell_gui"].collidepoint(mouse_position) and cell["cell_owner"] != 1:
                                if self.reachable_cells_by_pawn != None:
                                    if self.board.get_cell(self.board.board, cell["cell_index"]) in self.reachable_cells_by_pawn:
                                        self.player1.move_pawn(self.player2.player_pawns, self.selected_pawn, cell["cell_index"], self.board)
                                        print(cell)
                                        self.reachable_cells_by_pawn = None
                                        self.selected_pawn = None
                                        self.turn+=1
                                        data_to_send = (self.turn, self.player1.player_pawns, self.player2.player_pawns)
                                        self.client.send(data_to_send)
                                        print(data_to_send)
                    else: # Check if it's player 2's turn
                        for cell in self.board.board:
                            # For each cell in the board we check if the user click on it and if it contains a pawn
                            if cell["cell_gui"].collidepoint(mouse_position) and not cell["cell_is_empty"] and cell["cell_owner"] == 2:
                                # Get informations about the pawn that is currently on cell that the user clicked
                                self.selected_pawn: tuple[dict, int] = self.player2.get_pawn(self.player2.player_pawns, list(cell["cell_index"]))
                                if None not in self.selected_pawn: # If the pawn exists
                                    if self.selected_pawn[0]["pawn_status"] == "alive": # Check if the pawn is alive
                                        # Get the reachable cells by the pawn and store it in the variable reachable_cells_by_pawn 
                                        # that we initialized before to None
                                        self.reachable_cells_by_pawn: list[tuple[dict, int]] = self.player2.is_reachable(self.selected_pawn, self.board)
                                else:
                                    self.reachable_cells_by_pawn = None # If the pawn doesn't exist, the reachable cells will be reset
                            elif cell["cell_gui"].collidepoint(mouse_position) and cell["cell_owner"] != 2:
                                if self.reachable_cells_by_pawn != None:
                                    if self.board.get_cell(self.board.board, cell["cell_index"]) in self.reachable_cells_by_pawn:
                                        self.player2.move_pawn(self.player1.player_pawns, self.selected_pawn, cell["cell_index"], self.board)
                                        print(cell)
                                        self.reachable_cells_by_pawn = None
                                        self.selected_pawn = None
                                        self.turn+=1
                                        data_to_send = (self.turn, self.player1.player_pawns, self.player2.player_pawns)
                                        self.client.send(data_to_send)
                """
                -----------------------------------END TEST-------------------------------------
                ################################################################################
                """
                if event.type == pygame.QUIT:
                    self.receive_data = False
                    pygame.quit()
                    sys.exit()
            
            self.board.draw_gui_board(WINDOW, self.board.board) # Draw the board
            self.player1.draw_gui_pawns(WINDOW, self.player1.player_pawns) # Draw the pawns of player 1
            self.player2.draw_gui_pawns(WINDOW, self.player2.player_pawns) # Draw the pawns of player 2
            
            """
            ################################################################################
            --------------------------------------TEST--------------------------------------
            If the reachable cells by the pawn is not None, we will draw a little circle over the reachable cells
            """
            #THIS IS CURRENTLY A TEST - SO IT WILL BE CLEANER LATER
            if self.reachable_cells_by_pawn:
                for reachable_cell in self.reachable_cells_by_pawn:
                    reachable_cell_gui_indicator_color: tuple[int, int, int] = GUI_PAWN_COLOR_1 if self.selected_pawn[0]["pawn_owner"] == 1 else GUI_PAWN_COLOR_2
                    reachable_cell_gui_indicator_position: tuple[int, int] = (reachable_cell[0]["cell_gui"].x+GUI_CELL_SIZE//2, reachable_cell[0]["cell_gui"].y+GUI_CELL_SIZE//2)
                    reachable_cell_gui_indicator_size: int = 10
                    #print(reachable_cell_gui_indicator_color)
                    pygame.draw.circle(WINDOW, reachable_cell_gui_indicator_color, reachable_cell_gui_indicator_position, reachable_cell_gui_indicator_size)
            """
            -----------------------------------END TEST-------------------------------------
            ################################################################################
            """
            
            CLOCK.tick(FPS) # Set the framerate of the window
            self.window_update(WINDOW, BLACK, CLOCK, False) # Update the window