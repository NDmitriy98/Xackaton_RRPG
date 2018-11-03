from src.Classes.Enemy import Enemy


class Skeleton(Enemy):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.attack = 2
        self.protection = 1
        self.hp = 10
        self.info = "Skeleton"



