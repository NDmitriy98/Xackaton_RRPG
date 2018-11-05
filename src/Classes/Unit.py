from src import pyganim
from src.Classes.Object import Object
from src.Point.Point import Point
from src.a_star_path_find import PathFinder
from src.tile_list import *
from src.FOV import FOV


class Unit(Object):
    def __init__(self, hp=0, mp=0, attack=0, protection=0, level=0):
        super().__init__()
        self.info = "Unit"
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.protection = protection
        self.level = level
        self.alive = True
        self.view_range = 5
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.stay = True
        self.stay_up = True
        self.stay_down = False
        self.stay_right = False
        self.stay_left = False
        self.attack_up = False
        self.attack_down = False
        self.attack_right = False
        self.attack_left = False
        self.path_finder: PathFinder = None
        self.fov: FOV = None
        self.current_path = []
        self.iterations = 0

    def death(self):
        self.alive = False

    def makeAnim(self, animList, delay):
        boltAnim = []
        for anim in animList:
            boltAnim.append((anim, delay))
        Anim = pyganim.PygAnimation(boltAnim)
        return Anim

    def in_damage(self, incoming_damage):  # Входящий урон
        clean_damage = incoming_damage / ((10 + self.protection) / 10)
        self.hp -= clean_damage
        if self.hp <= 0:
            self.hp = 0
            self.death()

    def get_hp(self):
        return self.hp

    def set_hp(self, hp):
        self.hp = hp

    def get_mp(self):
        return self.mp

    def set_mp(self, mp):
        self.mp = mp

    def get_attack(self):
        return self.attack

    def set_attack(self, attack):
        self.attack = attack

    def get_protection(self):
        return self.protection

    def set_protection(self, protection):
        self.protection = protection




    def falseStay(self):
        self.stay = False
        self.stay_up = False
        self.stay_down = False
        self.stay_right = False
        self.stay_left = False

    def falseMove(self):
        self.up = False
        self.down = False
        self.right = False
        self.left = False

    def falseAttack(self):
        self.attack_up = False
        self.attack_down = False
        self.attack_right = False
        self.attack_left = False

    def init_fov(self, map_body):
        self.fov = FOV(map_body, radius_=self.view_range)

    def view(self):
        self.fov.do_fov(self.x, self.y)

    def init_path_finder(self, map_body):
        self.path_finder = PathFinder(map_body)

    def convert_path_to_letters(self, path):
        temp_path = path
        temp_path.reverse()
        previous = temp_path[0]
        for cell in temp_path[1:]:
            if previous[0] - cell[0] == -1 and previous[1] - cell[1] == 0:
                self.current_path.append('R')
            if previous[0] - cell[0] == 0 and previous[1] - cell[1] == -1:
                self.current_path.append('U')
            if previous[0] - cell[0] == 1 and previous[1] - cell[1] == 0:
                self.current_path.append('L')
            if previous[0] - cell[0] == 0 and previous[1] - cell[1] == 1:
                self.current_path.append('D')
            previous = cell

        self.current_path.reverse()


    def build_path(self, to_x, to_y, forbidden_symb=None):
        if forbidden_symb is None:
            forbidden_symb = {WALL_TILE}
        temp_path = self.path_finder.find_path(Point(self.x, self.y), Point(to_x, to_y), forbidden_symb)
        if not temp_path:
            temp_path = self.path_finder.find_path(Point(self.x, self.y), Point(to_x+1, to_y), forbidden_symb)
        self.convert_path_to_letters(temp_path)

