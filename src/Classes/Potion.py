from src.Classes.Item import Item


class Potion(Item):
    def __init__(self):
        super().__init__()

    def use(self = None):
        print("poition use")
