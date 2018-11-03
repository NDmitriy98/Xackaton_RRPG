from pygame.rect import Rect

from src.Classes import Object


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        #print("apply " + str(self.state.x) + " " + str(self.state.y) )
        return target.rect.move(self.state.topleft)

    def update(self, target):
        print("update " + str(self.state.x) + " " + str(self.state.y))
        self.state = self.camera_func(self.state, target.rect)
