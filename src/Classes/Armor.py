from src.Classes.Item import Item


class Armor(Item):
    def __init__(self, protection=0, strength=0):
        super().__init__()
        self.protection = protection
        self.strength = strength


