# DEPENDENCIES
from sys import argv
from Game import Game
from constants import *
from typing import *
from GUI import GUI
import os

def main() -> None:
    server_ip: str = GUI().gui_start_menu() if len(argv) == 1 else argv[1]
    game_pid: int = os.getpid()
    Game(server_ip, game_pid).gameloop()

if __name__ == "__main__":
    main()