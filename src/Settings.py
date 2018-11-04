import pygame as pg
from pygame.rect import Rect


WIN_WIDTH = 1024
WIN_HEIGHT = 680
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)


BACKGROUND_COLOR = (0, 255, 255)

BLOCK_WIDTH = 50
BLOCK_HEIGHT = 50
SPEED = 5

GAME_VERSION = "alpha 0.1"








class Block(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(BACKGROUND_COLOR)
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)