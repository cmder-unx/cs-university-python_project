# DEPENDENCIES
from sys import argv
from Game import Game
from constants import *
from typing import *

def main() -> None:
    print("SERVER IP : ")
    server_ip: str = input() if len(argv) == 1 else argv[1]
    Game(server_ip).gameloop()

if __name__ == "__main__":
    main()