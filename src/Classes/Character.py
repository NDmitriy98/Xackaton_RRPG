import pygame

from pygame.rect import Rect

from src import pyganim
from src.Classes import Item, Armor, Weapon, Inventory
from src.Classes.Unit import Unit

ANIMATION_DELAY = 0.15


ANIMATION_ATTACK_UP = ['Drawable/hero/attack_up1.png',
                       'Drawable/hero/attack_up2.png',
                       'Drawable/hero/attack_up3.png',
                       'Drawable/hero/attack_up4.png',
                       'Drawable/hero/attack_up5.png']

ANIMATION_ATTACK_DOWN = ['Drawable/hero/attack_down1.png',
                         'Drawable/hero/attack_down2.png',
                         'Drawable/hero/attack_down3.png',
                         'Drawable/hero/attack_down4.png',
                         'Drawable/hero/attack_down5.png']

ANIMATION_ATTACK_RIGHT = ['Drawable/hero/attack_right1.png',
                          'Drawable/hero/attack_right2.png',
                          'Drawable/hero/attack_right3.png',
                          'Drawable/hero/attack_right4.png',
                          'Drawable/hero/attack_right5.png']

ANIMATION_ATTACK_LEFT = ['Drawable/hero/attack_left1.png',
                         'Drawable/hero/attack_left2.png',
                         'Drawable/hero/attack_left3.png',
                         'Drawable/hero/attack_left4.png',
                         'Drawable/hero/attack_left5.png']


ANIMATION_STAY_UP = ['Drawable/hero/stay_up1.png',
                     'Drawable/hero/stay_up2.png',
                     'Drawable/hero/stay_up3.png',
                     'Drawable/hero/stay_up4.png']

ANIMATION_STAY_UP = ['Drawable/hero/stay_up1.png',
                     'Drawable/hero/stay_up2.png',
                     'Drawable/hero/stay_up3.png',
                     'Drawable/hero/stay_up4.png']

ANIMATION_STAY_DOWN = ['Drawable/hero/stay_down1.png',
                       'Drawable/hero/stay_down2.png',
                       'Drawable/hero/stay_down3.png',
                       'Drawable/hero/stay_down4.png']

ANIMATION_STAY_RIGHT = ['Drawable/hero/stay_right1.png',
                        'Drawable/hero/stay_right2.png',
                        'Drawable/hero/stay_right3.png',
                        'Drawable/hero/stay_right4.png']

ANIMATION_STAY_LEFT = ['Drawable/hero/stay_left1.png',
                       'Drawable/hero/stay_left2.png',
                       'Drawable/hero/stay_left3.png',
                       'Drawable/hero/stay_left4.png']


ANIMATION_MOVE_UP = ['Drawable/hero/move_up1.png',
                     'Drawable/hero/move_up2.png',
                     'Drawable/hero/move_up3.png',
                     'Drawable/hero/move_up4.png',
                     'Drawable/hero/move_up5.png',
                     'Drawable/hero/move_up6.png']
ANIMATION_MOVE_DOWN = ['Drawable/hero/move_down1.png',
                       'Drawable/hero/move_down2.png',
                       'Drawable/hero/move_down3.png',
                       'Drawable/hero/move_down4.png',
                       'Drawable/hero/move_down5.png',
                       'Drawable/hero/move_down6.png']
ANIMATION_MOVE_RIGHT = ['Drawable/hero/move_right1.png',
                        'Drawable/hero/move_right2.png',
                        'Drawable/hero/move_right3.png',
                        'Drawable/hero/move_right4.png',
                        'Drawable/hero/move_right5.png',
                        'Drawable/hero/move_right6.png']
ANIMATION_MOVE_LEFT = ['Drawable/hero/move_left1.png',
                       'Drawable/hero/move_left2.png',
                       'Drawable/hero/move_left3.png',
                       'Drawable/hero/move_left4.png',
                       'Drawable/hero/move_left5.png',
                       'Drawable/hero/move_left6.png']

