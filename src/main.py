import pygame as pg

pg.init()
gameDisplay = pg.display.set_mode((800, 600))
pg.display.set_caption('A Bit Racey')
clock = pg.time.Clock()

crashed = False

while not crashed:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True

        print(event)

    pg.display.update()
    clock.tick(60)

pg.quit()
quit()