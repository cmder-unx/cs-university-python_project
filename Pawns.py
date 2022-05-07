from GUI import GUI
from Board import Board
import constants
from typing import *

class Pawns:
    
    def __init__(self, player_id: int, board: list[dict]) -> None:
        """_summary_ : Initialisation de la classe Pawns. Création des pions du joueur sous forme de liste de dictionnaires.
        Chaque dictionnaire représente un pion. Chaque dictionnaire contient les informations à propos du pion.

        Args:
            player_id (int): Identifiant du joueur. 1 pour le joueur 1, 2 pour le joueur 2.
            board (list[dict]): Liste de dictionnaires représentant les cellules du plateau.
        """        
        self.player_id: int = player_id
        self.board: list[dict] = board
        self.player_pawns: list[dict] = self.create_player_pawns(3) 
        GUI().gui_pawns(self.player_pawns, self.board)
    
    def create_player_pawns(self, layer: int) -> list[dict]:
        """_summary_ : Création des pions du joueur sous forme de liste de dictionnaires. Chaque dictionnaire représente un pion.
        Un pion est représenté par les informations suivantes :
        - pawn_type (str): Type de pion. (Pawn, King)
        - pawn_color (str): Couleur du pion. (White, Black)
        - pawn_status (str): Statut du pion. (Alive, Dead)
        - pawn_owner (int): Identifiant du joueur possédant le pion.
        - pawn_row (int): Ligne où se trouve le pion. La ligne attribuée par défaut est la ligne où se trouve le pion au commencement de la partie.
        - pawn_col (str): Colonne où se trouve le pion. La colonne attribuée par défaut est la colonne où se trouve le pion au commencement de la partie.
        - pawn_pos (list[int, str]): Position où se trouve le pion. La position attribuée par défaut est la position où se trouve le pion au commencement de la partie.
        - pawn_gui (pygame.Rect): Representation graphique du pion avec pygame.

        Args:
            layer (int): Nombre de lignes de pions à créer.

        Returns:
            list[dict]: Liste de dictionnaires représentant les pions du joueur.
        """        
        player_pawns: list[dict] = []
        for cell in self.board:
            pawn_informations: dict = {}
            if self.player_id == 1 and cell["cell_row"] > constants.BOARD_SIZE-(layer+1) and cell["cell_color"] == "B":
                pawn_informations["pawn_type"] = "Pawn"
                pawn_informations["pawn_color"] = "W"
                pawn_informations["pawn_status"] = "alive"
                pawn_informations["pawn_owner"] = self.player_id
                pawn_informations["pawn_row"] = cell["cell_row"]
                pawn_informations["pawn_col"] = cell["cell_col"]
                pawn_informations["pawn_pos"] = list(cell["cell_index"])
                pawn_informations["pawn_gui"] = None
                player_pawns.append(pawn_informations)
                
                cell["cell_is_empty"] = False
                cell["cell_owner"] = self.player_id
            elif self.player_id == 2 and cell["cell_row"] < layer and cell["cell_color"] == "B":
                pawn_informations["pawn_color"] = "B"
                pawn_informations["pawn_type"] = "Pawn"
                pawn_informations["pawn_status"] = "alive"
                pawn_informations["pawn_owner"] = self.player_id
                pawn_informations["pawn_row"] = cell["cell_row"]
                pawn_informations["pawn_col"] = cell["cell_col"]
                pawn_informations["pawn_pos"] = list(cell["cell_index"])
                pawn_informations["pawn_gui"] = None
                player_pawns.append(pawn_informations)
                
                cell["cell_is_empty"] = False
                cell["cell_owner"] = self.player_id
        return player_pawns

    def get_pawn(self, pawns: list[dict], pawn_pos: list[int, str]) -> tuple[dict, int]:
        """_summary_ : Récupération du pion à la position donnée. (ligne, colonne)

        Args:
            pawns (list[dict]): Liste de dictionnaires représentant les pions du joueur.
            pawn_pos (list[int, str]): Position où se trouve le pion. (ligne, colonne)

        Returns:
            tuple[dict, int]: Tuple contenant le pion à la position donnée (ligne, colonne) et son index dans la liste de pions.
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
    
    def get_valid_moves(self, pawn: tuple[dict, int], board: Board) -> dict:
        """_summary_ : Récupération des coups valides pour le pion donné.

        Args:
            pawn (tuple[dict, int]): Tuple contenant le pion (ses informations) à la position donnée (ligne, colonne) et son index dans la liste de pions.
            board (Board): instance de la classe Board.

        Returns:
            dict: Dictionnaire contenant les coups valides pour le pion donné.
        """        
        moves: dict = {}
        left: int = constants.BOARD_COLUMNS.index(pawn[0]["pawn_col"]) - 1
        right: int = constants.BOARD_COLUMNS.index(pawn[0]["pawn_col"]) + 1
        row: int = pawn[0]["pawn_row"]
        
        if pawn[0]["pawn_owner"] == 1 or pawn[0]["pawn_type"] == "King":
            moves.update(self.path(row-1, max(row-3, -1), -1, board, left, "left", skipped=[]))
            moves.update(self.path(row-1, max(row-3, -1), -1, board, right, "right", skipped=[]))
        
        if pawn[0]["pawn_owner"] == 2 or pawn[0]["pawn_type"] == "King":
            moves.update(self.path(row+1, min(row+3, constants.BOARD_SIZE), 1, board, left, "left", skipped=[]))
            moves.update(self.path(row+1, min(row+3, constants.BOARD_SIZE), 1, board, right, "right", skipped=[]))
        
        # Garde uniquement le meilleur coup possible (si existant)
        move_max_length: int = 0
        best_moves_keys: dict = {}
        for move in moves:
            if len(moves[move]) > move_max_length:
                move_max_length = len(moves[move])
                best_moves_keys[move] = moves[move]
            elif move_max_length > 0 and len(moves[move]) == move_max_length:
                best_moves_keys[move] = moves[move]

        if best_moves_keys:
            return best_moves_keys
        
        return moves
    
    def path(self, start: int, stop: int, vertical_direction: int, board: Board, horizontal_direction: int, horizontal_direction_indicator: str, skipped: list = []) -> dict:     
        moves: dict = {}
        last: list = []
        
        for row in range(start, stop, vertical_direction):
            if horizontal_direction < 0 or horizontal_direction >= len(constants.BOARD_COLUMNS):
                break
            
            current_cell: tuple[dict, int] = board.get_cell(board.board, (row, constants.BOARD_COLUMNS[horizontal_direction]))
            if current_cell[0]["cell_is_empty"] == True:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, constants.BOARD_COLUMNS[horizontal_direction])] = last + skipped
                else:
                    moves[(row, constants.BOARD_COLUMNS[horizontal_direction])] = last
                
                if last:
                    if vertical_direction == -1:
                        row_range: int = max(row-3, -1)
                    else:
                        row_range: int = min(row+3, constants.BOARD_SIZE)
                    moves.update(self.path(row+vertical_direction, row_range, vertical_direction, board, horizontal_direction-1, "left", skipped=last))
                    moves.update(self.path(row+vertical_direction, row_range, vertical_direction, board, horizontal_direction+1, "right",skipped=last))
                break
            elif current_cell[0]["cell_owner"] == self.player_id:
                break
            else:
                last: list = [current_cell]
            
            if horizontal_direction_indicator == "right":
                horizontal_direction += 1
            elif horizontal_direction_indicator == "left":
                horizontal_direction -= 1
        
        return moves

    def move_pawn(self, pawn: tuple[dict, int], move_to: tuple[int, str], reachable_cells_by_pawn: dict, ennemy_pawns: list[dict], board: Board) -> bool:
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
                pawn[0]["pawn_gui"].x = destination_cell[0]["cell_gui"].x+constants.GUI_CELL_SIZE//2
                pawn[0]["pawn_gui"].y = destination_cell[0]["cell_gui"].y+constants.GUI_CELL_SIZE//2
                
                if self.player_id == 1 and pawn[0]["pawn_row"] == 0:
                    pawn[0]["pawn_type"] = "King"
                elif self.player_id == 2 and pawn[0]["pawn_row"] == constants.BOARD_SIZE-1:
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
                pawn[0]["pawn_gui"].x = destination_cell[0]["cell_gui"].x+constants.GUI_CELL_SIZE//2
                pawn[0]["pawn_gui"].y = destination_cell[0]["cell_gui"].y+constants.GUI_CELL_SIZE//2
                
                if self.player_id == 1 and pawn[0]["pawn_row"] == 0:
                    pawn[0]["pawn_type"] = "King"
                elif self.player_id == 2 and pawn[0]["pawn_row"] == constants.BOARD_SIZE-1:
                    pawn[0]["pawn_type"] = "King"
            
            return True
        else:
            return False

    def take_pawn(self, pawns: list[dict], pawn_pos: list[int, str]) -> None:
        pawn_to_take: tuple[dict, int] = self.get_pawn(pawns, pawn_pos)
        if None not in pawn_to_take:
            pawn_to_take[0]["pawn_status"] = "dead"
            pawn_to_take[0]["pawn_row"] = None
            pawn_to_take[0]["pawn_col"] = None
            pawn_to_take[0]["pawn_pos"] = None
            pawn_to_take[0]["pawn_gui"] = None



if __name__ == "__main__":
    board = Board(constants.BOARD_SIZE, constants.BOARD_COLUMNS)
    pawn = Pawns(1, board.board)
    pawn2 = Pawns(2, board.board)
    
    print("\n")
    
    print(pawn.get_valid_moves(pawn.get_pawn(pawn.player_pawns, [6, "F"]), board))
    
    #print(pawn.paths((5, "E"), board))