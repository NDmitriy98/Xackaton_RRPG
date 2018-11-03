import pygame as pg
from pygame.rect import Rect

from src.Camera import Camera
from src.Classes import *


WIN_WIDTH = 800
WIN_HEIGHT = 600
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = (0, 255, 255)

BLOCK_WIDTH = 50
BLOCK_HEIGHT = 50


class Block(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(BACKGROUND_COLOR)
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы
    return Rect(l, t, w, h)


def cartensian_to_iso(x, y):
    return x - y, (x + y) / 2


def main():



    delta_x = 0
    delta_y = 0

    start_x = 0
    start_y = 0

    pg.init()
    display = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pg.display.set_caption('RRPG alpha 0.1')
    bg = pg.Surface((WIN_WIDTH, WIN_HEIGHT))
    ##########################
    hero = Character.Character()
    hero.set_pos(100, WIN_HEIGHT / 2)
    ##########################
    # entities = pg.sprite.Group()
    # platforms = []
    # entities.add(hero)
    entities = pg.sprite.Group()
    #entities.add(hero)

    map = [
        "##########################",
        "#--###---###############",
        "#--###-------############",
        "#--#########-############",
        "#--------------##########",
        "#####-#######--##########",
        "#####-###################",
        "####---##################",
        "#########################"
    ]
    clock = pg.time.Clock()

    hero.img = pg.image.load('Drawable/1.png')
    wallimg = pg.image.load('Drawable/wall.png')
    floorimg = pg.image.load('Drawable/floor.png')

    total_level_width = len(map[0]) * BLOCK_WIDTH
    total_level_height = len(map) * BLOCK_HEIGHT
    print("full: " + str(total_level_width), " " + str(total_level_height))
    camera = Camera(camera_configure, total_level_width, total_level_height)

    crashed = False

    step_x = 0
    step_y = 0
    speed = 5

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

                delta_x = pos[0] - hero.x
                delta_y = pos[1] - hero.y

                start_x = -delta_x
                start_y = -delta_y

                #print("x = " + str(hero.x) + " delta = " + str(delta_x) + " click to " + str(pos[0]))
                #print("y = " + str(hero.y) + " delta = " + str(delta_y) + " click to " + str(pos[1]))

                hero.set_pos(pos[0], pos[1])
                hero.rect = Rect(pos[0], pos[1], WIN_WIDTH, WIN_HEIGHT)

        hero.move(step_x, step_y)


        display.fill(BACKGROUND_COLOR)

        bl = Block(0,0)
        #print("before" + str(camera.apply(bl).x) + " " + str(camera.apply(bl).y))
        camera.update(hero)
        #print("after" + str(camera.apply(bl).x) + " " + str(camera.apply(bl).y))
        x = y = 0
        for row in map:
            for col in row:
                if col == '#':
                    block = Block(x, y)
                    display.blit(wallimg, camera.apply(block))
                if col == '-':
                    block = Block(x, y)
                    display.blit(floorimg, camera.apply(block))
                x += BLOCK_WIDTH
            y += BLOCK_HEIGHT
            x = 0

        block = Block(hero.x, hero.y)
        display.blit(hero.img, camera.apply(block))

        pg.display.update()
        clock.tick(60)
    pg.quit()
    quit()


if __name__ == "__main__":
    main()