# DEPENDENCIES
from Game import Game
from constants import *
from typing import *

def main() -> None:
    print("SERVER IP : ")
    server_ip: str = input()
    Game(server_ip).gameloop()

if __name__ == "__main__":
    main()