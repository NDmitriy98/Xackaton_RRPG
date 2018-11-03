import src.Classes.Enemy as Enemy
import src.Classes.Character as Character
import src.a_star_path_find as PathFind
import src.Map as Map


class Controller:
    def __init__(self, enemy: Enemy):
        self.enemy = enemy

    
