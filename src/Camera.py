from pygame.rect import Rect

from src.Classes import Object


class Camera(object):
    def __init__(self, width, height):
        self.camera = Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.coefficient_x = 0
        self.coefficient_y = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)



    def update(self, target):
        x = -target.rect.x + int(400)
        y = -target.rect.y + int(300)
        self.camera = Rect(x, y, self.width, self.height)
