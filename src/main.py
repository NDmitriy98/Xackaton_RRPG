from src.Settings import *
from src.Camera import Camera
from src.Classes import *


class Game:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pg.display.set_caption('RRPG ' + GAME_VERSION)
        self.clock = pg.time.Clock()

    def new(self):  # Начало новой игры
        self.hero = Character.Character()
        self.hero.set_pos(50, 50)
        self.inventory = Inventory.Inventory(self.display, self.hero)
        self.hero.inventory = self.inventory

        heal_poition = Item.Item
        heal_poition.img = pg.image.load('Drawable/heal.png')
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)

        self.walls = Object.Object()
        self.floor = Object.Object()

        self.load_data()

    def load_data(self):
        self.map = [
            "#########################",
            "#--###---################",
            "#--###-------############",
            "#--#########-############",
            "#--------------##########",
            "#####-#######--##########",
            "#####-###################",
            "####---##################",
            "#########################"]

        self.hero.img = pg.image.load('Drawable/1.png')
        self.walls.img = pg.image.load('Drawable/wall.png')
        self.floor.img = pg.image.load('Drawable/floor.png')

        total_level_width = len(self.map[0]) * BLOCK_WIDTH
        total_level_height = len(self.map) * BLOCK_HEIGHT
        self.camera = Camera(total_level_width, total_level_height)

    def run(self):
        self.crashed = False
        while not self.crashed:
            self.event()
            self.update()
            self.render()

            self.hero.inventory.render_inventory()
            # print("pos " + str(self.hero.x) + " " + str(self.hero.y))

            pg.display.update()
            self.clock.tick(30)

        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.crashed = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.crashed = True

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_position = pg.mouse.get_pos()

                block_x = int((mouse_position[0] - self.camera.coefficient_x) / BLOCK_WIDTH)  # Позиция в блоках
                block_y = int((mouse_position[1] - self.camera.coefficient_y) / BLOCK_HEIGHT)

                pixels_x = block_x * BLOCK_WIDTH  # Позиция в пикселях
                pixels_y = block_y * BLOCK_HEIGHT

                if self.collision(block_x, block_y):
                    self.hero.rect = Rect(pixels_x, pixels_y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def collision(self, block_x, block_y):
        if len(self.map[0]) > block_x >= 0 and len(self.map) > block_y >= 0:
            if self.map[block_y][block_x] == '-':
                return True
        return False

    def update(self):
        self.camera.update(self.hero)

    def render(self):
        self.display.fill(BACKGROUND_COLOR)
        self.map_render()
        self.unit_render()

    def map_render(self):
        x = y = 0
        for row in self.map:
            for col in row:
                if col == '#':
                    block = Block(x, y)
                    self.display.blit(self.walls.img, self.camera.apply(block))
                if col == '-':
                    block = Block(x, y)
                    self.display.blit(self.floor.img, self.camera.apply(block))
                x += BLOCK_WIDTH
            y += BLOCK_HEIGHT
            x = 0

        self.camera.coefficient_x = self.camera.apply(Block(0, 0)).x  # Отклонения для x,y
        self.camera.coefficient_y = self.camera.apply(Block(0, 0)).y

    def unit_render(self):
        self.display.blit(self.hero.img, self.camera.apply(self.hero))


game = Game()
game.new()
game.run()
