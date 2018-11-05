from pygame import sprite
from pygame.rect import Rect

from src import Settings
from src.Tile import Tile


class Object(sprite.Sprite):
    def __init__(self, x=0, y=0, img=None):
        super().__init__()
        self.x = x
        self.y = y
        self.img = img
        self.tile = Tile("O", False)
        self.info = "Object"
        self.rect = Rect(self.x, self.y, Settings.BLOCK_WIDTH, Settings.BLOCK_HEIGHT)

    def __del__(self):
        print ("deling", self)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_rect(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_rect_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


    def get_rect_x(self):
        return self.rect.x

    def get_rect_y(self):
        return self.rect.y

    def get_info(self):
        return self.info
