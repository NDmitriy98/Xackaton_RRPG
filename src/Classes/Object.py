from pygame import sprite
from pygame.rect import Rect

from src import Settings
from src.Tile import Tile


class Object(sprite.Sprite):
    def __init__(self, x=0, y=0, img=None):
        self.x = x
        self.y = y
        self.img = img
        self.info = "Object"
        self.rect = Rect(self.x, self.y, Settings.BLOCK_WIDTH, Settings.BLOCK_HEIGHT)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_x(self):
        return self.rect.x

    def set_x(self, x):
        self.rect.x = x

    def get_y(self):
        return self.rect.y

    def set_y(self, y):
        self.rect.y = y

    def get_info(self):
        return self.info
