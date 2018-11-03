import pygame
from src.Classes.Item import Item


class Inventory:
    def __init__(self, display, character):
        self.item_list = []
        self.background = pygame.image.load('Drawable/inventory.png')
        self.display = display
        self.character = character

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

