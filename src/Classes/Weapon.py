from src.Classes.Item import Item


class Weapon(Item):
    def __init__(self, attack=0, condition=100):
        super().__init__()
        self.attack = attack
        self.condition = condition
        self.info = "Weapon"

    def get_attack(self):
        return self.attack

