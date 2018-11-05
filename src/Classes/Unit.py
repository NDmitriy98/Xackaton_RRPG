from src.Classes.Object import Object
from src.Point.Point import Point
from src.a_star_path_find import PathFinder
from src.tile_list import *


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
        self.current_path = []

    def death(self):
        self.alive = False

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

    def init_path_finder(self, map_body):
        self.path_finder = PathFinder(map_body)

    def build_path(self, to_x, to_y, forbidden_symb = set(WALL_TILE)):
        self.current_path = self.path_finder.find_path(Point(self.x, self.y), Point(to_x, to_y), forbidden_symb)
