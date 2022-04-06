import pygame
from Board import Board
from constants import *
from typing import *

class Pawns:
    
    def __init__(self, player_id: int, board: list[dict]) -> None:
        self.player_id: int = player_id # player id (1 or 2)
        self.board: list[dict] = board # board with all the cells
        
        # Create the pawns for the player. The pawns is represented by a list of dictionnaries, 
        # where each dictionnary is a pawn. The pawns are represented by a dictionnary with the following keys:
        # pawn_type: the type of the pawn (Pawn or King), pawn_color: the color of the pawn (W or B), 
        # pawn_status: the status of the pawn (alive or dead), pawn_owner: the owner of the pawn (1 or 2),
        # pawn_row: the row of the pawn, pawn_col: the column of the pawn, pawn_pos: the position of the pawn (row, col),
        # pawn_gui: the gui of the pawn
        self.player_pawns: list[dict] = self.create_player_pawns() 
        
        self.gui_pawns(self.player_pawns, self.board) # Create the gui for the pawns (GUI = Graphical User Interface)
    
    def create_player_pawns(self) -> list[dict]:
        """_summary_: this function will create the pawns for the player as a list of dictionnaries

        Returns:
            list[dict]: the list of the pawns for the player, each pawn is represented by a dictionnary
        """
        player_pawns: list[dict] = [] # will contain each dict that represents a pawn
        for cell in self.board:
            pawn_informations: dict = {} # will contain the informations about the pawn
            if self.player_id == 1 and cell["cell_row"] > 5 and cell["cell_color"] == "B":
                #Create pawn with its data and add it to pawn_informations
                pawn_informations["pawn_type"] = "Pawn"
                pawn_informations["pawn_color"] = "W"
                pawn_informations["pawn_status"] = "alive"
                pawn_informations["pawn_owner"] = self.player_id
                pawn_informations["pawn_row"] = cell["cell_row"]
                pawn_informations["pawn_col"] = cell["cell_col"]
                pawn_informations["pawn_pos"] = list(cell["cell_index"])
                pawn_informations["pawn_gui"] = None
                player_pawns.append(pawn_informations)
                
                #Update the cell data
                cell["cell_is_empty"] = False
                cell["cell_owner"] = self.player_id
            elif self.player_id == 2 and cell["cell_row"] < 4 and cell["cell_color"] == "B":
                #Create pawn with its data and add it to pawn_informations
                pawn_informations["pawn_color"] = "B"
                pawn_informations["pawn_type"] = "Pawn"
                pawn_informations["pawn_status"] = "alive"
                pawn_informations["pawn_owner"] = self.player_id
                pawn_informations["pawn_row"] = cell["cell_row"]
                pawn_informations["pawn_col"] = cell["cell_col"]
                pawn_informations["pawn_pos"] = list(cell["cell_index"])
                pawn_informations["pawn_gui"] = None
                player_pawns.append(pawn_informations)
                
                #Update the cell data
                cell["cell_is_empty"] = False
                cell["cell_owner"] = self.player_id
        return player_pawns

    def get_pawn(self, pawns: list[dict], pawn_pos: list[int, str]) -> tuple[dict, int]:
        """_summary_: this function will return the informations about the pawn 
                    at the position pawn_pos and the index of the pawn in the pawns list

        Args:
            pawns (list[dict]): player pawns list
            pawn_pos (list[int, str]): the position of the pawn that we want to get list [row, col]

        Returns:
            tuple[dict, int]: pawn informations and the index of the pawn in the pawns list
        """        
        beginning_index_of_the_pawns_list: int = 0
        end_index_of_the_pawns_list: int = len(pawns) - 1
        while beginning_index_of_the_pawns_list <= end_index_of_the_pawns_list:
            if pawns[beginning_index_of_the_pawns_list]["pawn_pos"] == pawn_pos:
                return pawns[beginning_index_of_the_pawns_list], beginning_index_of_the_pawns_list
            else:
                beginning_index_of_the_pawns_list+=1
            if pawns[end_index_of_the_pawns_list]["pawn_pos"] == pawn_pos:
                return pawns[end_index_of_the_pawns_list], end_index_of_the_pawns_list
            else:
                end_index_of_the_pawns_list-=1
        return None, None
    
    def is_reachable(self, pawn: tuple[dict, int], board: Board) -> list[tuple[dict, int]]:
        """_summary_: this function will return the list of cells (with their informations and index in the board list) 
                        that are reachable by the pawn

        Args:
            pawn (tuple[dict, int]): the pawn that we want to check the reachability
            board (Board): the board initializer

        Returns:
            list[tuple[dict, int]]: the list of cells (with their informations and index in the board list) 
                                    that are reachable by the pawn
        """        
        reachable_cells: list[tuple[dict, int]] = [] # will contain the cells that are reachable by the pawn
        columns: list[str] = BOARD_COLUMNS
        pawn_type: str = pawn[0]["pawn_type"]
        pawn_owner:int = pawn[0]["pawn_owner"]
        pawn_row: int = pawn[0]["pawn_row"]
        pawn_col: int = columns.index(pawn[0]["pawn_col"])
        
        for i in range(1, PAWN_MAX_RANGE+1 if pawn_type == "Pawn" else KING_MAX_RANGE+1): # change the range depending on the pawn type
            row_top: int = pawn_row - i
            row_bottom: int = pawn_row + i
            column_left: int = pawn_col - i
            column_right: int = pawn_col + i
            
            # We will compute the reachable cells in 2 different ways if it's a basic pawn and 
            # 4 different ways if it's a king 
            # depending on the pawn type
            # for basic pawn
            if column_right < len(columns):
                reach_top_right_cell: tuple[int, str] = (row_top if pawn_owner == 1 else row_bottom, columns[column_right])
            else:
                reach_top_right_cell: tuple[int, str] = (None, None)
            if column_left >= 0:
                reach_top_left_cell: tuple[int, str] = (row_top if pawn_owner == 1 else row_bottom, columns[column_left])
            else:
                reach_top_left_cell: tuple[int, str] = (None, None)
            # if the pawn is a king in addition to the 2 different way for the basic pawn, 
            # we will compute the 2 other different way
            if pawn_type == "King":
                reach_bottom_left_cell: tuple[int, str] = (row_bottom if pawn_owner == 1 else row_top, columns[column_left])
                if column_right < len(columns):
                    reach_bottom_right_cell: tuple[int, str] = (row_bottom if pawn_owner == 1 else row_top, columns[column_right])
                else:
                    reach_bottom_right_cell: tuple[int, str] = (None, None)

            # Get informations about the reachable cells
            top_right_cell_informations: tuple[dict, int] = board.get_cell(board.board, reach_top_right_cell)
            top_left_cell_informations: tuple[dict, int] = board.get_cell(board.board, reach_top_left_cell)

            if None not in top_right_cell_informations: # if the cell exists we will add it to the reachable cells list
                reachable_cells.append(top_right_cell_informations)
            if None not in top_left_cell_informations:
                reachable_cells.append(top_left_cell_informations)
            
            
            if pawn_type == "King": # if the pawn is a king we will add the 2 other different way
                # Get informations about the reachable cells
                bottom_left_cell_informations: tuple[dict, int] = board.get_cell(board.board, reach_bottom_left_cell)
                bottom_right_cell_informations: tuple[dict, int] = board.get_cell(board.board, reach_bottom_right_cell)
                
                if None not in bottom_left_cell_informations: # if the cell exists we will add it to the reachable cells list
                    reachable_cells.append(bottom_left_cell_informations)
                if None not in bottom_right_cell_informations:
                    reachable_cells.append(bottom_right_cell_informations)
        
        return reachable_cells

    def move_pawn(self, pawns:list[dict], pawn: tuple[dict, int], move_to: tuple[int, str], board: Board) -> bool:
        """_summary_: this function will move the pawn to the cell that is passed in parameter and return True if the move has been done, False otherwise

        Args:
            pawns (list[dict]): list of pawns 
            pawn (tuple[dict, int]): the pawn that we want to move
            move_to (tuple[int, str]): the destination cell
            board (Board): board initializer

        Returns:
            bool: boolean that will be True if the move has been done, False otherwise
        """
        informations_about_the_actual_cell: tuple[dict, int] = board.get_cell(board.board, tuple(pawn[0]["pawn_pos"])) # get the informations about the actual cell
        informations_about_the_destination_cell: tuple[dict, int] = board.get_cell(board.board, move_to) # get the informations about the destination cell
        if pawn[0]["pawn_pos"] != list(move_to): # if the pawn is not already in the destination cell
            if informations_about_the_destination_cell in self.is_reachable(pawn, board) and informations_about_the_destination_cell[0]["cell_owner"] == 0: # if the destination cell is reachable and empty (has no owner)
                
                
                # Update informations about the actual cell
                informations_about_the_actual_cell[0]["cell_is_empty"] = True
                informations_about_the_actual_cell[0]["cell_owner"] = 0
                
                # Update the pawn informations (position and gui)
                pawns[pawn[1]]["pawn_row"] = move_to[0]
                pawns[pawn[1]]["pawn_col"] = move_to[1]
                pawns[pawn[1]]["pawn_pos"] = [pawns[pawn[1]]["pawn_row"], pawns[pawn[1]]["pawn_col"]]
                
                pawns[pawn[1]]["pawn_gui"].x = informations_about_the_destination_cell[0]["cell_gui"].x+GUI_CELL_SIZE//2
                pawns[pawn[1]]["pawn_gui"].y = informations_about_the_destination_cell[0]["cell_gui"].y+GUI_CELL_SIZE//2
                
                # Update informations about the destination cell
                informations_about_the_destination_cell[0]["cell_is_empty"] = False
                informations_about_the_destination_cell[0]["cell_owner"] = pawns[pawn[1]]["pawn_owner"]
                return True
            elif informations_about_the_destination_cell in self.is_reachable(pawn, board) and informations_about_the_destination_cell[0]["cell_owner"] != self.player_id:
                pass
            else:
                return False
        else:
            return False
    
    def gui_pawns(self, pawns: list[dict], board: list[dict]) -> None:
        """_summary_: this function will create the gui for the pawns

        Args:
            pawns (list[dict]): list of pawns
            board (list[dict]): the board and all cells
        """        
        for pawn in pawns:
            for cell in board:
                if cell["cell_row"] == pawn["pawn_row"] and cell["cell_col"] == pawn["pawn_col"]:
                    pawn_gui_position: tuple[int, int] = (cell["cell_gui"].x+GUI_CELL_SIZE//2, cell["cell_gui"].y+GUI_CELL_SIZE//2)
                    pawn_gui_size: tuple[int, int] = (GUI_PAWN_SIZE, GUI_PAWN_SIZE)
                    pawn["pawn_gui"] = pygame.Rect(pawn_gui_position, pawn_gui_size)
    
    def draw_gui_pawns(self, screen: pygame.Surface, pawns: list[dict]) -> None:
        """_summary_: this function will draw the gui for the pawns

        Args:
            screen (pygame.Surface): the screen where we want to draw the gui for the pawns, here the screen will be WINDOW constant, see constants.py for more info
            pawns (list[dict]): the list of pawns
        """        
        for pawn in pawns:
            if pawn["pawn_gui"] != None:
                color: tuple[int, int, int] = GUI_PAWN_COLOR_1 if pawn["pawn_owner"] == 1 else GUI_PAWN_COLOR_2
                pygame.draw.circle(screen, color, (pawn["pawn_gui"].x, pawn["pawn_gui"].y), pawn["pawn_gui"].width)
