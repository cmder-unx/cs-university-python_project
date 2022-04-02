# DEPENDENCIES
import pygame, sys
from Board import Board
from Pawns import Pawns
from constants import *
from typing import *

pygame.init()

WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(GAME_NAME)

def window_update(window, color, clock, show_fps):
    pygame.display.update()
    window.fill(color)
    print(clock.get_fps()) if show_fps else None

board = Board(BOARD_SIZE, BOARD_COLUMNS)
player1: list[dict] = Pawns().create_player_pawns(1, board.board)
player2: list[dict] = Pawns().create_player_pawns(2, board.board)
get_a_pawn_informations: tuple[dict, int] = Pawns().get_pawn(player1, [6, "B"])

#print(board)
#print("Player1 pawns :\n", player1,"\n\n\nPlayer2 pawns :\n", player2,"\n\n\n")
#print(board,"\n\n\n")
#print(Pawns().is_reachable(get_a_pawn_informations, board), "\n\n\n")
#print(Pawns().move_pawn(player1, get_a_pawn_informations, (5, "C"), board), "\n\n\n")
#print(board,"\n\n\n")

def main():
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        board.draw_gui_board(WINDOW, board.board)
        CLOCK.tick(FPS)
        window_update(WINDOW, BLACK, CLOCK, True)

main()