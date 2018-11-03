from src.Classes import Item, Armor, Weapon
from src.Classes.Unit import Unit


class Character(Unit):
    def __init__(self, experience=0, weapon: Weapon.Weapon = None, armor: Armor.Armor = None, inventory: Item.Item = None):
        super().__init__()
        self.info = "Character"
        self.weapon = weapon
        self.armor = armor
        self.inventory = inventory
        self.experience = experience
        self.hp = 10
        self.level = 1

        if weapon:
            self.full_attack = self.attack + weapon.get_attack()  # Атака с учётом снаряжения
        else:
            self.full_attack = self.attack

        if armor:
            self.full_protection = self.protection + armor.get_protection()
        else:
            self.full_protection = self.protection

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

    def get_damage(self):
        return self.full_attack

    def set_weapon(self, weapon: Weapon.Weapon):
        self.weapon = weapon
        self.full_attack = self.attack + weapon.attack
