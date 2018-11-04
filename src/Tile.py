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
        print(self.symbol, end='')

    def check_coords(self, x, y):
        if WIN_WIDTH > x > -BLOCK_WIDTH:
            if WIN_HEIGHT > y > -BLOCK_HEIGHT:
                return True
        return False
