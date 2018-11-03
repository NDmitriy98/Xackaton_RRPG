import pygame as pg
from pygame.rect import Rect

from src.Settings import *
from src.Camera import Camera
from src.Classes import *



def main():

    temp_x = 0
    temp_y = 0

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
    camera = Camera(total_level_width, total_level_height)

    all_sprites = pg.sprite.Group()
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

                block_x = int(pos[0]/BLOCK_WIDTH)
                block_y = int(pos[1]/BLOCK_HEIGHT)

                pixels_x = block_x * BLOCK_WIDTH
                pixels_y = block_y * BLOCK_HEIGHT



                result = camera.apply(Block(pixels_x, pixels_y))
                print("mouse " + str(result.x))

                #hero.set_pos(pixels_x, pixels_y)
                #hero.rect = Rect(result.x, result.y, WIN_WIDTH, WIN_HEIGHT)
                hero.rect = Rect(pixels_x - temp_x, pixels_y - temp_y, BLOCK_WIDTH, BLOCK_HEIGHT)
        hero.move(step_x, step_y)


        display.fill(BACKGROUND_COLOR)

        bl = Block(0,0)
        #print("before" + str(camera.apply(bl).x) + " " + str(camera.apply(bl).y))
        all_sprites.update()
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

        print("map " + str(camera.apply(Block(0, 0)).x))
        temp_x = camera.apply(Block(0, 0)).x
        temp_y = camera.apply(Block(0, 0)).y

        #all_sprites.add(hero)
        #block = Block(hero.rect.x, hero.rect.y)

        display.blit(hero.img, camera.apply(hero))


        print("temp x_y " + str(temp_x) + " " + str(temp_y))


        pg.display.update()
        clock.tick(60)
    pg.quit()
    quit()


if __name__ == "__main__":
    main()