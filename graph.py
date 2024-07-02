from math import sqrt

class Graph:
    def __init__(self, data):
        self.data = data        #Conteudo do nodo
        self.paths = []         #Lista de nodos vizinhos
        self.heuristic = 0      #Heuristica do nodo
        self.d = 500

    def add_path(self, node):
        node.set_path(self)
        self.paths.append(node)

    def get_paths(self):
        return self.paths

    def get_point(self):
        return self.data

    def get_heuristic(self):
        return self.heuristic

    def get_distance(self, node):
        goal = node.get_point()
        return sqrt((self.data[0] - goal[0]) ** 2 + (self.data[1] - goal[1]) ** 2)

    def set_path(self, obj):
        self.paths.append(obj)

    def not_in_paths(self, node):
        for path in self.paths:
            if path.get_point() == node.get_point():
                return False
        return True

    def calculate_heuristic(self, node):
        goal = node.get_point()
        self.heuristic = sqrt((self.data[0] - goal[0]) ** 2 + (self.data[1] - goal[1]) ** 2)
        return self.heuristic

    
    def calculate_pixel_heuristic(self, node):
        goal = node.get_point()
        self.heuristic = abs(self.data[0] - goal[0]) + abs(self.data[1] - goal[1])
        #Pune ele por andar proximo a um caminho com muitos obstaculos, por consequencia com menos caminhos
        return ((17 - (len(self.paths)**2)))*self.heuristic

    def __str__(self):
        return str(self.data)