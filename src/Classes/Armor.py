from src.Classes.Item import Item


class Armor(Item):
    def __init__(self, protection=0, condition=100):
        super().__init__()
        self.protection = protection
        self.condition = condition
        self.info = "Armor"

    def get_protection(self):
        return self.protection


