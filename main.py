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

init_board = Board(BOARD_SIZE, BOARD_COLUMNS)
player1: list[dict] = Pawns().create_player_pawns(1, init_board.board)
player2: list[dict] = Pawns().create_player_pawns(2, init_board.board)
get_a_pawn_informations: tuple[dict, int] = Pawns().get_pawn(player1, [6, "B"])

#print(init_board)
#print("Player1 pawns :\n", player1,"\n\n\nPlayer2 pawns :\n", player2,"\n\n\n")
#print(init_board,"\n\n\n")
#print(Pawns().is_reachable(get_a_pawn_informations, init_board), "\n\n\n")
#print(Pawns().move_pawn(player1, get_a_pawn_informations, (5, "C"), init_board), "\n\n\n")
#print(init_board,"\n\n\n")

def main():
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        init_board.draw_gui_board(WINDOW, init_board.board)
        CLOCK.tick(FPS)
        window_update(WINDOW, BLACK, CLOCK, True)

main()