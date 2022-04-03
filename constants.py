import string, pygame

# DEFINE CONSTANTS
BOARD_SIZE: int = 10
BOARD_COLUMNS: tuple[str] = tuple(string.ascii_uppercase[:BOARD_SIZE])
PAWN_MAX_RANGE: int = 1
QUEEN_MAX_RANGE: int = 9
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

#    PYGAME
GAME_NAME: str = "Checkers"
WIDTH: int = BOARD_SIZE*GUI_CELL_SIZE
HEIGHT: int = BOARD_SIZE*GUI_CELL_SIZE
WINDOW_SIZE: tuple[int, int] = (WIDTH, HEIGHT)
FPS: int = 60
CLOCK: pygame.time.Clock = pygame.time.Clock()
