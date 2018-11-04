class Item:
    def __init__(self, cost=1, weight=1):
        self.cost = cost
        self.weight = weight
        self.info = "Item"
        self.description = "None"
        self.class_name = "Item"
        self.use()

    def use(self):
        print("Used")

