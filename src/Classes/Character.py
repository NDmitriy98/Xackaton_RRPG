from src.Classes import Item
from src.Classes.Unit import Unit


class Character(Unit):
    def __init__(self, experience=0, weapon=None, armor=None, inventory: Item = None):
        super().__init__()
        self.info = "Character"
        self.weapon = weapon
        self.armor = armor
        self.inventory = inventory
        self.experience = experience

    def level_up(self):
        self.level += 1
        self.attack += 1
        self.protection += 1

    def add_experience(self, dp_exp):
        self.experience += dp_exp
        while self.experience > (self.level * 10 + 10):
            self.experience -= (self.level * 10 + 10)
            self.level_up()

