from constants import *
import sys, os, signal

class GUI:
    
    def __init__(self) -> None:
        pygame.init()
    
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
    
    def event_gui_close_game(self, event: pygame.event, game_pid: int = None) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            if game_pid is not None:
                os.kill(game_pid, signal.SIGKILL)
            sys.exit()
    
    def gui_label(self, screen: pygame.Surface, text: str, position: tuple[int, int], font: str, size: int, color: tuple[int, int, int]) -> None:
        """_summary_: this function will create a label on the screen

        Args:
            screen (pygame.Surface): the screen where we want to draw the label, here the screen will be WINDOW constant, see constants.py for more info
            text (str): the text of the label
            position (tuple[int, int]): the position of the label
            size (int): the size of the label
            color (tuple[int, int, int]): the color of the label
            font (str): the font of the label
        """        
        label_font = pygame.font.Font(font, size)
        label_text = label_font.render(text, True, color)
        label_rect = label_text.get_rect()
        label_rect.center = position
        screen.blit(label_text, label_rect)
    
    def gui_button(self, screen: pygame.Surface, text: str, position: tuple[int, int], font: str, size: int, color: tuple[int, int, int], background_color: tuple[int, int, int]) -> pygame.Rect:
        """_summary_: this function will create a button on the screen

        Args:
            screen (pygame.Surface): the screen where we want to draw the button, here the screen will be WINDOW constant, see constants.py for more info
            text (str): the text of the button
            position (tuple[int, int]): the position of the button
            size (int): the size of the button
            color (tuple[int, int, int]): the color of the button
            background_color (tuple[int, int, int]): the background color of the button
        """        
        button_font = pygame.font.Font(font, size)
        button_text = button_font.render(text, True, color)
        button_rect = button_text.get_rect()
        button_rect.center = position
        pygame.draw.rect(screen, background_color, button_rect)
        screen.blit(button_text, button_rect)
        return button_rect
    
    def gui_user_input_field(self, screen: pygame.Surface, text: str, position: tuple[int, int], input_width: int, input_height: int, font: str, size: int, color: tuple[int, int, int], background_color: tuple[int, int, int]) -> None:
        """_summary_: this function will create a user input field on the screen

        Args:
            screen (pygame.Surface): the screen where we want to draw the user input field, here the screen will be WINDOW constant, see constants.py for more info
            text (str): the text of the user input field
            position (tuple[int, int]): the position of the user input field
            size (int): the size of the user input field
            color (tuple[int, int, int]): the color of the user input field
            font (str): the font of the user input field
        """        
        user_input_field_font = pygame.font.Font(font, size)
        user_input_field_text = user_input_field_font.render(text, True, color)
        user_input_field_rect = pygame.Rect(position[0],position[1],input_width,input_height)
        user_input_field_rect.center = position
        pygame.draw.rect(screen, background_color, user_input_field_rect)
        screen.blit(user_input_field_text, (user_input_field_rect.x+10, user_input_field_rect.y+3))
    
    def window_update(self, window: pygame.Surface, color: tuple[int, int, int], clock: pygame.time.Clock, show_fps: bool) -> None:
        """_summary_: Update the window

        Args:
            window (pygame.Surface): The window to update
            color (tuple[int, int, int]): The color used to update the window
            clock (pygame.time.Clock): The clock used to get the framerate of the window
            show_fps (bool): If True, the framerate of the window will be print in the console
        """
        pygame.display.update()
        window.fill(color)
        print(clock.get_fps()) if show_fps else None
    
    def gui_start_menu_screen(self) -> str:
        titre = "Jeu de Dames !"
        ordre = "Entre ton adresse réseau local pour jouer avec un ami (si tu en as)"
        join_button_text = "Rejoindre"
        user_text: str = "" #Ce qui sera saisi par l'utilisateur
        while True:
            mouse_position: tuple[int, int] = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        #Pour pouvoir utiliser la touche Effacer
                        user_text=user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(user_text) > 0:
                            return user_text
                    elif len(user_text) < 15:
                        if event.unicode.isdigit() or event.unicode == ".":
                            user_text += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if join_button_rect.collidepoint(mouse_position):
                        if len(user_text) > 0:
                            return user_text
                self.event_gui_close_game(event)
            
            self.gui_label(WINDOW, titre, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-125), None, 45, BLUE)
            self.gui_label(WINDOW, ordre, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-90), None, 28, BLUE)
            self.gui_user_input_field(WINDOW, user_text, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-25), 240, 35, None, 35, WHITE, BLUE)
            join_button_rect = self.gui_button(WINDOW, join_button_text, (WINDOW_SIZE[0]/2,WINDOW_SIZE[1]/2+25), None, 45, WHITE, GREEN)

            CLOCK.tick(FPS)
            self.window_update(WINDOW, BLACK, CLOCK, False)
    
    def gui_player_has_left_screen(self, game_pid: int) -> None:
        while True:
            for event in pygame.event.get():
                self.event_gui_close_game(event, game_pid)
            
            self.gui_label(WINDOW, "A PLAYER HAS LEFT", (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), None, 45, WHITE)
            
            CLOCK.tick(FPS)
            self.window_update(WINDOW, BLACK, CLOCK, False)
    
    def gui_winner_screen(self, winner: str, game_pid: int) -> None:
        while True:
            for event in pygame.event.get():
                self.event_gui_close_game(event, game_pid)
            
            self.gui_label(WINDOW, winner+" WON", (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), None, 45, WHITE)
            
            CLOCK.tick(FPS)
            self.window_update(WINDOW, BLACK, CLOCK, False)
    