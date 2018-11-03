from abc import abstractmethod

import src.Classes.Enemy as Enemy
import src.Classes.Character as Character
import src.a_star_path_find as PathFind
import src.Map as Map
import src.AI.Controller

class AI:
    def __init__(self, controller):
        self.controller = controller

        @abstractmethod
        def do_ai_action():
            pass

