from pygame.rect import Rect

from src.Classes import Item, Armor, Weapon, Inventory
from src.Classes.Unit import Unit


class Character(Unit):
    def __init__(self, experience=0, inventory = None):
        super().__init__()

        self.info = "Character"
        self.inventory: Inventory = inventory
        self.experience = experience
        self.hp = 10
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

        self.full_attack += 1
        self.full_protection += 1

    def add_experience(self, dp_exp):  # Получение опыта
        self.experience += dp_exp
        while self.experience > (self.level * 10):
            self.experience -= (self.level * 10)
            self.level_up()

    def get_attack(self):
        return self.attack + self.inventory.weapon.attack

    def get_protection(self):
        return self.protection + self.inventory.armor.protection

    def set_weapon(self, weapon: Weapon.Weapon):
        self.inventory.weapon = weapon
        self.full_attack = self.attack + weapon.attack

    def set_armor(self, armor: Armor.Armor):
        self.inventory.armor = armor
        self.full_protection = self.protection + armor.protection
