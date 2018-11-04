from src.Settings import *
from src.Camera import Camera
from src.Classes import *
from src.Map import Map
from src.tile_list import *
from src.drawable_dict import *
from src.Isometric.convert import *

#ero = Character.Character

class Game:

    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pg.display.set_caption('RRPG ' + GAME_VERSION)
        self.clock = pg.time.Clock()
        self.images = {}

    def new(self):  # Начало новой игры

        self.hero = Character.Character()
        self.inventory = Inventory.Inventory(self.display, self.hero)
        self.hero.inventory = self.inventory

        weapon = Weapon.Weapon()
        weapon.img = pg.image.load('Drawable/start_sword.png')
        weapon.info = "Оружие новичка"
        self.hero.inventory.weapon = weapon

        armor = Armor.Armor()
        armor.img = pg.image.load('Drawable/start_armor.png')
        armor.info = "Броня новичка"
        self.hero.inventory.armor = armor

        weapon2 = Weapon.Weapon()
        weapon2.img = pg.image.load('Drawable/start_sword1.png')
        weapon2.info = "Оружие новичка +1"
        weapon2.set_attack(3)
        self.hero.inventory.add_item(weapon2)

        armor2 = Armor.Armor()
        armor2.img = pg.image.load('Drawable/start_armor1.png')
        armor2.info = "Броня новичка +1"
        armor2.set_protection(2)
        self.hero.inventory.add_item(armor2)



        heal_poition = Potion.Potion
        heal_poition.img = pg.image.load('Drawable/heal.png')
        heal_poition.info = "Зелье лечения"
        heal_poition.description = "+25HP"
        heal_poition.cost = 15


        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.walls = Object.Object()
        self.floor = Object.Object()

        self.load_data()
        (s_x, s_y) = self.map.rooms[0].center()
        self.hero.set_pos(s_x*BLOCK_WIDTH, s_y*BLOCK_HEIGHT)

    def load_images(self):
        self.images = {}
        for drw in drawable.items():
            self.images[drw[0]] = pg.image.load(drw[1])

    def load_data(self):
        self.load_images()
        self.hero.img = pg.image.load('Drawable/1.png')

        self.map = Map()
        self.map.generate_map()

        total_level_width = len(self.map.body[0]) * BLOCK_WIDTH
        total_level_height = len(self.map.body) * BLOCK_HEIGHT
        self.camera = Camera(total_level_width, total_level_height)

    def run(self):
        self.crashed = False
        while not self.crashed:
            self.event()
            self.update()
            self.render()

            pg.display.update()
            self.clock.tick(30)

        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            self.event_keys(event)
            if self.hero.inventory.opened:
                self.hero.inventory.inventory_event(event)
            else:
                self.move_event(event)


    def move_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_position = pg.mouse.get_pos()

            block_x = int((mouse_position[0] - self.camera.coefficient_x) / BLOCK_WIDTH)  # Позиция в блоках
            block_y = int((mouse_position[1] - self.camera.coefficient_y) / BLOCK_HEIGHT)

            pixels_x = block_x * BLOCK_WIDTH  # Позиция в пикселях
            pixels_y = block_y * BLOCK_HEIGHT

            if self.collision(block_x, block_y):
                self.hero.rect = Rect(pixels_x, pixels_y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def event_keys(self, event):
        if event.type == pg.QUIT:
            self.crashed = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.crashed = True
            if event.key == pg.K_i:
                if self.hero.inventory.opened:
                    self.hero.inventory.opened = False
                else:
                    self.hero.inventory.opened = True

    def collision(self, block_x, block_y):
        if len(self.map.body[0]) > block_x >= 0 and len(self.map.body) > block_y >= 0:
            if self.map.body[block_y][block_x].symbol != WALL_TILE and \
                    self.map.body[block_y][block_x].symbol != BACK_TILE:

                if self.map.body[block_y][block_x].symbol == DOOR_TILE:
                    self.map.body[block_y][block_x].symbol = OPEN_DOOR_TILE
                elif self.map.body[block_y][block_x].symbol == OPEN_DOOR_TILE:
                    self.map.body[block_y][block_x].symbol = DOOR_TILE

                return True
        return False

    def update(self):
        self.camera.update(self.hero)

    def render(self):
        self.display.fill(BACKGROUND_COLOR)
        self.map_render()
        self.unit_render()
        self.inventory_render()

    def inventory_render(self):
        if self.hero.inventory.opened:
            self.display.blit(self.hero.inventory.background, (20, 50))
            self.display.blit(self.hero.inventory.info_background, (600, 50))
            text = self.hero.inventory.font.render(str(self.hero.get_attack())[0:17], True, (200, 220, 180))

            self.display.blit(text, [650, 400])
            i = j = 0
            if self.hero.inventory:
                for item in self.hero.inventory.item_list:
                    self.display.blit(item.img, (50 + i * 50, 65 + j * 50))
                    i += 1
                    if i == 4:
                        j += 1
                        i = 0
            if self.hero.inventory.item_info:
                self.display.blit(self.hero.inventory.item_background,(self.hero.inventory.item_x, self.hero.inventory.item_y))
                self.display.blit(self.hero.inventory.item_list[self.hero.inventory.item_num].img,
                                  (self.hero.inventory.item_x + 10, self.hero.inventory.item_y + 23, 40, 40))

                text = self.hero.inventory.font.render(self.hero.inventory.item_list
                                                       [self.hero.inventory.item_num].info[0:17], True, (200, 220, 180))
                text_dis = self.hero.inventory.font_small.render(self.hero.inventory.item_list
                                                                 [self.hero.inventory.item_num].description[0:17], True, (200, 220, 180))
                text_cost = self.hero.inventory.font.render(str(self.hero.inventory.item_list
                                                                [self.hero.inventory.item_num].cost)[0:5], True, (200, 220, 180))

                self.display.blit(text, [self.hero.inventory.item_x + 70, self.hero.inventory.item_y + 40])
                self.display.blit(text_dis, [self.hero.inventory.item_x + 70, self.hero.inventory.item_y + 85])
                self.display.blit(text_cost, [self.hero.inventory.item_x + 160, self.hero.inventory.item_y + 120])

            if self.hero.inventory.weapon:
                self.display.blit(self.hero.inventory.weapon.img, (70, 385))
            if self.hero.inventory.armor:
                self.display.blit(self.hero.inventory.armor.img, (180, 385))

    def map_render(self):

        #self.map.debug_print_map()
        self.map.print_map(self.display, self.camera, self.images)

        self.camera.coefficient_x = self.camera.apply(Block(0, 0)).x  # Отклонения для x,y
        self.camera.coefficient_y = self.camera.apply(Block(0, 0)).y

    def unit_render(self):
        self.display.blit(self.hero.img, self.camera.apply(self.hero))


game = Game()
game.new()
game.run()
