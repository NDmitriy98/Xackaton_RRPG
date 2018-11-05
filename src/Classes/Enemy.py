from src.Classes import Item
from src.Classes.Unit import Unit


class Enemy(Unit):
    def __init__(self, attitude=1, visibility=0, drop: Item = None):
        super().__init__()
        self.info = "Enemy"
        self.attitude = attitude
        self.drop = drop
        self.visibility = visibility
        self.tile.symbol = 'E'
