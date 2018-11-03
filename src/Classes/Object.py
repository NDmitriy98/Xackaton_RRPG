from src.Tile import Tile


class Object:
    def __init__(self, x=0, y=0, img=None):
        self.x = x
        self.y = y
        self.img = img
        self.info = "Object"
        tile = Tile("", True)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        self.tile.draw()

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_info(self):
        return self.info