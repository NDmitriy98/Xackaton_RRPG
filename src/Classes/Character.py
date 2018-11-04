from pygame.rect import Rect

from src.Classes import Item, Armor, Weapon, Inventory
from src.Classes.Unit import Unit


class Character(Unit):
    def __init__(self, experience=0, inventory = None):
        super().__init__()

        self.info = "Character"
        self.inventory: Inventory = inventory
        self.experience = experience
        self.hp = 20
        self.mp = 10
        self.level = 1
        self.attack = 1
        self.protection = 1
        if inventory:
            if inventory.weapon:
                self.full_attack = self.attack + inventory.weapon.get_attack()  # Атака с учётом снаряжения
            else:
                self.full_attack = self.attack

            if inventory.armor:
                self.full_protection = self.protection + inventory.armor.get_protection()
            else:
                self.full_protection = self.protection
        else:
            self.full_attack = self.attack
    def level_up(self):
        self.level += 1
        self.attack += 1
        self.protection += 1
        self.hp += 10
        self.mp += 10

    def add_experience(self, dp_exp):  # Получение опыта
        self.experience += dp_exp
        while self.experience > (self.level * 10):
            self.experience -= (self.level * 10)
            self.level_up()

    def get_max_hp(self):
        return 10 + self.level * 10
    def get_max_mp(self):
        return self.level * 10

    def get_attack(self):
        if self.inventory.weapon:
            return self.attack + self.inventory.weapon.attack
        else:
            return self.attack

    def get_protection(self):
        if self.inventory.armor:
            return self.protection + self.inventory.armor.protection
        else:
            return self.protection

    def in_damage(self, incoming_damage):  # Входящий урон
        if self.inventory.armor:
            clean_damage = incoming_damage / ((10 + self.protection + self.inventory.armor.protection) / 10)
        else:
            clean_damage = incoming_damage / ((10 + self.protection ) / 10)
        self.hp -= clean_damage
        if self.hp <= 0:
            self.hp = 0
            self.death()


    def set_weapon(self, weapon: Weapon.Weapon):
        self.inventory.weapon = weapon
        self.full_attack = self.attack + weapon.attack

    def set_armor(self, armor: Armor.Armor):
        self.inventory.armor = armor
        self.full_protection = self.protection + armor.protection
