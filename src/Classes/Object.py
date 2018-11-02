from src.Tile import Tile


class Object:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.info = "Object"
        tile = Tile("", True)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        self.tile.draw()