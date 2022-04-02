from constants import *
from typing import *

class Pawns:
    
    def create_player_pawns(self, player_id: int, board: list[dict]) -> list:
        """
        this function will create the pawns for the player with the given id
        """
        player_pawns: list[dict] = []
        for cell in board:
            pawn_informations: dict = {}
            if player_id == 1 and cell["cell_row"] > 5 and cell["cell_color"] == "B":
                #Create pawn with its data and add it to the player 1 pawns list
                pawn_informations["pawn_type"] = "Pawn"
                pawn_informations["pawn_color"] = "W"
                pawn_informations["pawn_status"] = "alive"
                pawn_informations["pawn_owner"] = 1
                pawn_informations["pawn_row"] = cell["cell_row"]
                pawn_informations["pawn_col"] = cell["cell_col"]
                pawn_informations["pawn_pos"] = list(cell["cell_index"])
                player_pawns.append(pawn_informations)
                #Update the cell data
                cell["cell_is_empty"] = False
                cell["cell_owner"] = player_id
            elif player_id == 2 and cell["cell_row"] < 4 and cell["cell_color"] == "B":
                pawn_informations["pawn_color"] = "B"
                pawn_informations["pawn_type"] = "Pawn"
                pawn_informations["pawn_status"] = "alive"
                pawn_informations["pawn_owner"] = 2
                pawn_informations["pawn_row"] = cell["cell_row"]
                pawn_informations["pawn_col"] = cell["cell_col"]
                pawn_informations["pawn_pos"] = list(cell["cell_index"])
                player_pawns.append(pawn_informations)
                cell["cell_is_empty"] = False
                cell["cell_owner"] = player_id
        return player_pawns

    def get_pawn(self, pawns: list[dict], pawn_pos: list[int, str]) -> tuple[dict, int]:
        """
        this function will return the pawn that is in the given position
        """
        i: int = 0
        j: int = len(pawns) - 1
        while i <= j:
            if pawns[i]["pawn_pos"] == pawn_pos:
                return pawns[i], i
            else:
                i+=1
            if pawns[j]["pawn_pos"] == pawn_pos:
                return pawns[j], j
            else:
                j-=1
        return None, None
    
    def is_reachable(self, pawn: tuple[dict, int], init_board) -> list[tuple[dict, int]]:
        """
        this function will return the list of the cells that the pawn can move to
        """
        reachable_cells: list[dict] = []
        columns: list[str] = BOARD_COLUMNS
        pawn_type: str = pawn[0]["pawn_type"]
        pawn_owner:int = pawn[0]["pawn_owner"]
        pawn_row: int = pawn[0]["pawn_row"]
        pawn_col: int = columns.index(pawn[0]["pawn_col"])
        
        for i in range(1, PAWN_MAX_RANGE+1 if pawn_type == "Pawn" else QUEEN_MAX_RANGE+1):
            row_top: int = pawn_row - i
            row_bottom: int = pawn_row + i
            column_left: int = pawn_col - i
            column_right: int = pawn_col + i
            
            if pawn_owner == 1:
                reach_top_right_cell: tuple[int, str] = (row_top, columns[column_right])
                reach_top_left_cell: tuple[int, str] = (row_top, columns[column_left])
                if pawn_type == "Queen":
                    reach_bottom_left_cell: tuple[int, str] = (row_bottom, columns[column_left])
                    reach_bottom_right_cell: tuple[int, str] = (row_bottom, columns[column_right])
            else:
                reach_top_right_cell: tuple[int, str] = (row_bottom, columns[column_right])
                reach_top_left_cell: tuple[int, str] = (row_bottom, columns[column_left])
                if pawn_type == "Queen":
                    reach_bottom_left_cell: tuple[int, str] = (row_top, columns[column_left])
                    reach_bottom_right_cell: tuple[int, str] = (row_top, columns[column_right])
        
            top_right_cell_informations: tuple[dict, int] = init_board.get_cell(init_board.board, reach_top_right_cell)
            top_left_cell_informations: tuple[dict, int] = init_board.get_cell(init_board.board, reach_top_left_cell)

            if None not in top_right_cell_informations:
                reachable_cells.append(top_right_cell_informations)
            if None not in top_left_cell_informations:
                reachable_cells.append(top_left_cell_informations)
            
            if pawn_type == "Queen":
                bottom_left_cell_informations: tuple[dict, int] = init_board.get_cell(init_board.board, reach_bottom_left_cell)
                bottom_right_cell_informations: tuple[dict, int] = init_board.get_cell(init_board.board, reach_bottom_right_cell)
                
                if None not in bottom_left_cell_informations:
                    reachable_cells.append(bottom_left_cell_informations)
                if None not in bottom_right_cell_informations:
                    reachable_cells.append(bottom_right_cell_informations)
        
        return reachable_cells

    def move_pawn(self, pawns:list[dict], pawn: tuple[dict, int], move_to: tuple[int, str], init_board) -> bool:
        """
        this function will move the pawn
        return True if the move is good and False otherwise
        """
        informations_about_the_actual_cell: tuple[dict, int] = init_board.get_cell(init_board.board, tuple(pawn[0]["pawn_pos"]))
        informations_about_the_destination_cell: tuple[dict, int] = init_board.get_cell(init_board.board, move_to)
        if pawn[0]["pawn_pos"] != list(move_to):
            if informations_about_the_destination_cell in self.is_reachable(pawn, init_board) and informations_about_the_destination_cell[0]["cell_is_empty"]:
                informations_about_the_actual_cell[0]["cell_is_empty"] = True
                informations_about_the_actual_cell[0]["cell_owner"] = 0
                
                pawns[pawn[1]]["pawn_row"] = move_to[0]
                pawns[pawn[1]]["pawn_col"] = move_to[1]
                pawns[pawn[1]]["pawn_pos"] = [pawns[pawn[1]]["pawn_row"], pawns[pawn[1]]["pawn_col"]]
                
                informations_about_the_destination_cell[0]["cell_is_empty"] = False
                informations_about_the_destination_cell[0]["cell_owner"] = pawns[pawn[1]]["pawn_owner"]
                return True
            else:
                return False
        else:
            return False