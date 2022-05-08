from constants import *
import sys, os, signal

class GUI:
    
    def __init__(self) -> None:
        pygame.init()
    
    def draw_gui_pawns(self, screen: pygame.Surface, pawns: list[dict]) -> None:
        """_summary_ : Dessine la représentation graphique des pions à l'écran

        Args:
            screen (pygame.Surface): la surface sur laquelle on dessine les pions
            pawns (list[dict]): la liste des pions
        """           
        for pawn in pawns:
            if pawn["pawn_gui"] != None:
                if pawn["pawn_type"] == "Pawn":
                    color: tuple[int, int, int] = GUI_PAWN_COLOR_1 if pawn["pawn_owner"] == 1 else GUI_PAWN_COLOR_2
                elif pawn["pawn_type"] == "King":
                    color: tuple[int, int, int] = GUI_KING_COLOR_1 if pawn["pawn_owner"] == 1 else GUI_KING_COLOR_2
                pygame.draw.circle(screen, color, (pawn["pawn_gui"].x, pawn["pawn_gui"].y), pawn["pawn_gui"].width)
    
    def gui_pawns(self, pawns: list[dict], board: list[dict]) -> None:
        """_summary_: Ajoute une représentation graphique aux pions

        Args:
            pawns (list[dict]): la liste des pions
            board (list[dict]): la (la liste des cellules de la board)
        """        
        for pawn in pawns:
            for cell in board:
                if cell["cell_row"] == pawn["pawn_row"] and cell["cell_col"] == pawn["pawn_col"]:
                    pawn_gui_position: tuple[int, int] = (cell["cell_gui"].x+GUI_CELL_SIZE//2, cell["cell_gui"].y+GUI_CELL_SIZE//2)
                    pawn_gui_size: tuple[int, int] = (GUI_PAWN_SIZE, GUI_PAWN_SIZE)
                    pawn["pawn_gui"] = pygame.Rect(pawn_gui_position, pawn_gui_size)
    
    def gui_board(self, board: list[dict]) -> None:
        """_summary_: Ajoute une représentation graphique aux cellules de la board.

        Args:
            board (list[dict]): la board (la liste des cellules de la board)
        """               
        for cell_dict in board:
            cell_gui_position: tuple[int, int] = (BOARD_COLUMNS.index(cell_dict["cell_col"]) * GUI_CELL_SIZE, cell_dict["cell_row"] * GUI_CELL_SIZE)
            cell_gui_size: tuple[int, int] = (GUI_CELL_SIZE, GUI_CELL_SIZE)
            cell_dict["cell_gui"] = pygame.Rect(cell_gui_position, cell_gui_size) # create the gui of the cell, the gui is a rectangle
    
    def draw_gui_board(self, screen: pygame.Surface, board: list[dict]) -> None:
        """_summary_: Dessine la représentation graphique de la board à l'écran

        Args:
            screen (pygame.Surface): la surface sur laquelle on dessine la board
            board (list[dict]): la liste des cellules de la board (la board)
        """              
        for cell_dict in board:
            color: tuple[int, int, int] = GUI_CELL_COLOR_1 if cell_dict["cell_color"] == CELL_COLOR_1 else GUI_CELL_COLOR_2
            pygame.draw.rect(screen, color, cell_dict["cell_gui"])
    
    def draw_gui_reachable_cells(self, screen: pygame.Surface, reachable_cells_by_pawn: dict, selected_pawn: tuple[dict, int], board) -> None:
        """_summary_: Dessine un indicateur (petit cercle) sur les cellules accessibles par le pion sélectionné

        Args:
            screen (pygame.Surface): la surface sur laquelle on dessine les cellules accessibles
            reachable_cells_by_pawn (dict): les cellules accessibles par le pion sélectionné
            selected_pawn (tuple[dict, int]): le pion sélectionné
            board (Board): instance de la classe Board
        """              
        if reachable_cells_by_pawn:
            for move in reachable_cells_by_pawn:
                row, col = move
                reachable_cell_gui_indicator_color: tuple[int, int, int] = GUI_PAWN_COLOR_1 if selected_pawn[0]["pawn_owner"] == 1 else GUI_PAWN_COLOR_2
                reachable_cell_gui_indicator_position: tuple[int, int] = (board.get_cell(board.board, (row, col))[0]["cell_gui"].x+GUI_CELL_SIZE//2, board.get_cell(board.board, (row, col))[0]["cell_gui"].y+GUI_CELL_SIZE//2)
                reachable_cell_gui_indicator_size: int = 10
                pygame.draw.circle(screen, reachable_cell_gui_indicator_color, reachable_cell_gui_indicator_position, reachable_cell_gui_indicator_size)
    
    def event_gui_close_game(self, event: pygame.event, game_pid: int = None) -> None:
        """_summary_: Quitte le jeu en cas de clic sur la croix de la fenêtre.

        Args:
            event (pygame.event): l'évènement
            game_pid (int, optional): PID du jeu. Defaults to None.
        """        
        if event.type == pygame.QUIT:
            pygame.quit()
            if game_pid is not None:
                os.kill(game_pid, signal.SIGKILL)
            sys.exit()
    
    def gui_label(self, screen: pygame.Surface, text: str, position: tuple[int, int], font: str, size: int, color: tuple[int, int, int]) -> None:
        """_summary_: Dessine un label à l'écran

        Args:
            screen (pygame.Surface): la surface sur laquelle on dessine le label
            text (str): le texte du label
            position (tuple[int, int]): la position du label
            font (str): la police du label
            size (int): la taille du label
            color (tuple[int, int, int]): la couleur du label
        """               
        label_font = pygame.font.Font(font, size)
        label_text = label_font.render(text, True, color)
        label_rect = label_text.get_rect()
        label_rect.center = position
        screen.blit(label_text, label_rect)
    
    def gui_button(self, screen: pygame.Surface, text: str, position: tuple[int, int], font: str, size: int, color: tuple[int, int, int], background_color: tuple[int, int, int]) -> pygame.Rect:
        """_summary_: Dessine un bouton à l'écran

        Args:
            screen (pygame.Surface): la surface sur laquelle on dessine le bouton
            text (str): le texte du bouton
            position (tuple[int, int]): la position du bouton
            font (str): la police du bouton
            size (int): la taille du bouton
            color (tuple[int, int, int]): la couleur du texte du bouton
            background_color (tuple[int, int, int]): la couleur de fond du bouton

        Returns:
            pygame.Rect: le rectangle du bouton
        """             
        button_font = pygame.font.Font(font, size)
        button_text = button_font.render(text, True, color)
        button_rect = button_text.get_rect()
        button_rect.center = position
        pygame.draw.rect(screen, background_color, button_rect)
        screen.blit(button_text, button_rect)
        return button_rect
    
    def gui_user_input_field(self, screen: pygame.Surface, text: str, position: tuple[int, int], input_width: int, input_height: int, font: str, size: int, color: tuple[int, int, int], background_color: tuple[int, int, int]) -> None:
        """_summary_: Dessine un champ de saisie à l'écran

        Args:
            screen (pygame.Surface): la surface sur laquelle on dessine le champ de saisie
            text (str): le texte du champ de saisie
            position (tuple[int, int]): la position du champ de saisie
            input_width (int): la largeur du champ de saisie
            input_height (int): la hauteur du champ de saisie
            font (str): la police du texte du champ de saisie
            size (int): la taille du texte du champ de saisie
            color (tuple[int, int, int]): la couleur du texte du champ de saisie
            background_color (tuple[int, int, int]): la couleur de fond du champ de saisie
        """               
        user_input_field_font = pygame.font.Font(font, size)
        user_input_field_text = user_input_field_font.render(text, True, color)
        user_input_field_rect = pygame.Rect(position[0],position[1],input_width,input_height)
        user_input_field_rect.center = position
        pygame.draw.rect(screen, background_color, user_input_field_rect)
        screen.blit(user_input_field_text, (user_input_field_rect.x+10, user_input_field_rect.y+3))
    
    def gui_window_update(self, window: pygame.Surface, color: tuple[int, int, int], clock: pygame.time.Clock, show_fps: bool) -> None:
        """_summary_: Met à jour la fenêtre

        Args:
            window (pygame.Surface): la surface de la fenêtre
            color (tuple[int, int, int]): la couleur de fond de la fenêtre
            clock (pygame.time.Clock): le temps
            show_fps (bool): affiche ou non les FPS dans le terminal
        """        
        pygame.display.update()
        window.fill(color)
        print(clock.get_fps()) if show_fps else None
    
    def gui_start_menu_screen(self) -> str:
        """_summary_: Affiche le menu de démarrage

        Returns:
            str: le texte saisi par l'utilisateur
        """        
        user_text: str = ""
        while True:
            mouse_position: tuple[int, int] = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
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
            
            self.gui_label(WINDOW, START_MENU_TITLE, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-125), None, 45, BLACK)
            self.gui_label(WINDOW, START_MENU_SUBTITLE, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-90), None, 28, BLACK)
            self.gui_user_input_field(WINDOW, user_text, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-25), 240, 35, None, 35, WHITE, BLACK)
            join_button_rect = self.gui_button(WINDOW, START_MENU_JOIN_BUTTON_TEXT, (WINDOW_SIZE[0]/2,WINDOW_SIZE[1]/2+25), None, 45, WHITE, BLACK)

            CLOCK.tick(FPS)
            self.gui_window_update(WINDOW, WHITE, CLOCK, False)
    
    def gui_player_has_left_screen(self, game_pid: int) -> None:
        """_summary_: Affiche le message de départ d'un joueur

        Args:
            game_pid (int): PID du jeu
        """        
        while True:
            for event in pygame.event.get():
                self.event_gui_close_game(event, game_pid)
            
            self.gui_label(WINDOW, "UN JOUEUR A SUBITEMENT QUITTÉ LA PARTIE", (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), None, 25, BLACK)
            self.gui_label(WINDOW, "QUITTEZ ET RELANCEZ LE JEU", (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2+25), None, 25, BLACK)
            
            CLOCK.tick(FPS)
            self.gui_window_update(WINDOW, WHITE, CLOCK, False)
    
    def gui_winner_screen(self, winner: str, game_pid: int) -> None:
        """_summary_: Affiche le message de victoire d'un joueur

        Args:
            winner (str): le nom du gagnant
            game_pid (int): PID du jeu
        """        
        while True:
            for event in pygame.event.get():
                self.event_gui_close_game(event, game_pid)
            
            self.gui_label(WINDOW, winner, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), None, 45, BLACK)
            
            CLOCK.tick(FPS)
            self.gui_window_update(WINDOW, WHITE, CLOCK, False)
    