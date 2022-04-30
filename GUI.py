from constants import *

class GUI:
    
    def draw_gui_pawns(self, screen: pygame.Surface, pawns: list[dict]) -> None:
        """_summary_: this function will draw the gui for the pawns

        Args:
            screen (pygame.Surface): the screen where we want to draw the gui for the pawns, here the screen will be WINDOW constant, see constants.py for more info
            pawns (list[dict]): the list of pawns
        """        
        for pawn in pawns:
            if pawn["pawn_gui"] != None:
                if pawn["pawn_type"] == "Pawn":
                    color: tuple[int, int, int] = GUI_PAWN_COLOR_1 if pawn["pawn_owner"] == 1 else GUI_PAWN_COLOR_2
                elif pawn["pawn_type"] == "King":
                    color: tuple[int, int, int] = GUI_KING_COLOR_1 if pawn["pawn_owner"] == 1 else GUI_KING_COLOR_2
                pygame.draw.circle(screen, color, (pawn["pawn_gui"].x, pawn["pawn_gui"].y), pawn["pawn_gui"].width)
    
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
    
    def draw_gui_reachable_cells(self, screen: pygame.Surface, reachable_cells_by_pawn: dict, selected_pawn: tuple[dict, int], board) -> None:
        """_summary_: this function will draw the reachable cells

        Args:
            screen (pygame.Surface): the screen where we want to draw the reachable cells, here the screen will be WINDOW constant, see constants.py for more info
            reachable_cells_by_pawn (dict): the dict of reachable cells
        """        
        if reachable_cells_by_pawn:
            for move in reachable_cells_by_pawn:
                row, col = move
                reachable_cell_gui_indicator_color: tuple[int, int, int] = GUI_PAWN_COLOR_1 if selected_pawn[0]["pawn_owner"] == 1 else GUI_PAWN_COLOR_2
                reachable_cell_gui_indicator_position: tuple[int, int] = (board.get_cell(board.board, (row, col))[0]["cell_gui"].x+GUI_CELL_SIZE//2, board.get_cell(board.board, (row, col))[0]["cell_gui"].y+GUI_CELL_SIZE//2)
                reachable_cell_gui_indicator_size: int = 10
                pygame.draw.circle(screen, reachable_cell_gui_indicator_color, reachable_cell_gui_indicator_position, reachable_cell_gui_indicator_size)