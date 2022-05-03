import string, pygame

"""
THIS FILE CONTAINS ALL THE CONSTANTS USED IN THE GAME
"""

# DEFINE CONSTANTS
BOARD_SIZE: int = 8
BOARD_COLUMNS: tuple[str] = tuple(string.ascii_uppercase[:BOARD_SIZE])
CELL_COLOR_1: str = "W"
CELL_COLOR_2: str = "B"

#_____COLORS_____
BLACK: tuple[int, int, int] = (0,0,0)
WHITE: tuple[int, int, int] = (255,255,255)
RED: tuple[int, int, int] = (255,0,0)
GREEN: tuple[int, int, int] = (0,255,0)
BLUE: tuple[int, int, int] = (0,0,255)

#_____GUI_____
GUI_CELL_SIZE: int = 50
GUI_CELL_COLOR_1: tuple[int] = WHITE
GUI_CELL_COLOR_2: tuple[int] = BLACK

GUI_PAWN_SIZE: int = 25
GUI_PAWN_COLOR_1: tuple[int, int, int] = (0,0,255)
GUI_PAWN_COLOR_2: tuple[int, int, int] = (255,0,0)

GUI_KING_COLOR_1: tuple[int, int, int] = (60,125,255)
GUI_KING_COLOR_2: tuple[int, int, int] = (255,125,60)

#    PYGAME
GAME_NAME: str = "Checkers"
WIDTH: int = BOARD_SIZE*GUI_CELL_SIZE
HEIGHT: int = BOARD_SIZE*GUI_CELL_SIZE
WINDOW_SIZE: tuple[int, int] = (WIDTH, HEIGHT)
FPS: int = 60
CLOCK: pygame.time.Clock = pygame.time.Clock()

WINDOW: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(GAME_NAME)
