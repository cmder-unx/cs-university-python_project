# DEPENDENCIES
import pygame, sys
from Board import Board
from Pawns import Pawns
from Game import Game
from constants import *
from typing import *

def main() -> None:
    Game().gameloop()

if __name__ == "__main__":
    main()