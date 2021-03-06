import random

from src import pyganim
from src.Tile import Tile
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
        self.menu_show = True
        self.game_start = False
        self.enemies = []
        self.step = True
        self.npc_step = False
        self.steps = 0
        self.menu_background = pg.image.load('Drawable/menu_background.png')
        self.menu_background_start = pg.image.load('Drawable/start_button.png')
        self.menu_background_exit = pg.image.load('Drawable/exit_button.png')
        self.menu_game_over = pg.image.load('Drawable/game_over.png')
        pg.mixer_music.load('sound/background.wav')
        pg.mixer_music.play(-1)

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
        heal_poition.img = pg.image.load('Drawable/heal_poit.png')
        heal_poition.info = "Зелье лечения"
        heal_poition.description = "+20 HP"
        heal_poition.cost = 15



        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)
        self.hero.inventory.add_item(heal_poition)


        self.load_data()
        self.game_map.debug_print_map()
        (s_x, s_y) = self.game_map.rooms[0].center()
        self.hero.set_pos(s_x, s_y)
        self.hero.set_rect_pos(s_x * BLOCK_WIDTH, s_y * BLOCK_HEIGHT)

        self.set_enemies()
        self.update_state()

    def menu(self):
        while self.menu_show:
            picture = pg.transform.scale(self.menu_background, (WIN_WIDTH, WIN_HEIGHT))
            self.display.blit(self.menu_background, (0, 0))
            pg.draw.rect(self.display, (0, 50, 50), (40, 30, 250, 100))
            self.display.blit(self.menu_background_start, (40, 30))
            self.display.blit(self.menu_background_exit, (40, 270))
            self.menu_event()
            pg.display.update()
            self.clock.tick(30)
        if not self.game_start:
            pg.quit()
            quit()

    def load_images(self):
        self.images = {}
        for drw in drawable.items():
            self.images[drw[0]] = pg.image.load(drw[1])

    def load_data(self):
        self.load_images()
        self.hero.img = pg.image.load('Drawable/1.png')
        self.hud_background = pg.image.load('Drawable/hud.png')
        self.hud_level_background = pg.image.load('Drawable/hud_level.png')
        self.time_ico = pg.image.load('Drawable/time_ico.png')

        self.game_map.generate_map()

        total_level_width = len(self.game_map.body[0]) * BLOCK_WIDTH
        total_level_height = len(self.game_map.body) * BLOCK_HEIGHT
        self.camera = Camera(total_level_width, total_level_height)

    def copy_state(self):
        copy = []
        for y, row in enumerate(self.game_map.body):
            copy.append([])
            for x, col in enumerate(row):
                copy[y].append(Tile(self.game_map.body[y][x].symbol, self.game_map.body[y][x].visible))

        return copy

    def hero_view(self):
        self.hero.view()
        for y, row in enumerate(self.game_map.body):
            for x, col in enumerate(row):
                if self.hero.fov.lit(x, y):
                    self.game_map.body[y][x].visible = True
                    self.game_map.body[y][x].explored = True
                else:
                    self.game_map.body[y][x].visible = False

    def update_state(self):
        self.game_state = self.copy_state()
        self.game_state[int(self.hero.y)][int(self.hero.x)].symbol = self.hero.tile.symbol
        for enemy in self.enemies:
            self.game_state[enemy.y][enemy.x].symbol = enemy.tile.symbol

        self.hero.init_path_finder(self.game_state)
        self.hero.init_fov(self.game_state)
        self.hero_view()

        for enemy in self.enemies:
            enemy.init_path_finder(self.game_state)
            enemy.init_fov(self.game_state)
            enemy.look_for_hero()

        # self.game_state.debug_print_map()

    def run(self):
        self.crashed = False
        while not self.crashed:
            self.event()
            self.update()
            self.render()

            pg.display.update()
            self.clock.tick(30)
            if not self.hero.alive:
                self.render_death()
        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            self.event_keys(event)
            if self.hero.inventory.opened:
                res = self.hero.inventory.inventory_event(event)
                self.check_res(res)
            else:
                if self.hero.stay:
                    self.move_event(event)

    def check_res(self, res):
        # if res == 0:
        #    print("NO RES")
        if res == 1:
            self.hero.add_experience(50)
        if res == 2:
            self.hero.hp += 20
            if self.hero.hp > self.hero.get_max_hp():
                self.hero.hp = self.hero.get_max_hp()
            # self.hero.in_damage(100)

    def move_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_position = pg.mouse.get_pos()

            block_x = int((mouse_position[0] - self.camera.coefficient_x) / BLOCK_WIDTH)  # Позиция в блоках
            block_y = int((mouse_position[1] - self.camera.coefficient_y) / BLOCK_HEIGHT)

            print("pos " + str(self.hero.x) + " " + str(self.hero.y))
            print("block " + str(block_x) + " " + str(block_y))
            print("tile " + str(self.game_state[block_y][block_x].symbol))

            if (WIN_WIDTH / 2 + 125) > mouse_position[0] > (WIN_WIDTH / 2 - 125) and 70 > mouse_position[1] > 30:
                self.npc_start()

            if self.hero.get_destination(block_x, block_y):
                if self.check_npc(block_x, block_y):
                    for enemy in self.enemies:
                        if enemy.x == block_x and enemy.y == block_y:
                            print("punch")
                            damage = self.hero.get_attack()
                            enemy.in_damage(damage)
                            self.npc_start()
                            if not enemy.alive:
                                if enemy.drop:
                                    self.hero.inventory.item_list.append(enemy.drop)
                                self.enemies.remove(enemy)
                                self.hero.add_experience(8)
                                try:
                                    self.update_state()
                                except Exception as msg:
                                    print(msg)

                            self.hero.set_attack_direction(block_x, block_y)

                else:
                    if self.collision(block_x, block_y):
                        self.hero.init_path_finder(self.game_state)
                        # self.hero.build_path(block_x, block_y)
                        self.npc_start()
                        if self.hero.y - block_y == 1 and self.hero.x == block_x:
                            ############UP MOVE
                            self.hero.falseAll()
                            self.hero.up = True

                        if self.hero.y - block_y == -1 and self.hero.x == block_x:
                            ############DOWN MOVE
                            self.hero.falseAll()
                            self.hero.down = True

                        if self.hero.y == block_y and self.hero.x - block_x == -1:
                            ############RIGHT MOVE
                            self.hero.falseAll()
                            self.hero.right = True

                        if self.hero.y == block_y and self.hero.x - block_x == 1:
                            ############LEFT MOVE
                            self.hero.falseAll()
                            self.hero.left = True

    def render_death(self):
        self.restart = False
        while not self.restart:
            self.display.blit(self.menu_game_over, (200, 100))
            self.death_event()

            pg.display.update()
            self.clock.tick(30)
        if self.restart and not self.crashed:
            self.images = {}
            self.game_map = Map()
            self.game_state = deepcopy(self.game_map.body)

            self.hero = Character.Character()
            self.inventory = Inventory.Inventory()

            self.enemies = []
            self.step = True
            self.npc_step = False
            self.steps = 0

            game.new()

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
            if self.game_state[block_y][block_x].symbol == DWARF_TILE:
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

    def death_event(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_position = pg.mouse.get_pos()
                if 470 > mouse_position[0] > 258 and 460 > mouse_position[1] > 385:
                    self.restart = True
                if 744 > mouse_position[0] > 525 and 460 > mouse_position[1] > 385:
                    self.restart = True
                    self.crashed = True

    def menu_event(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_position = pg.mouse.get_pos()
                if 340 > mouse_position[0] > 40 and 140 > mouse_position[1] > 30:
                    self.menu_show = False
                    self.game_start = True
                if 340 > mouse_position[0] > 40 and 380 > mouse_position[1] > 270:
                    self.menu_show = False

    def npc_start(self):
        for enemy in self.enemies:
            enemy.npc_step = True

    _step = True

    def update(self):
        self.camera.update(self.hero)

    def render(self):
        self.display.fill(BACKGROUND_COLOR)
        self.map_render()
        self.enemy_render()
        self.unit_render(self.hero)
        self.hud_render()
        self.inventory_render()

    def render_damage(self, unit):
        damage = unit.get_attack()
        text = self.hero.inventory.font_big.render(" - " + str(damage) + " HP"[0:9], True, (200, 220, 250))
        self.display.blit(text, [WIN_WIDTH / 2, WIN_HEIGHT / 2 - 100 + self.hero.iterations * SPEED])

    def unit_render(self, unit):

        if unit != self.hero and unit.npc_step:
            if not unit.armed:
                if unit.current_path and len(unit.current_path) != 0:

                    if unit.stay == True:
                        k = unit.current_path.pop()
                        unit.npc_step = False
                        if k == "L":
                            unit.left = True
                        if k == "R":
                            unit.right = True
                        if k == "U":
                            unit.up = True
                        if k == "D":
                            unit.down = True
                        unit.falseStay()
                        unit.falseAttack()
                else:
                    rand_room = random.randint(0, self.game_map.roomCount - 1)
                    rand_point = self.game_map.rooms[rand_room].center()
                    unit.init_path_finder(self.game_state)
                    unit.build_path(rand_point[0], rand_point[1])
            else:
                unit.npc_step = False
                attacked = True
                damage = unit.get_attack()
                self.hero.in_damage(damage)
                unit.armed = False
                print('{0} attacked'.format(unit.info))

        in_display = self.camera.apply(unit)

        if WIN_WIDTH >= in_display.x >= 0 and WIN_HEIGHT >= in_display.y >= 0:
            pos_changed = False
            if unit.up and unit.iterations < (BLOCK_HEIGHT // SPEED):
                unit.move_rect(0, -SPEED)
                unit.animMoveUp.blit(self.display, self.camera.apply(unit))
                unit.iterations += 1
                if unit.iterations >= (BLOCK_HEIGHT // SPEED):
                    unit.falseAll()
                    unit.move(0, -1)
                    pos_changed = True
                    unit.up = False
                    unit.stay = True
                    unit.stay_up = True
                    unit.iterations = 0

            if unit.down and unit.iterations < (BLOCK_HEIGHT / SPEED):
                unit.move_rect(0, SPEED)
                unit.animMoveDown.blit(self.display, self.camera.apply(unit))
                unit.iterations += 1
                if unit.iterations >= (BLOCK_HEIGHT / SPEED):
                    unit.falseAll()
                    unit.move(0, 1)
                    unit.stay = True
                    unit.stay_down = True
                    unit.iterations = 0
                    pos_changed = True

            if unit.right and unit.iterations < (BLOCK_HEIGHT / SPEED):
                unit.move_rect(SPEED, 0)
                unit.animMoveRight.blit(self.display, self.camera.apply(unit))
                unit.iterations += 1
                if unit.iterations >= (BLOCK_HEIGHT / SPEED):
                    unit.falseAll()
                    unit.move(1, 0)
                    unit.stay = True
                    unit.stay_right = True
                    unit.iterations = 0
                    pos_changed = True

            if unit.left and unit.iterations < (BLOCK_HEIGHT / SPEED):
                unit.move_rect(-SPEED, 0)
                unit.animMoveLeft.blit(self.display, self.camera.apply(unit))
                unit.iterations += 1
                if unit.iterations >= (BLOCK_HEIGHT / SPEED):
                    unit.falseAll()
                    unit.move(-1, 0)
                    unit.stay = True
                    unit.stay_left = True
                    unit.iterations = 0
                    pos_changed = True

            if unit.attack_up and unit.iterations < (BLOCK_HEIGHT / SPEED):
                unit.animAttackUp.blit(self.display, self.camera.apply(unit))
                unit.iterations += 1
                self.render_damage(unit)
                if unit.iterations >= (BLOCK_HEIGHT / SPEED):
                    unit.falseAll()
                    unit.stay = True
                    unit.stay_up = True
                    unit.iterations = 0

            if unit.attack_down and unit.iterations < (BLOCK_HEIGHT / SPEED):
                unit.animAttackDown.blit(self.display, self.camera.apply(unit))
                unit.iterations += 1
                self.render_damage(unit)
                if unit.iterations >= (BLOCK_HEIGHT / SPEED):
                    unit.falseAll()
                    unit.stay = True
                    unit.stay_down = True
                    unit.iterations = 0

            if unit.attack_right and unit.iterations < (BLOCK_HEIGHT / SPEED):
                unit.animAttackRight.blit(self.display, self.camera.apply(unit))
                unit.iterations += 1
                self.render_damage(unit)
                if unit.iterations >= (BLOCK_HEIGHT / SPEED):
                    unit.falseAll()
                    unit.stay = True
                    unit.stay_right = True
                    unit.iterations = 0

            if unit.attack_left and unit.iterations < (BLOCK_HEIGHT / SPEED):
                unit.animAttackLeft.blit(self.display, self.camera.apply(unit))
                unit.iterations += 1
                self.render_damage(unit)
                if unit.iterations >= (BLOCK_HEIGHT / SPEED):
                    unit.falseAll()
                    unit.stay = True
                    unit.stay_left = True
                    unit.iterations = 0

            if unit.stay:
                if unit.stay_up:
                    unit.animStayUp.blit(self.display, self.camera.apply(unit))
                if unit.stay_down:
                    unit.animStayDown.blit(self.display, self.camera.apply(unit))
                if unit.stay_right:
                    unit.animStayRight.blit(self.display, self.camera.apply(unit))
                if unit.stay_left:
                    unit.animStayLeft.blit(self.display, self.camera.apply(unit))
            if pos_changed:
                self.update_state()

    def inventory_render(self):
        if self.hero.inventory.opened:
            self.display.blit(self.hero.inventory.background, (20, 50))
            self.display.blit(self.hero.inventory.info_background, (600, 50))
            text = [self.hero.inventory.font_big.render(str(self.hero.get_attack())[0:6], True, (200, 220, 180)),
                    self.hero.inventory.font_big.render(str(self.hero.get_protection())[0:6], True, (200, 220, 180)),
                    self.hero.inventory.font_big.render(str(self.hero.info)[0:9], True, (200, 220, 180)),
                    self.hero.inventory.font_big.render(str(self.hero.level)[0:4], True, (200, 220, 180)),
                    self.hero.inventory.font_default.render((str(self.hero.hp))[:4] + "/" + str(self.hero.get_max_hp()),
                                                            True, (200, 220, 180)),
                    self.hero.inventory.font_default.render(str(len(self.hero.inventory.item_list)) + "/24"[0:6], True,
                                                            (200, 220, 180))]

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

        if self.hero.stay:
            pg.draw.rect(self.display, (0, 50, 50), (WIN_WIDTH / 2 - 125, 30, 250, 40))
            text = self.hero.inventory.font_default.render("Пропуск хода", True, (200, 200, 200))
            self.display.blit(text, [WIN_WIDTH / 2 - 80, 38])
            self.display.blit(self.time_ico, (WIN_WIDTH / 2 - 123, 32))

        self.display.blit(self.hud_background, (20, 500))
        self.display.blit(self.hud_level_background, (280, 500))

        hp = self.hero.hp / self.hero.get_max_hp()
        mp = self.hero.mp / self.hero.get_max_mp()
        exp = self.hero.experience / (self.hero.level * 10)

        pg.draw.rect(self.display, (255, 50, 50), (70, 514, hp * 196, 31))
        pg.draw.rect(self.display, (50, 50, 255), (70, 559, mp * 196, 26))
        pg.draw.rect(self.display, (200, 200, 200), (70, 604, exp * 196, 11))

        text = [self.hero.inventory.font_ultra_big.render(str(self.hero.level)[0:3], True, (200, 200, 200)),
                self.hero.inventory.font_big.render(str(self.hero.hp)[0:4] + "/" + str(self.hero.get_max_hp()), True,
                                                    (200, 220, 180)),
                self.hero.inventory.font_big.render(str(self.hero.mp) + "/" + str(self.hero.get_max_mp())[0:8], True,
                                                    (200, 200, 200)),
                self.hero.inventory.font_small.render(str(self.hero.experience) + "/" + str(self.hero.level * 10)[0:8],
                                                      True, (10, 20, 10))]

        self.display.blit(text[0], [295, 520])
        self.display.blit(text[1], [100, 517])
        self.display.blit(text[2], [100, 560])
        self.display.blit(text[3], [100, 603])

    def map_render(self):

        self.game_map.print_map(self.display, self.camera, self.images)

        self.camera.coefficient_x = self.camera.apply(Block(0, 0)).x  # Отклонения для x,y
        self.camera.coefficient_y = self.camera.apply(Block(0, 0)).y

    def enemy_render(self):
        for enemy in self.enemies:
            if self.game_map.body[enemy.y][enemy.x].visible is True:
                self.unit_render(enemy)

    def set_enemies(self):
        enemy_count = random.randint(MIN_ENEMY_COUNT, MAX_ENEMY_COUNT)

        for room in self.game_map.rooms[1:]:
            if enemy_count == 0:
                break
            else:
                in_room = random.randint(0, MAX_ENEMY_IN_ROOM)
                for i in range(in_room):
                    enemy = Dwarf.Dwarf()
                    pos_x = random.randint(room.x1, room.x2)
                    pos_y = random.randint(room.y1, room.y2)
                    while self.game_map.body[pos_y][pos_x].symbol != FLOOR_TILE and \
                            self.game_state[pos_y][pos_x].symbol != FLOOR_TILE:
                        pos_x = random.randint(room.x1, room.x2)
                        pos_y = random.randint(room.y1, room.y2)

                    enemy.set_pos(pos_x, pos_y)
                    enemy.set_rect_pos(pos_x * BLOCK_WIDTH, pos_y * BLOCK_HEIGHT)
                    enemy_count -= 1
                    self.enemies.append(enemy)


game = Game()
game.menu()
game.new()
game.run()