class Character(Unit):
    def __init__(self, experience=0, inventory = None):
        super().__init__()

        self.info = "Character"
        self.inventory: Inventory = inventory
        self.experience = experience
        self.hp = 20
        self.mp = 10
        self.level = 1
        self.attack = 1
        self.protection = 1
        self.tile.symbol = '@'

        self.old_x = 0
        self.old_y = 0

        def makeAnim(animList, delay):
            boltAnim = []
            for anim in animList:
                boltAnim.append((anim,delay))
            Anim = pyganim.PygAnimation(boltAnim)
            return Anim

        self.animStayUp = makeAnim(ANIMATION_STAY_UP, ANIMATION_DELAY)
        self.animStayUp.play()

        self.animStayDown = makeAnim(ANIMATION_STAY_DOWN, ANIMATION_DELAY)
        self.animStayDown.play()

        self.animStayRight = makeAnim(ANIMATION_STAY_RIGHT, ANIMATION_DELAY)
        self.animStayRight.play()

        self.animStayLeft = makeAnim(ANIMATION_STAY_LEFT, ANIMATION_DELAY)
        self.animStayLeft.play()

        self.animMoveUp = makeAnim(ANIMATION_MOVE_UP, ANIMATION_DELAY)
        self.animMoveUp.play()

        self.animMoveDown = makeAnim(ANIMATION_MOVE_DOWN, ANIMATION_DELAY)
        self.animMoveDown.play()

        self.animMoveRight = makeAnim(ANIMATION_MOVE_RIGHT, ANIMATION_DELAY)
        self.animMoveRight.play()

        self.animMoveLeft = makeAnim(ANIMATION_MOVE_LEFT, ANIMATION_DELAY)
        self.animMoveLeft.play()

        self.animAttackUp = makeAnim(ANIMATION_ATTACK_UP, ANIMATION_DELAY)
        self.animAttackUp.play()

        self.animAttackDown = makeAnim(ANIMATION_ATTACK_DOWN, ANIMATION_DELAY)
        self.animAttackDown.play()

        self.animAttackRight = makeAnim(ANIMATION_ATTACK_RIGHT, ANIMATION_DELAY)
        self.animAttackRight.play()

        self.animAttackLeft = makeAnim(ANIMATION_ATTACK_LEFT, ANIMATION_DELAY)
        self.animAttackLeft.play()



        if inventory:
            if inventory.weapon:
                self.full_attack = self.attack + inventory.weapon.get_attack()  # Атака с учётом снаряжения
            else:
                self.full_attack = self.attack

            if inventory.armor:
                self.full_protection = self.protection + inventory.armor.get_protection()
            else:
                self.full_protection = self.protection
        else:
            self.full_attack = self.attack
    def level_up(self):
        self.level += 1
        self.attack += 1
        self.protection += 1
        self.hp += 10
        self.mp += 10

    def add_experience(self, dp_exp):  # Получение опыта
        self.experience += dp_exp
        while self.experience > (self.level * 10):
            self.experience -= (self.level * 10)
            self.level_up()

    def get_max_hp(self):
        return 10 + self.level * 10
    def get_max_mp(self):
        return self.level * 10

    def get_attack(self):
        if self.inventory.weapon:
            return self.attack + self.inventory.weapon.attack
        else:
            return self.attack

    def get_protection(self):
        if self.inventory.armor:
            return self.protection + self.inventory.armor.protection
        else:
            return self.protection

    def in_damage(self, incoming_damage):  # Входящий урон
        if self.inventory.armor:
            clean_damage = incoming_damage / ((10 + self.protection + self.inventory.armor.protection) / 10)
        else:
            clean_damage = incoming_damage / ((10 + self.protection ) / 10)
        self.hp -= clean_damage
        if self.hp <= 0:
            self.hp = 0
            self.death()


    def set_weapon(self, weapon: Weapon.Weapon):
        self.inventory.weapon = weapon
        self.full_attack = self.attack + weapon.attack

    def set_armor(self, armor: Armor.Armor):
        self.inventory.armor = armor
        self.full_protection = self.protection + armor.protection


    def falseStay(self):
        self.stay = False
        self.stay_up = False
        self.stay_down = False
        self.stay_right = False
        self.stay_left = False

    def falseMove(self):
        self.up = False
        self.down = False
        self.right = False
        self.left = False

    def falseAttack(self):
        self.attack_up = False
        self.attack_down = False
        self.attack_right = False
        self.attack_left = False
