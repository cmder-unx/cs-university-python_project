# DEPENDENCIES
import pygame, sys
from Board import Board
from Pawns import Pawns
from constants import *
from typing import *

pygame.init() # Initialize pygame

def window_update(window: pygame.Surface, color: tuple[int, int, int], clock: pygame.time.Clock, show_fps: bool) -> None:
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

board: Board = Board(BOARD_SIZE, BOARD_COLUMNS) # Initialize the checkers board
player1: list[dict] = Pawns(1, board.board) # Initialize pawns for player 1
player2: list[dict] = Pawns(2, board.board) # Initialize pawns for player 2

# Get informations about the pawn that is currently on cell at the index [6, "B"]
get_a_pawn_informations: tuple[dict, int] = player1.get_pawn(player1.player_pawns, [6, "B"]) 

def main() -> None:
    turn:int = 0 # The turn of the game when turn%2 == 0, it's player 1's turn when turn%2 == 1, it's player 2's turn
    game_running = True
    selected_pawn: tuple[dict, int] = None # Will contain the pawn that is currently selected
    reachable_cells_by_pawn: list[tuple[dict, int]] = None # Will contain the reachable cells by the pawn
    while game_running:
        print(turn)
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
                if turn%2 == 0: # Check if it's player 1's turn
                    for cell in board.board:
                        # For each cell in the board we check if the user click on it and if it contains a pawn
                        if cell["cell_gui"].collidepoint(mouse_position) and not cell["cell_is_empty"] and cell["cell_owner"] == 1:
                            # Get informations about the pawn that is currently on cell that the user clicked
                            selected_pawn: tuple[dict, int] = player1.get_pawn(player1.player_pawns, list(cell["cell_index"]))
                            if None not in selected_pawn: # If the pawn exists
                                if selected_pawn[0]["pawn_status"] == "alive": # Check if the pawn is alive
                                    # Get the reachable cells by the pawn and store it in the variable reachable_cells_by_pawn 
                                    # that we initialized before to None
                                    reachable_cells_by_pawn: list[tuple[dict, int]] = player1.is_reachable(selected_pawn, board)
                            else:
                                reachable_cells_by_pawn = None # If the pawn doesn't exist, the reachable cells will be reset
                        elif cell["cell_gui"].collidepoint(mouse_position) and cell["cell_is_empty"]:
                            if reachable_cells_by_pawn != None:
                                if board.get_cell(board.board, cell["cell_index"]) in reachable_cells_by_pawn:
                                    player1.move_pawn(player1.player_pawns, selected_pawn, cell["cell_index"], board)
                                    reachable_cells_by_pawn = None
                                    selected_pawn = None
                                    turn+=1
                else: # Check if it's player 2's turn
                    for cell in board.board:
                        # For each cell in the board we check if the user click on it and if it contains a pawn
                        if cell["cell_gui"].collidepoint(mouse_position) and not cell["cell_is_empty"] and cell["cell_owner"] == 2:
                            # Get informations about the pawn that is currently on cell that the user clicked
                            selected_pawn: tuple[dict, int] = player2.get_pawn(player2.player_pawns, list(cell["cell_index"]))
                            if None not in selected_pawn: # If the pawn exists
                                if selected_pawn[0]["pawn_status"] == "alive": # Check if the pawn is alive
                                    # Get the reachable cells by the pawn and store it in the variable reachable_cells_by_pawn 
                                    # that we initialized before to None
                                    reachable_cells_by_pawn: list[tuple[dict, int]] = player2.is_reachable(selected_pawn, board)
                            else:
                                reachable_cells_by_pawn = None # If the pawn doesn't exist, the reachable cells will be reset
                        elif cell["cell_gui"].collidepoint(mouse_position) and cell["cell_is_empty"]:
                            if reachable_cells_by_pawn != None:
                                if board.get_cell(board.board, cell["cell_index"]) in reachable_cells_by_pawn:
                                    player2.move_pawn(player2.player_pawns, selected_pawn, cell["cell_index"], board)
                                    reachable_cells_by_pawn = None
                                    selected_pawn = None
                                    turn+=1
            """
            -----------------------------------END TEST-------------------------------------
            ################################################################################
            """
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        board.draw_gui_board(WINDOW, board.board) # Draw the board
        player1.draw_gui_pawns(WINDOW, player1.player_pawns) # Draw the pawns of player 1
        player2.draw_gui_pawns(WINDOW, player2.player_pawns) # Draw the pawns of player 2
        
        """
        ################################################################################
        --------------------------------------TEST--------------------------------------
        If the reachable cells by the pawn is not None, we will draw a little circle over the reachable cells
        """
        #THIS IS CURRENTLY A TEST - SO IT WILL BE CLEANER LATER
        if reachable_cells_by_pawn:
            for reachable_cell in reachable_cells_by_pawn:
                reachable_cell_gui_indicator_color: tuple[int, int, int] = GUI_PAWN_COLOR_1 if selected_pawn[0]["pawn_owner"] == 1 else GUI_PAWN_COLOR_2
                reachable_cell_gui_indicator_position: tuple[int, int] = (reachable_cell[0]["cell_gui"].x+GUI_CELL_SIZE//2, reachable_cell[0]["cell_gui"].y+GUI_CELL_SIZE//2)
                reachable_cell_gui_indicator_size: int = 10
                #print(reachable_cell_gui_indicator_color)
                pygame.draw.circle(WINDOW, reachable_cell_gui_indicator_color, reachable_cell_gui_indicator_position, reachable_cell_gui_indicator_size)
        """
        -----------------------------------END TEST-------------------------------------
        ################################################################################
        """
        
        
        CLOCK.tick(FPS) # Set the framerate of the window
        window_update(WINDOW, BLACK, CLOCK, False) # Update the window

if __name__ == "__main__":
    main()