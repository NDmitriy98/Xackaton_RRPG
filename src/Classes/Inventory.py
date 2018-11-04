import pygame

from src.Classes import Weapon, Armor
from src.Classes.Item import Item


class Inventory:
    def __init__(self, display, character):
        self.item_list = []
        self.weapon: Weapon = None
        self.armor: Armor = None
        self.background = pygame.image.load('Drawable/inventory.png')
        self.item_background = pygame.image.load('Drawable/item_background.png')
        self.display = display
        self.character = character
        self.item_info = False
        self.item_num = None
        self.item_x = 0
        self.item_y = 0
        self.font = pygame.font.Font(None, 26)
        self.font_small = pygame.font.Font(None, 22)

    def add_item(self, item: Item):
        if len(self.item_list) != 24:
            self.item_list.append(item)


    def render_inventory(self):
        self.display.blit(self.background, (20, 50))
        i = j = 0
        if self.character.inventory:
            for item in self.item_list:
                self.display.blit(item.img, (50 + i * 50, 65 + j * 50))
                i += 1
                if i == 4:
                    j += 1
                    i = 0
        if self.item_info:
            self.display.blit(self.item_background,(self.item_x, self.item_y))
            self.display.blit(self.item_list[self.item_num].img, (self.item_x + 10, self.item_y + 23, 40, 40))

            text = self.font.render(self.item_list[self.item_num].info[0:17], True, (200, 220, 180))
            text_dis = self.font_small.render(self.item_list[self.item_num].description[0:17], True, (200, 220, 180))
            text_cost = self.font.render(str(self.item_list[self.item_num].cost)[0:5], True, (200, 220, 180))

            self.display.blit(text, [self.item_x + 70, self.item_y + 40])
            self.display.blit(text_dis, [self.item_x + 70, self.item_y + 85])
            self.display.blit(text_cost, [self.item_x + 160, self.item_y + 120])

        if self.weapon:
            self.display.blit(self.weapon.img, (70, 385))
        if self.armor:
            self.display.blit(self.armor.img, (180, 385))


    def inventory_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                block = False
                if self.item_info:
                    if self.item_x + 140 > mouse_position[0] > self.item_x + 15 and \
                            self.item_y + 190 > mouse_position[1] > self.item_y+150:
                        block = True
                        use = self.item_list[self.item_num].use()
                        if use:
                            if use.class_name == "Weapon":
                                if self.weapon:
                                    temp = self.weapon
                                    self.weapon = use
                                    self.item_list[self.item_num] = temp
                                else:
                                    self.weapon = use
                                    del self.item_list[self.item_num]

                            if use.class_name == "Armor":
                                if self.armor:
                                    temp = self.armor
                                    self.armor = use
                                    self.item_list[self.item_num] = temp
                                else:
                                    self.armor = use
                                    del self.item_list[self.item_num]
                        else:
                            del self.item_list[self.item_num]
                        self.item_info = False
                            #print("use")
                    if self.item_x + 235 > mouse_position[0] > self.item_x + 155 and \
                            self.item_y + 190 > mouse_position[1] > self.item_y + 150:
                        block = True
                        del self.item_list[self.item_num]
                        self.item_info = False
                        #print("del")

                if 260 > mouse_position[0] > 50 and 365 > mouse_position[1] > 65 and not block:
                    x = mouse_position[0] - 50
                    y = mouse_position[1] - 65
                    res = 4 * int(y / 50) + int(x / 50)
                    print("num " + str(res))
                    if len(self.item_list) > res:
                        self.item_info = True
                        self.item_num = res
                        self.item_x = mouse_position[0] + 40
                        self.item_y = mouse_position[1] - 15
                if 120 > mouse_position[0] > 70 and 435 > mouse_position[1] > 385 and not block:
                    print("yes!")
                    self.item_list.append(self.weapon)
                    self.weapon = None
                if 230 > mouse_position[0] > 180 and 435 > mouse_position[1] > 385 and not block:
                    print("yes!")
                    self.item_list.append(self.armor)
                    self.armor = None








