from src.tile_list import *
import src.tile_list as tl
from src.Settings import *
class Tile:

    def __init__(self, symbol, visible):
        self.symbol = symbol
        self.image = symbol
        self.visible = visible
        self.explored = False

    def draw(self,x, y, display, camera):
        self.image = self.symbol
        img = pg.image.load(self.image)
        block = Block(x, y)
        display.blit(img, camera.apply(block))

    def debug_draw(self):
        s = ''
        if self.symbol == tl.FLOOR_TILE:
            s = '-'
        elif self.symbol == tl.WALL_TILE:
            s = '#'
        elif self.symbol == tl.ROAD_TILE:
            s = 'R'
        elif self.symbol == tl.BACK_TILE:
            s = ' '
        elif self.symbol == tl.DOOR_TILE:
            s = 'D'
        print(s, end='')


