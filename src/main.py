import pygame as pg
from pygame.rect import Rect

from src.Camera import Camera
from src.Classes import *


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+display_width / 2, -t+display_height / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-display_width), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-display_height), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)






pg.init()

display_width = 800
display_height = 600

PLATFORM_WIDTH = 12
PLATFORM_HEIGHT = 12

map = [
    "###############",
    "#--###---######",
    "#--###-------##",
    "#--#########-##",
    "#------------##",
    "#####-#########",
    "#####-#########",
    "####---########",
    "###############"
]

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('RRPG alpha 0.1')
clock = pg.time.Clock()

character = Character.Character()
character.img = pg.image.load('Drawable/1.png')
wallimg = pg.image.load('Drawable/wall.png')
floorimg = pg.image.load('Drawable/floor.png')


step_x = 0
step_y = 0
speed = 5

total_level_width = len(map[0])*PLATFORM_WIDTH
total_level_height = len(map)*PLATFORM_HEIGHT
camera = Camera(total_level_width, total_level_height)

def drawChar():
    gameDisplay.blit(character.img, (character.x, character.y))


def drawMap():
    x = 0
    y = 0
    for row in map:
        for col in row:
            if col == '#':
                gameDisplay.blit(wallimg, (x, y))
            if col == '-':
                gameDisplay.blit(floorimg, (x, y))
            x += 50
        y += 50
        x = 0

crashed = False

while not crashed:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                crashed = True
            if event.key == pg.K_d:
                step_x = speed
            if event.key == pg.K_a:
                step_x = -speed
            if event.key == pg.K_w:
                step_y = -speed
            if event.key == pg.K_s:
                step_y = speed

        if event.type == pg.KEYUP:
            if event.key == pg.K_d or event.key == pg.K_a or event.key == pg.K_w or event.key == pg.K_s:
                step_x = 0
                step_y = 0

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()



            character.set_pos(pos[0] - 25, pos[1] - 25)


    character.move(step_x, step_y)

    gameDisplay.fill(white)
    drawMap()
    drawChar()
    pg.display.update()
    clock.tick(60)

pg.quit()
quit()
