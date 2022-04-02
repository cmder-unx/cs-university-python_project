import string, pygame

# DEFINE CONSTANTS
BOARD_SIZE: int = 10
BOARD_COLUMNS: tuple[str] = tuple(string.ascii_uppercase[:BOARD_SIZE])
PAWN_MAX_RANGE: int = 1
QUEEN_MAX_RANGE: int = 9
CELL_COLOR_1: str = "W"
CELL_COLOR_2: str = "B"

#_____COLORS_____
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#_____GUI_____
GAME_NAME = "Checkers"
WIDTH, HEIGHT = 1080, 720
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 60
CLOCK = pygame.time.Clock()

GUI_CELL_SIZE: int = 50
GUI_CELL_COLOR_1: tuple[int] = WHITE
GUI_CELL_COLOR_2: tuple[int] = BLACK