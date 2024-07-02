class Tree:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.cost = 0

    def add_cost(self, value):
        self.cost += value

    def get_cost(self):
        return self.cost