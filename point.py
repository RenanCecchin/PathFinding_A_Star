from math import sqrt

class Point:
    def __init__(self, x, y, cost = 0):
        self.x = x
        self.y = y
        self.cost = cost

    def addCost(self, point):
        self.cost += abs(sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2))

    def getCost(self):
        return self.cost

    def getPoint(self):
        return (self.x, self.y)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) +  ", " + str(self.cost) + ")"
        