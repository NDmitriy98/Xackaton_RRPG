from src.Classes.Object import Object


class Unit(Object):
    def __init__(self, hp=10, mp=10, attack=0, protection=0):
        super().__init__()
        self.info = "Unit"
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.protection = protection

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

    def set_attack(self, attack):
        self.attack = attack

    def set_attack(self, protection):
        self.protection = protection

    def set_attack(self, protection):
        self.protection = protection


