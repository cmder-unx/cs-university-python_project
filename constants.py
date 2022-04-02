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
GAME_NAME: str = "Checkers"
WIDTH: int = 1080
HEIGHT: int = 720
WINDOW_SIZE: tuple[int, int] = (WIDTH, HEIGHT)
FPS: int = 60
CLOCK = pygame.time.Clock()

GUI_CELL_SIZE: int = 50
GUI_CELL_COLOR_1: tuple[int] = WHITE
GUI_CELL_COLOR_2: tuple[int] = BLACK