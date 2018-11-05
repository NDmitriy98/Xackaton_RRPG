import random

from src import pyganim
from src.Settings import *
from src.Camera import Camera
from src.Classes import *
from src.Map import Map
from src.tile_list import *
from src.drawable_dict import *
from src.Isometric.convert import *
from copy import copy, deepcopy

MIN_ENEMY_COUNT = 6
MAX_ENEMY_COUNT = 16
MAX_ENEMY_IN_ROOM = 3


class Game:

    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pg.display.set_caption('RRPG ' + GAME_VERSION)
        self.clock = pg.time.Clock()
        self.images = {}
        self.game_map = Map()
        self.game_state = deepcopy(self.game_map.body)
        self.hero = Character.Character()
        self.inventory = Inventory.Inventory()
        self.enemies = []
        self.step = False
        self.iterations = 0

    def new(self):  # Начало новой игры

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
        # self.walls = Object.Object()
        # self.floor = Object.Object()

        self.load_data()
        self.game_map.debug_print_map()
        (s_x, s_y) = self.game_map.rooms[0].center()
        self.hero.set_pos(s_x, s_y)
        self.hero.set_rect_pos(s_x * BLOCK_WIDTH, s_y * BLOCK_HEIGHT)

        self.set_enemies()
        self.update_state()
        #self.game_state.debug_print_map()

    def load_images(self):
        self.images = {}
        for drw in drawable.items():
            self.images[drw[0]] = pg.image.load(drw[1])

    def load_data(self):
        self.load_images()
        self.hero.img = pg.image.load('Drawable/1.png')
        self.hud_background = pg.image.load('Drawable/hud.png')
        self.hud_level_background = pg.image.load('Drawable/hud_level.png')

        self.game_map.generate_map()

        total_level_width = len(self.game_map.body[0]) * BLOCK_WIDTH
        total_level_height = len(self.game_map.body) * BLOCK_HEIGHT
        self.camera = Camera(total_level_width, total_level_height)

    def update_state(self):
        self.game_state = deepcopy(self.game_map.body)
        self.game_state[self.hero.y][self.hero.x].symbol = self.hero.tile.symbol
        for enemy in self.enemies:
            self.game_state[enemy.y][enemy.x].symbol = enemy.tile.symbol


        self.hero.init_path_finder(self.game_state)
        for enemy in self.enemies:
            enemy.init_path_finder(self.game_state)


        #self.game_state.debug_print_map()


    def run(self):
        self.crashed = False
        while not self.crashed:
            self.event()
            self.update()
            self.render()
            #print("x, y " + str(self.hero.x) + " " + str(self.hero.y))
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

            if self.check_npc(block_x, block_y):
                for enemy in self.enemies:
                    if enemy.x == block_x and enemy.y == block_y:
                        print("punch")
                        damage = self.hero.get_attack()
                        enemy.in_damage(damage)
                        #self.print_damage(block_x, block_y, damage)
                        if not enemy.alive:
                            self.enemies.remove(enemy)
                            try:
                                self.update_state()
                            except Exception as msg:
                                print(msg)



                        if self.hero.get_rect_y() - pixels_y == 50 and self.hero.get_rect_x() == pixels_x:
                            ############UP ATTACK
                            self.hero.attack_up = True
                            self.hero.falseStay()
                            self.hero.falseMove()
                        if self.hero.get_rect_y() - pixels_y == -50 and self.hero.get_rect_x() == pixels_x:
                            ############DOWN ATTACK
                            self.hero.attack_down = True
                            self.hero.falseStay()
                            self.hero.falseMove()
                        if self.hero.get_rect_y() == pixels_y and self.hero.get_rect_x() - pixels_x == -50:
                            ############RIGHT ATTACK
                            self.hero.attack_right = True
                            self.hero.falseStay()
                            self.hero.falseMove()
                        if self.hero.get_rect_y() == pixels_y and self.hero.get_rect_x() - pixels_x == 50:
                            ############LEFT ATTACK
                            self.hero.attack_left = True
                            self.hero.falseStay()
                            self.hero.falseMove()



            else:
                if self.collision(block_x, block_y):
                    self.hero.init_path_finder(self.game_state)
                    self.hero.build_path(block_x, block_y)
                    if self.hero.get_rect_y() - pixels_y == 50 and self.hero.get_rect_x() == pixels_x:
                        ############UP MOVE
                        self.hero.up = True
                        self.hero.falseStay()
                        self.hero.falseAttack()
                    if self.hero.get_rect_y() - pixels_y == -50 and self.hero.get_rect_x() == pixels_x:
                        ############DOWN MOVE
                        self.hero.down = True
                        self.hero.falseStay()
                        self.hero.falseAttack()
                    if self.hero.get_rect_y() == pixels_y and self.hero.get_rect_x() - pixels_x == -50:
                        ############RIGHT MOVE
                        self.hero.right = True
                        self.hero.falseStay()
                        self.hero.falseAttack()
                    if self.hero.get_rect_y() == pixels_y and self.hero.get_rect_x() - pixels_x == 50:
                        ############LEFT MOVE
                        self.hero.left = True
                        self.hero.falseStay()
                        self.hero.falseAttack()



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
            if event.key == pg.K_e:
                self.hero.add_experience(3)

    def check_npc(self, block_x, block_y):
        if len(self.game_state[0]) > block_x >= 0 and len(self.game_state) > block_y >= 0:
            if self.game_state[block_y][block_x].symbol == SKELETON_TILE:
                return True
        return False

    def collision(self, block_x, block_y):
        if len(self.game_map.body[0]) > block_x >= 0 and len(self.game_map.body) > block_y >= 0:
            if self.game_map.body[block_y][block_x].symbol != WALL_TILE and \
                    self.game_map.body[block_y][block_x].symbol != BACK_TILE:

                if self.game_map.body[block_y][block_x].symbol == DOOR_TILE:
                    self.game_map.body[block_y][block_x].symbol = OPEN_DOOR_TILE
                elif self.game_map.body[block_y][block_x].symbol == OPEN_DOOR_TILE:
                    self.game_map.body[block_y][block_x].symbol = DOOR_TILE

                return True
        return False

    def update(self):
        self.camera.update(self.hero)

    def render(self):
        self.display.fill(BACKGROUND_COLOR)
        self.map_render()
        self.enemy_render()
        self.unit_render(self.hero)
        self.hud_render()
        self.inventory_render()
       # self.update_state()

    def render_damage(self):
        damage = self.hero.get_attack()
        text =self.hero.inventory.font_big.render(" - " + str(damage) + " HP"[0:9], True, (200, 220, 250))
        print("rect" + str(self.hero.get_rect_x()) + " " + str(self.hero.get_rect_y()))
        self.display.blit(text, [WIN_WIDTH/2, WIN_HEIGHT/2 - 100 + self.iterations * SPEED])


    def unit_render(self, unit):
        in_display = self.camera.apply(unit)
        if WIN_WIDTH >= in_display.x >= 0 and WIN_HEIGHT >= in_display.y >= 0:
            if unit.up and self.iterations < (BLOCK_HEIGHT / SPEED):
                unit.move_rect(0, -SPEED)
                unit.animMoveUp.blit(self.display, self.camera.apply(unit))
                self.iterations += 1
                if self.iterations >= (BLOCK_HEIGHT / SPEED):
                    unit.up = False
                    unit.stay = True
                    unit.stay_up = True
                    self.iterations = 0
                    unit.move(0, -1)

            if unit.down and self.iterations < (BLOCK_HEIGHT/SPEED):
                unit.move_rect(0, SPEED)
                unit.animMoveDown.blit(self.display, self.camera.apply(unit))
                self.iterations += 1
                if self.iterations >= (BLOCK_HEIGHT/SPEED):
                    unit.down = False
                    unit.stay = True
                    unit.stay_down = True
                    self.iterations = 0
                    unit.move(0, 1)

            if unit.right and self.iterations < (BLOCK_HEIGHT/SPEED):
                unit.move_rect(SPEED, 0)
                unit.animMoveRight.blit(self.display, self.camera.apply(unit))
                self.iterations += 1
                if self.iterations >= (BLOCK_HEIGHT/SPEED):
                    unit.right = False
                    unit.stay = True
                    unit.stay_right = True
                    self.iterations = 0
                    unit.move(1, 0)

            if unit.left and self.iterations < (BLOCK_HEIGHT/SPEED):
                unit.move_rect(-SPEED, 0)
                unit.animMoveLeft.blit(self.display, self.camera.apply(unit))
                self.iterations += 1
                if self.iterations >= (BLOCK_HEIGHT/SPEED):
                    unit.left = False
                    unit.stay = True
                    unit.stay_left = True
                    self.iterations = 0
                    unit.move(-1, 0)

            if unit.attack_up and self.iterations < (BLOCK_HEIGHT/SPEED):
                unit.animAttackUp.blit(self.display, self.camera.apply(unit))
                self.iterations += 1
                self.render_damage()
                if self.iterations >= (BLOCK_HEIGHT/SPEED):
                    unit.attack_up = False
                    unit.stay = True
                    unit.stay_up = True
                    self.iterations = 0

            if unit.attack_down and self.iterations < (BLOCK_HEIGHT/SPEED):
                unit.animAttackDown.blit(self.display, self.camera.apply(unit))
                self.iterations += 1
                self.render_damage()
                if self.iterations >= (BLOCK_HEIGHT/SPEED):
                    unit.attack_down = False
                    unit.stay = True
                    unit.stay_down = True
                    self.iterations = 0


            if unit.attack_right and self.iterations < (BLOCK_HEIGHT/SPEED):
                unit.animAttackRight.blit(self.display, self.camera.apply(unit))
                self.iterations += 1
                self.render_damage()
                if self.iterations >= (BLOCK_HEIGHT/SPEED):
                    unit.attack_right = False
                    unit.stay = True
                    unit.stay_right = True
                    self.iterations = 0


            if unit.attack_left and self.iterations < (BLOCK_HEIGHT/SPEED):
                unit.animAttackLeft.blit(self.display, self.camera.apply(unit))
                self.iterations += 1
                self.render_damage()
                if self.iterations >= (BLOCK_HEIGHT/SPEED):
                    unit.attack_left = False
                    unit.stay = True
                    unit.stay_left = True
                    self.iterations = 0

            if unit.stay:
                if unit.stay_up:
                    unit.animStayUp.blit(self.display, self.camera.apply(unit))
                if unit.stay_down:
                    unit.animStayDown.blit(self.display, self.camera.apply(unit))
                if unit.stay_right:
                    unit.animStayRight.blit(self.display, self.camera.apply(unit))
                if unit.stay_left:
                    unit.animStayLeft.blit(self.display, self.camera.apply(unit))



    def inventory_render(self):
        if self.hero.inventory.opened:
            self.display.blit(self.hero.inventory.background, (20, 50))
            self.display.blit(self.hero.inventory.info_background, (600, 50))
            text = [self.hero.inventory.font_big.render(str(self.hero.get_attack())[0:6], True, (200, 220, 180)),
                    self.hero.inventory.font_big.render(str(self.hero.get_protection())[0:6], True, (200, 220, 180)),
                    self.hero.inventory.font_big.render(str(self.hero.info)[0:9], True, (200, 220, 180)),
                    self.hero.inventory.font_big.render(str(self.hero.level)[0:4], True, (200, 220, 180)),
                    self.hero.inventory.font_default.render((str(self.hero.hp))+"/"+str(self.hero.get_hp())[0:10], True, (200, 220, 180)),
                    self.hero.inventory.font_default.render(str(len(self.hero.inventory.item_list)) + "/24"[0:6], True, (200, 220, 180))]

            self.display.blit(text[0], [650, 390])
            self.display.blit(text[1], [770, 390])
            self.display.blit(text[2], [700, 90])
            self.display.blit(text[3], [780, 150])
            self.display.blit(text[4], [755, 220])
            self.display.blit(text[5], [755, 290])

            i = j = 0
            if self.hero.inventory:
                for item in self.hero.inventory.item_list:
                    self.display.blit(item.img, (50 + i * 50, 65 + j * 50))
                    i += 1
                    if i == 4:
                        j += 1
                        i = 0
            if self.hero.inventory.item_info:
                self.display.blit(self.hero.inventory.item_background,
                                  (self.hero.inventory.item_x, self.hero.inventory.item_y))
                self.display.blit(self.hero.inventory.item_list[self.hero.inventory.item_num].img,
                                  (self.hero.inventory.item_x + 10, self.hero.inventory.item_y + 23, 40, 40))

                text = self.hero.inventory.font.render(self.hero.inventory.item_list
                                                       [self.hero.inventory.item_num].info[0:17], True, (200, 220, 180))
                text_dis = self.hero.inventory.font_small.render(self.hero.inventory.item_list
                                                                 [self.hero.inventory.item_num].description[0:17], True,
                                                                 (200, 220, 180))
                text_cost = self.hero.inventory.font.render(str(self.hero.inventory.item_list
                                                                [self.hero.inventory.item_num].cost)[0:5], True,
                                                            (200, 220, 180))

                self.display.blit(text, [self.hero.inventory.item_x + 70, self.hero.inventory.item_y + 40])
                self.display.blit(text_dis, [self.hero.inventory.item_x + 70, self.hero.inventory.item_y + 85])
                self.display.blit(text_cost, [self.hero.inventory.item_x + 160, self.hero.inventory.item_y + 120])

            if self.hero.inventory.weapon:
                self.display.blit(self.hero.inventory.weapon.img, (70, 385))
            if self.hero.inventory.armor:
                self.display.blit(self.hero.inventory.armor.img, (180, 385))

    def hud_render(self):
        self.display.blit(self.hud_background, (20, 500))
        self.display.blit(self.hud_level_background, (280, 500))

        hp = self.hero.hp/self.hero.get_max_hp()
        mp = self.hero.mp/self.hero.get_max_mp()
        exp = self.hero.experience/(self.hero.level * 10)

        pg.draw.rect(self.display, (255, 50, 50), (70, 514, hp*196, 31))
        pg.draw.rect(self.display, (50, 50, 255), (70, 559, mp * 196, 26))
        pg.draw.rect(self.display, (200, 200, 200), (70, 604, exp * 196, 11))

        text = [self.hero.inventory.font_ultra_big.render(str(self.hero.level)[0:3], True, (200, 200, 200)),
                self.hero.inventory.font_big.render(str(self.hero.hp) + "/" + str(self.hero.get_max_hp())[0:8], True, (200, 220, 180)),
                self.hero.inventory.font_big.render(str(self.hero.mp) + "/" + str(self.hero.get_max_mp())[0:8], True, (200, 200, 200)),
                self.hero.inventory.font_small.render(str(self.hero.experience) + "/" + str(self.hero.level*10)[0:8], True, (10, 20, 10))]

        self.display.blit(text[0], [295, 520])
        self.display.blit(text[1], [100, 517])
        self.display.blit(text[2], [100, 560])
        self.display.blit(text[3], [100, 603])



    def map_render(self):

        # self.map.debug_print_map()
        self.game_map.print_map(self.display, self.camera, self.images)

        self.camera.coefficient_x = self.camera.apply(Block(0, 0)).x  # Отклонения для x,y
        self.camera.coefficient_y = self.camera.apply(Block(0, 0)).y

    def enemy_render(self):
        for enemy in self.enemies:
            enemy.set_rect_pos(enemy.x * BLOCK_WIDTH, enemy.y * BLOCK_HEIGHT)
            self.unit_render(enemy)
            #enemy.tile.draw(enemy.x * BLOCK_WIDTH, enemy.y * BLOCK_HEIGHT, self.display, self.camera, self.images)

    def set_enemies(self):
        enemy_count = random.randint(MIN_ENEMY_COUNT, MAX_ENEMY_COUNT)

        for room in self.game_map.rooms[1:]:
            if enemy_count == 0:
                break
            else:
                in_room = random.randint(0, MAX_ENEMY_IN_ROOM)
                for i in range(in_room):
                    enemy = Skeleton.Skeleton()
                    pos_x = random.randint(room.x1, room.x2)
                    pos_y = random.randint(room.y1, room.y2)
                    while self.game_map.body[pos_y][pos_x].symbol != FLOOR_TILE and \
                            self.game_state[pos_y][pos_x].symbol != FLOOR_TILE:
                        pos_x = random.randint(room.x1, room.x2)
                        pos_y = random.randint(room.y1, room.y2)

                    enemy.set_pos(pos_x, pos_y)
                    enemy_count -= 1
                    self.enemies.append(enemy)
        self.update_state()


game = Game()
game.new()
game.run()
