from pygame.rect import Rect

from src.Classes import Object


class Camera(object):
    def __init__(self, width, height, x=0, y=0):
        self.width = 800
        self.height = 600
        self.x = 0
        self.y = 0
    def apply(self, character):
        character.x = self.width/2
        character.y = self.height/2


    def update(self, obj: Object.Object):
        obj.set_pos(obj.x+self.width/2, obj.y + self.height/2)
