# DEPENDENCIES
import pygame, sys
from Board import Board
from Pawns import Pawns
from constants import *
from typing import *

pygame.init()

WINDOW: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(GAME_NAME)

def window_update(window: pygame.Surface, color: tuple[int, int, int], clock: pygame.time.Clock, show_fps: bool) -> None:
    pygame.display.update()
    window.fill(color)
    print(clock.get_fps()) if show_fps else None

board: Board = Board(BOARD_SIZE, BOARD_COLUMNS)
player1: list[dict] = Pawns(1, board.board)
player2: list[dict] = Pawns(2, board.board)
get_a_pawn_informations: tuple[dict, int] = player1.get_pawn(player1.player_pawns, [6, "B"])

#print(get_a_pawn_informations,"\n\n\n")
#player1.move_pawn(player1.player_pawns, get_a_pawn_informations, (5, "C"), board)
#print(board,"\n\n\n")
#get_a_pawn_informations2: tuple[dict, int] = player1.get_pawn(player1.player_pawns, [5, "C"])
#print(get_a_pawn_informations2)

def main() -> None:
    game_running = True
    reachable_cells_by_pawn = None
    while game_running:
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #THIS IS CURRENTLY A TEST - SO IT WILL BE CLEANER LATER
                for cell in board.board:
                    if cell["cell_gui"].collidepoint(mouse_pos_x, mouse_pos_y):
                        cell_informations: tuple[dict, int] = board.get_cell(board.board, cell["cell_index"])
                        if not cell_informations[0]["cell_is_empty"]:
                            pawn_informations: tuple[dict, int] = player1.get_pawn(player1.player_pawns, list(cell_informations[0]["cell_index"]))
                            if None not in pawn_informations:
                                if pawn_informations[0]["pawn_status"] == "alive":
                                    reachable_cells_by_pawn: list[tuple[dict, int]] = player1.is_reachable(pawn_informations, board)
                            else:
                                reachable_cells_by_pawn = None
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        board.draw_gui_board(WINDOW, board.board)
        player1.draw_gui_pawns(WINDOW, player1.player_pawns)
        player2.draw_gui_pawns(WINDOW, player2.player_pawns)
        
        if reachable_cells_by_pawn:
            for reachable_cell in reachable_cells_by_pawn:
                reachable_cell_gui_indicator_color: tuple[int, int, int] = GUI_PAWN_COLOR_1 if pawn_informations[0]["pawn_owner"] == 1 else GUI_PAWN_COLOR_2
                reachable_cell_gui_indicator_position: tuple[int, int] = (reachable_cell[0]["cell_gui"].x+GUI_CELL_SIZE//2, reachable_cell[0]["cell_gui"].y+GUI_CELL_SIZE//2)
                reachable_cell_gui_indicator_size: int = 10
                #print(reachable_cell_gui_indicator_color)
                pygame.draw.circle(WINDOW, reachable_cell_gui_indicator_color, reachable_cell_gui_indicator_position, reachable_cell_gui_indicator_size)
        
        
        mouse_pos_x: int = pygame.mouse.get_pos()[0]
        mouse_pos_y: int = pygame.mouse.get_pos()[1]
        
        CLOCK.tick(FPS)
        window_update(WINDOW, BLACK, CLOCK, False)

main()