from src.Classes.Item import Item


class Armor(Item):
    def __init__(self, protection=1, condition=100):
        super().__init__()
        self.protection = protection
        self.condition = condition
        self.info = "Armor"
        self.class_name = "Armor"
        self.description = "Защита = " + str(self.protection)

    def set_protection(self, protection):
        self.protection = protection
        self.description = "Защита = " + str(self.protection)

    def get_protection(self):
        return self.protection

    def use(self = None):
        #print("Used weapon")
        return self
