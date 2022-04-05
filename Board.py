import pygame
from constants import *
from typing import *

class Board:
    
    def __init__(self, size: int, columns: list[str]) -> None:
        self.size: int = size # size of the board, number of rows and columns
        self.columns: list[str] = columns # list of the columns names, check constants.py for more info BOARD_COLUMNS
        
        # Create the board. The board represented by a list of the cells, 
        # each cell is a dict with the following keys: 
        # cell_row, cell_col, cell_index, cell_color, cell_is_empty, cell_owner, cell_gui
        self.board: list[dict] = self.create_board()
        
        self.gui_board(self.board) # Create the gui board (GUI = Graphical User Interface)
    
    def __repr__(self) -> str:
        """_summary_ : this function will return a string containing the representation of the board in its raw form

        Returns:
            str: the representation of the board in its raw form
        """
        return f"{self.board}"
    
    def __str__(self) -> str:
        """
        return the board in a nice way with the owner of each cell 
        with the column on the top of the board and the row 
        on the left side of the board
        """
        board_in_its_nice_form: str = "" # will contain the board in its nice form (combinaison of rows_names and columns_names)
        column_names: str = "  " # will contain the column names
        row_names_and_cells: str = "" # will contain the row names with the cells owner for each cell of each row
        
        # add column names to the top of the board
        for column in range(self.size):
            column_names += f" {self.columns[column]} "
        
        # add each cells with the row number to the left side of the board
        for row in range(self.size):
            row_names_and_cells += f"\n{row} " # add the row number
            for cell in self.board:
                if cell["cell_row"] == row: # if the cell is in the row we are looking at
                    row_names_and_cells += f" {cell['cell_owner']} " # add the cell owner
        
        board_in_its_nice_form: str = f"{column_names}{row_names_and_cells}" # combine the column names and the row names with cells
        return board_in_its_nice_form
    
    def create_board(self) -> list[dict]:
        """_summary_ : this function will create the board and return it as a list of dicts

        Returns:
            list[dict]: the board as a list of dicts, each dict represent a cell
        """
        board: list = [] # will contain each dict that represent a cell of the board
        for column in self.columns:
            for row in range(self.size):
                cell: dict = {} # will contain the informations about the cell
                cell["cell_row"] = row
                cell["cell_col"] = column
                cell["cell_index"] = (row, column)
                
                # if the cell is in a even row and column, it will be colored with the color 1, else it will be colored with the color 2
                cell["cell_color"] = CELL_COLOR_1 if (self.columns.index(column) + row) % 2 == 0 else CELL_COLOR_2 
                
                cell["cell_is_empty"] = True
                cell["cell_owner"] = 0
                cell["cell_gui"] = None
                board.append(cell) # add the cell to the board
        return board
    
    def get_cell(self, board: list[dict], cell_index: tuple[int, str]) -> tuple[dict, int]:
        """_summary_ : this function will return the cell of the board that correspond to the cell_index

        Args:
            board (list[dict]): the board with all the cells
            cell_index (tuple[int, str]): the index of the cell we want to get (row, column)

        Returns:
            tuple[dict, int]: return the cell of the board that correspond to the cell_index and its position index in the board
                            if the cell that we are looking for is not in the board, return None, None
        """        
        beginning_index_of_the_board: int = 0
        end_index_of_the_board: int = len(board) - 1
        while beginning_index_of_the_board <= end_index_of_the_board:
            if board[beginning_index_of_the_board]["cell_index"] == cell_index:
                return board[beginning_index_of_the_board], beginning_index_of_the_board
            else:
                beginning_index_of_the_board+=1
            if board[end_index_of_the_board]["cell_index"] == cell_index:
                return board[end_index_of_the_board], end_index_of_the_board
            else:
                end_index_of_the_board-=1
        return None, None
    
    def gui_board(self, board: list[dict]) -> None:
        """_summary_: this function will create the gui board (GUI = Graphical User Interface), adding the rectangles to each cell of the board

        Args:
            board (list[dict]): the board with all the cells
        """        
        for cell_dict in board:
            cell_gui_position: tuple[int, int] = (BOARD_COLUMNS.index(cell_dict["cell_col"]) * GUI_CELL_SIZE, cell_dict["cell_row"] * GUI_CELL_SIZE)
            cell_gui_size: tuple[int, int] = (GUI_CELL_SIZE, GUI_CELL_SIZE)
            cell_dict["cell_gui"] = pygame.Rect(cell_gui_position, cell_gui_size) # create the gui of the cell, the gui is a rectangle
    
    def draw_gui_board(self, screen: pygame.Surface, board: list[dict]) -> None:
        """_summary_: this function will draw the gui board (GUI = Graphical User Interface) on the screen

        Args:
            screen (pygame.Surface): the screen where we want to draw the gui board, here the screen will be WINDOW constant, see constants.py for more info
            board (list[dict]): the board with all the cells
        """        
        for cell_dict in board:
            color: tuple[int, int, int] = GUI_CELL_COLOR_1 if cell_dict["cell_color"] == CELL_COLOR_1 else GUI_CELL_COLOR_2
            pygame.draw.rect(screen, color, cell_dict["cell_gui"])
