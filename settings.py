from enum import Enum

RES = WIDTH, HEIGHT = (1200, 800)
FPS = 100
TILE = 30
ROWS = HEIGHT // TILE
COLS = WIDTH // TILE

class State(Enum):

    UNVISITED = 'white'
    START = '#71DE5F'
    FINISH = 'gold'
    WALL = 'red'
    VISITED = 'blue'
    PATH = 'yellow'