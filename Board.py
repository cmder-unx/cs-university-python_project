from GUI import GUI
from constants import *
from typing import *

class Board:
    
    def __init__(self, size: int, columns: list[str]) -> None:
        self.size: int = size
        self.columns: list[str] = columns
        self.board: list[dict] = self.create_board()
        GUI().gui_board(self.board)
    
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
        board: list = []
        for column in self.columns:
            for row in range(self.size):
                cell: dict = {}
                cell["cell_row"] = row
                cell["cell_col"] = column
                cell["cell_index"] = (row, column)
                
                # if the cell is in a even row and column, it will be colored with the color 1, else it will be colored with the color 2
                cell["cell_color"] = CELL_COLOR_1 if (self.columns.index(column) + row) % 2 == 0 else CELL_COLOR_2 
                
                cell["cell_is_empty"] = True
                cell["cell_owner"] = 0
                cell["cell_gui"] = None
                board.append(cell)
        return board
    
    def get_cell(self, board: list[dict], cell_index: tuple[int, str]) -> tuple[dict, int]:
        """_summary_ : this function will return the cell of the board that correspond to the cell_index

        Args:
            board (list[dict]): the board with all the cells
            cell_index (tuple[int, str]): the index of the cell we want to get tuple (row, column)

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

