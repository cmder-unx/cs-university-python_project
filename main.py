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
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        board.draw_gui_board(WINDOW, board.board)
        player1.draw_gui_pawns(WINDOW, player1.player_pawns)
        player2.draw_gui_pawns(WINDOW, player2.player_pawns)
        CLOCK.tick(FPS)
        window_update(WINDOW, BLACK, CLOCK, True)

main()