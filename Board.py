from GUI import GUI
import constants
from typing import *

class Board:
    
    def __init__(self, size: int, columns: list[str]) -> None:
        """_summary_ : Initialisation de la classe Board. Création de la board sous forme de liste de dictionnaires.
        Chaque dictionnaire représente une cellule. Chaque dictionnaire contient les informations à propos de la cellule.

        Args:
            size (int): la taille de la board
            columns (list[str]): la liste des noms de colonnes de la board
        """
        self.size: int = size
        self.columns: list[str] = columns
        self.board: list[dict] = self.create_board()
        GUI().gui_board(self.board)
    
    def __repr__(self) -> str:
        """_summary_ : Représentation de la board sous sa forme brute de liste de dictionnaire.

        Returns:
            str: la board sous sa forme brute de liste de dictionnaire
        """
        return f"{self.board}"
    
    def __str__(self) -> str:
        """_summary_ : Affichage de la board sous une forme plus sympathique de damier en console.

        Returns:
            str: la board sous une forme plus sympathique de damier en console.
        """
        board_in_its_nice_form: str = ""
        column_names: str = "  "
        row_names_and_cells: str = ""
        
        for column in range(self.size):
            column_names += f" {self.columns[column]} "
        
        for row in range(self.size):
            row_names_and_cells += f"\n{row} "
            for cell in self.board:
                if cell["cell_row"] == row:
                    row_names_and_cells += f" {cell['cell_owner']} "
        
        board_in_its_nice_form: str = f"{column_names}{row_names_and_cells}"
        return board_in_its_nice_form
    
    def create_board(self) -> list[dict]:
        """_summary_ : Création de la board sous forme de liste de dictionnaires. Chaque dictionnaire représente une cellule.
        Une cellule est représentée par les informations suivantes:
        - cell_row (int): la ligne de la cellule
        - cell_column (str): la colonne de la cellule
        - cell_index (tuple[int, str]): l'index de la cellule (ligne, colonne)
        - cell_color (str): la couleur de la cellule (claire ou foncé)
        - cell_is_empty (bool): True si la cellule est vide, False sinon
        - cell_owner (str): le propriétaire de la cellule, celui qui se trouve sur la cellule. 0 si vide, 1 si noir, 2 si blanc
        - cell_gui (pygame.Rect) : la cellule sous forme de pygame.Rect (representation graphique de la cellule)
        

        Returns:
            list[dict]: la board sous forme de liste de dictionnaires
        """
        board: list = []
        for column in self.columns:
            for row in range(self.size):
                cell: dict = {}
                cell["cell_row"] = row
                cell["cell_col"] = column
                cell["cell_index"] = (row, column)
                cell["cell_color"] = constants.CELL_COLOR_1 if (self.columns.index(column) + row) % 2 == 0 else constants.CELL_COLOR_2 
                cell["cell_is_empty"] = True
                cell["cell_owner"] = 0
                cell["cell_gui"] = None
                board.append(cell)
        return board
    
    def get_cell(self, board: list[dict], cell_index: tuple[int, str]) -> tuple[dict, int]:
        """_summary_ : Récupération de la cellule correspondant à l'index (ligne, colonne) donné.

        Args:
            board (list[dict]): la board sous forme de liste de dictionnaires.
            cell_index (tuple[int, str]): l'index de la cellule (ligne, colonne)

        Returns:
            tuple[dict, int]: Tuple contenant la cellule correspondant à l'index (ligne, colonne) donné, et son index dans la board
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

