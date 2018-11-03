from src.tile_list import *
class Tile:

    def __init__(self, symbol, visible, image=None):
        self.symbol = symbol
        self.image = image
        self.visible = visible
        self.explored = False

    def draw(self):
        print(self.symbol, end='')
