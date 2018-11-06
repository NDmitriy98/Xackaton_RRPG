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
        self.npc_step = False
        self.armed = False

    def look_for_hero(self):
        self.fov.do_fov(self.x, self.y)
        is_hero, pos = self.fov.find_in_fov('@')
        if is_hero:
            self.armed = True
            if not self.hero_is_near(pos[0], pos[1]):
                self.build_path(pos[0], pos[1])
        else:
            self.armed = False

    def hero_is_near(self, hero_x, hero_y):
        near = self.get_destination(hero_x, hero_y)
        if near:
            self.set_attack_direction(hero_x, hero_y)
        else:
            self.armed = False
        return near

