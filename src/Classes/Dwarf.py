from src.Classes.Enemy import Enemy
from src.Tile import *
from src.Animations.DwarfAnimation import *


class Dwarf(Enemy):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.attack = 2
        self.protection = 1
        self.hp = 10
        self.info = "Dwarf"
        self.tile = Tile(DWARF_TILE, True)
        #self.down = True
       #self.stay = False
        self.current_path = []
        """["L", "U", "R", "D","L", "U", "R", "D", "L", "U", "R", "D","L", "U", "R", "D",
                         "L", "U", "R", "D", "L", "U", "R", "D", "L", "U", "R", "D", "L", "U", "R", "D",
                         "L", "U", "R", "D", "L", "U", "R", "D", "L", "U", "R", "D", "L", "U", "R", "D",
                         "L", "U", "R", "D", "L", "U", "R", "D", "L", "U", "R", "D", "L", "U", "R", "R"]
"""


        self.animStayUp = self.makeAnim(ANIMATION_STAY_UP, ANIMATION_DELAY)
        self.animStayUp.play()

        self.animStayDown = self.makeAnim(ANIMATION_STAY_DOWN, ANIMATION_DELAY)
        self.animStayDown.play()

        self.animStayRight = self.makeAnim(ANIMATION_STAY_RIGHT, ANIMATION_DELAY)
        self.animStayRight.play()

        self.animStayLeft = self.makeAnim(ANIMATION_STAY_LEFT, ANIMATION_DELAY)
        self.animStayLeft.play()

        self.animMoveUp = self.makeAnim(ANIMATION_MOVE_UP, ANIMATION_DELAY)
        self.animMoveUp.play()

        self.animMoveDown = self.makeAnim(ANIMATION_MOVE_DOWN, ANIMATION_DELAY)
        self.animMoveDown.play()

        self.animMoveRight = self.makeAnim(ANIMATION_MOVE_RIGHT, ANIMATION_DELAY)
        self.animMoveRight.play()

        self.animMoveLeft = self.makeAnim(ANIMATION_MOVE_LEFT, ANIMATION_DELAY)
        self.animMoveLeft.play()

        self.animAttackUp = self.makeAnim(ANIMATION_ATTACK_UP, ANIMATION_DELAY)
        self.animAttackUp.play()

        self.animAttackDown = self.makeAnim(ANIMATION_ATTACK_DOWN, ANIMATION_DELAY)
        self.animAttackDown.play()

        self.animAttackRight = self.makeAnim(ANIMATION_ATTACK_RIGHT, ANIMATION_DELAY)
        self.animAttackRight.play()

        self.animAttackLeft = self.makeAnim(ANIMATION_ATTACK_LEFT, ANIMATION_DELAY)
        self.animAttackLeft.play()



