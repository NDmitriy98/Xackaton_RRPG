from src.Classes.Item import Item


class Weapon(Item):
    def __init__(self, attack=1, condition=100):
        super().__init__()
        self.attack = attack
        self.condition = condition
        self.info = "Weapon"
        self.class_name = "Weapon"
        self.description = "Урон = " + str(self.attack)

    def set_attack(self, attack):
        self.attack = attack
        self.description = "Урон = " + str(self.attack)

    def get_attack(self):
        return self.attack

    def use(self = None):
        #print("Used weapon")
        return self

