import pygame
from constants import *
from typing import *

class Board:
    
    def __init__(self, size: int, columns: list[str]) -> None:
        self.size: int = size
        self.columns: list[str] = columns
        self.board: list[dict] = self.create_board()
        self.gui_board(self.board)
    
    def __repr__(self) -> str:
        return f"{self.board}"
    
    def __str__(self) -> str:
        """
        print the board in a nice way with the owner of each cell 
        with the column on the top of the board and the row 
        on the left side of the board
        """
        board_string: str = ""
        column_names: str = "  "
        rows_names: str = ""
        # add column names to the top of the board
        for column in range(self.size):
            column_names += f" {self.columns[column]} "
        # add each cells rows with the row number to the left side of the board
        for row in range(self.size):
            rows_names += f"\n{row} "
            for cell in self.board:
                if cell["cell_row"] == row:
                    rows_names += f" {cell['cell_owner']} "
        board_string = f"{column_names}{rows_names}"
        return board_string
    
    def create_board(self) -> list[dict]:
        """
        This function will create the board
        """
        board: list = []
        for column in self.columns:
            for row in range(self.size):
                cell: dict = {}
                cell["cell_row"] = row
                cell["cell_col"] = column
                cell["cell_index"] = (row, column)
                cell["cell_color"] = CELL_COLOR_1 if (self.columns.index(column) + row) % 2 == 0 else CELL_COLOR_2
                cell["cell_is_empty"] = True
                cell["cell_owner"] = 0
                cell["cell_gui"] = None
                board.append(cell)
        return board
    
    def get_cell(self, board: list[dict], cell_index: tuple[int, str]) -> tuple[dict, int]:
        """
        this function will return a tuple with the dict that contain 
        informations about the cell and the index of this dict in the board list.
        For searching the cell in the board list we will use disection algorithm.
        """
        i: int = 0
        j: int = len(board) - 1
        while i <= j:
            if board[i]["cell_index"] == cell_index:
                return board[i], i
            else:
                i+=1
            if board[j]["cell_index"] == cell_index:
                return board[j], j
            else:
                j-=1
        return None, None
    
    def gui_board(self, board: list[dict]) -> None:
        for cell_dict in board:
            cell_gui_position: tuple[int, int] = (BOARD_COLUMNS.index(cell_dict["cell_col"]) * GUI_CELL_SIZE, cell_dict["cell_row"] * GUI_CELL_SIZE)
            cell_gui_size: tuple[int, int] = (GUI_CELL_SIZE, GUI_CELL_SIZE)
            cell_dict["cell_gui"] = pygame.Rect(cell_gui_position, cell_gui_size)
    
    def draw_gui_board(self, screen: pygame.Surface, board: list[dict]) -> None:
        for cell_dict in board:
            color: tuple[int, int, int] = GUI_CELL_COLOR_1 if cell_dict["cell_color"] == CELL_COLOR_1 else GUI_CELL_COLOR_2
            pygame.draw.rect(screen, color, cell_dict["cell_gui"])
