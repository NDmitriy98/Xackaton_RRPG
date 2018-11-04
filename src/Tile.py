from src.tile_list import *
import src.tile_list as tl
from src.Settings import *
class Tile:

    def __init__(self, symbol, visible):
        self.symbol = symbol
        self.image = symbol
        self.visible = visible
        self.explored = False

    def draw(self,x, y, display, camera, images):
        self.image = images[self.symbol]
        result = camera.apply(Block(x, y))
        if self.check_coords(result.x, result.y):
            display.blit(self.image, (result.x, result.y))

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

    def check_coords(self, x, y):
        if WIN_WIDTH > x > -BLOCK_WIDTH:
            if WIN_HEIGHT > y > -BLOCK_HEIGHT:
                return True
        return False
