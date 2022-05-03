from GUI import GUI
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
        self.player_pawns: list[dict] = self.create_player_pawns(3) 
        
        GUI().gui_pawns(self.player_pawns, self.board) # Create the gui for the pawns (GUI = Graphical User Interface)
    
    def create_player_pawns(self, layer: int) -> list[dict]:
        """_summary_: this function will create the pawns for the player as a list of dictionnaries

        Returns:
            list[dict]: the list of the pawns for the player, each pawn is represented by a dictionnary
        """
        player_pawns: list[dict] = [] # will contain each dict that represents a pawn
        for cell in self.board:
            pawn_informations: dict = {} # will contain the informations about the pawn
            if self.player_id == 1 and cell["cell_row"] > BOARD_SIZE-(layer+1) and cell["cell_color"] == "B":
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
            elif self.player_id == 2 and cell["cell_row"] < layer and cell["cell_color"] == "B":
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
    
    def get_valid_moves(self, pawn: tuple[dict, int], board: Board):
        moves: dict = {}
        left: int = BOARD_COLUMNS.index(pawn[0]["pawn_col"]) - 1
        right: int = BOARD_COLUMNS.index(pawn[0]["pawn_col"]) + 1
        row: int = pawn[0]["pawn_row"]
        
        if pawn[0]["pawn_owner"] == 1 or pawn[0]["pawn_type"] == "King":
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, board, left, skipped=[]))
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, board, right, skipped=[]))
        
        if pawn[0]["pawn_owner"] == 2 or pawn[0]["pawn_type"] == "King":
            moves.update(self._traverse_left(row+1, min(row+3, BOARD_SIZE), 1, board, left, skipped=[]))
            moves.update(self._traverse_right(row+1, min(row+3, BOARD_SIZE), 1, board, right, skipped=[]))
        
        """ if pawn[0]["pawn_type"] == "King":
            moves.update(self._traverse_left_king(row-1, -1, -1, board, left, skipped=[]))
            moves.update(self._traverse_right_king(row-1, -1, -1, board, right, skipped=[]))
            moves.update(self._traverse_left_king(row+1, BOARD_SIZE, 1, board, left, skipped=[]))
            moves.update(self._traverse_right_king(row+1, BOARD_SIZE, 1, board, right, skipped=[])) """
        
        tmp_len: int = 0
        best_move_key: tuple[int, str] = None
        for move in moves:
            if len(moves[move]) > tmp_len:
                tmp_len = len(moves[move])
                best_move_key = move
        
        if best_move_key:
            moves = {best_move_key: moves[best_move_key]}
        
        return moves
    
    def _traverse_left(self, start, stop, step, board: Board, left, skipped=[]):
        moves = {}
        last = []
        
        for row in range(start, stop, step):
            if left < 0:
                break
            
            current_cell = board.get_cell(board.board, (row, BOARD_COLUMNS[left]))
            if current_cell[0]["cell_is_empty"] == True:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, BOARD_COLUMNS[left])] = last + skipped
                else:
                    moves[(row, BOARD_COLUMNS[left])] = last
                
                if last:
                    if step == -1:
                        row_range = max(row-3, -1)
                    else:
                        row_range = min(row+3, BOARD_SIZE)
                    moves.update(self._traverse_left(row+step, row_range, step, board, left-1, skipped=last))
                    moves.update(self._traverse_right(row+step, row_range, step, board, left+1, skipped=last))
                break
            elif current_cell[0]["cell_owner"] == self.player_id:
                break
            else:
                last = [current_cell]
            
            left -= 1
        
        return moves
    
    def _traverse_right(self, start, stop, step, board: Board, right, skipped=[]):
        moves = {}
        last = []
        
        for row in range(start, stop, step):
            if right >= len(BOARD_COLUMNS):
                break
            
            current_cell = board.get_cell(board.board, (row, BOARD_COLUMNS[right]))
            if current_cell[0]["cell_is_empty"] == True:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, BOARD_COLUMNS[right])] = last + skipped
                else:
                    moves[(row, BOARD_COLUMNS[right])] = last
                
                if last:
                    if step == -1:
                        row_range = max(row-3, -1)
                    else:
                        row_range = min(row+3, BOARD_SIZE)
                    moves.update(self._traverse_left(row+step, row_range, step, board, right-1, skipped=last))
                    moves.update(self._traverse_right(row+step, row_range, step, board, right+1, skipped=last))
                break
            elif current_cell[0]["cell_owner"] == self.player_id:
                break
            else:
                last = [current_cell]
            
            right += 1
        
        return moves
    
    def _traverse_left_king(self, start, stop, step, board: Board, left, skipped=[]):
        moves = {}
        last = []
        
        for row in range(start, stop, step):
            if row < 0 or row >= BOARD_SIZE or left < 0:
                break
            
            current_cell = board.get_cell(board.board, (row, BOARD_COLUMNS[left]))
            if row+step > -1 and row+step < BOARD_SIZE and left-1 > -1:
                next_cell = board.get_cell(board.board, (row+step, BOARD_COLUMNS[left-1]))
                if current_cell[0]["cell_is_empty"] == False and next_cell[0]["cell_is_empty"] == False:
                    break
            if current_cell[0]["cell_is_empty"] == True:
                if skipped:
                    moves[(row, BOARD_COLUMNS[left])] = last + skipped
                else:
                    moves[(row, BOARD_COLUMNS[left])] = last
                
                moves.update(self._traverse_left_king(row+step, stop, step, board, left-1, skipped=last+skipped))
                break
            elif current_cell[0]["cell_owner"] == self.player_id:
                break
            else:
                last = [current_cell]
            
            left -= 1
        
        return moves
    
    def _traverse_right_king(self, start, stop, step, board: Board, right, skipped=[]):
        moves = {}
        last = []
        
        for row in range(start, stop, step):
            if row < 0 or row >= BOARD_SIZE or right >= len(BOARD_COLUMNS):
                break
            
            current_cell = board.get_cell(board.board, (row, BOARD_COLUMNS[right]))
            if row+step > -1 and row+step < BOARD_SIZE and right+1 < len(BOARD_COLUMNS):
                next_cell = board.get_cell(board.board, (row+step, BOARD_COLUMNS[right+1]))
                if current_cell[0]["cell_is_empty"] == False and next_cell[0]["cell_is_empty"] == False:
                    break
            if current_cell[0]["cell_is_empty"] == True:
                if skipped:
                    moves[(row, BOARD_COLUMNS[right])] = last + skipped
                else:
                    moves[(row, BOARD_COLUMNS[right])] = last
                
                moves.update(self._traverse_right_king(row+step, stop, step, board, right+1, skipped=last+skipped))
                break
            elif current_cell[0]["cell_owner"] == self.player_id:
                break
            else:
                last = [current_cell]
            
            right += 1
        
        return moves

    def move_pawn(self, pawn: tuple[dict, int], move_to: tuple[int, str], reachable_cells_by_pawn: dict, ennemy_pawns: list[dict], board: Board):
        if move_to in reachable_cells_by_pawn:
            current_cell: tuple[dict, int] = board.get_cell(board.board, tuple(pawn[0]["pawn_pos"]))
            destination_cell: tuple[dict, int] = board.get_cell(board.board, move_to)
            if not reachable_cells_by_pawn[move_to]:
                current_cell[0]["cell_owner"] = 0
                current_cell[0]["cell_is_empty"] = True
                
                destination_cell[0]["cell_owner"] = self.player_id
                destination_cell[0]["cell_is_empty"] = False
                
                pawn[0]["pawn_row"], pawn[0]["pawn_col"] = move_to[0], move_to[1]
                pawn[0]["pawn_pos"] = list(move_to)
                pawn[0]["pawn_gui"].x = destination_cell[0]["cell_gui"].x+GUI_CELL_SIZE//2
                pawn[0]["pawn_gui"].y = destination_cell[0]["cell_gui"].y+GUI_CELL_SIZE//2
                
                if self.player_id == 1 and pawn[0]["pawn_row"] == 0:
                    pawn[0]["pawn_type"] = "King"
                elif self.player_id == 2 and pawn[0]["pawn_row"] == BOARD_SIZE-1:
                    pawn[0]["pawn_type"] = "King"
                
            else:
                for cell in reachable_cells_by_pawn[move_to]:
                    if not cell[0]["cell_is_empty"]:
                        current_cell[0]["cell_owner"] = 0
                        current_cell[0]["cell_is_empty"] = True
                        
                        cell[0]["cell_owner"] = 0
                        cell[0]["cell_is_empty"] = True
                        self.take_pawn(ennemy_pawns, list(cell[0]["cell_index"]))
                
                destination_cell[0]["cell_owner"] = self.player_id
                destination_cell[0]["cell_is_empty"] = False
                
                pawn[0]["pawn_row"], pawn[0]["pawn_col"] = move_to[0], move_to[1]
                pawn[0]["pawn_pos"] = list(move_to)
                pawn[0]["pawn_gui"].x = destination_cell[0]["cell_gui"].x+GUI_CELL_SIZE//2
                pawn[0]["pawn_gui"].y = destination_cell[0]["cell_gui"].y+GUI_CELL_SIZE//2
                
                if self.player_id == 1 and pawn[0]["pawn_row"] == 0:
                    pawn[0]["pawn_type"] = "King"
                elif self.player_id == 2 and pawn[0]["pawn_row"] == BOARD_SIZE-1:
                    pawn[0]["pawn_type"] = "King"

    def take_pawn(self, pawns: list[dict], pawn_pos: list[int, str]):
        pawn_to_take: tuple[dict, int] = self.get_pawn(pawns, pawn_pos)
        if None not in pawn_to_take:
            pawn_to_take[0]["pawn_status"] = "dead"
            pawn_to_take[0]["pawn_row"] = None
            pawn_to_take[0]["pawn_col"] = None
            pawn_to_take[0]["pawn_pos"] = None
            pawn_to_take[0]["pawn_gui"] = None
        else:
            print(False)
    
    def selectable_pawns(self):
        pass



if __name__ == "__main__":
    board = Board(BOARD_SIZE, BOARD_COLUMNS)
    pawn = Pawns(1, board.board)
    pawn2 = Pawns(2, board.board)
    
    print("\n")
    
    print(pawn.get_valid_moves(pawn.get_pawn(pawn.player_pawns, [6, "F"]), board))
    
    #print(pawn.paths((5, "E"), board))