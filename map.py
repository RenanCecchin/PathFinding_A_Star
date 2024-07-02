from random import randint
from point import Point
from graph import Graph
from copy import deepcopy

class Map:
    def __init__(self, filename):
        self.map = []
        self.original_nodes = []
        self.nodes = []
        self.filename = filename
        self.width = 0
        self.height = 0

    def read_map(self):                         #Le o mapa e armazena todos os cantos em uma lista de tuplas
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            self.height = int(lines[1][7:])
            self.width = int(lines[2][5:])
            lines = lines[4:]                   #Remove header
            self.map = lines
            for j in range(self.height):
                for i in range(self.width):
                    sum = 0                     #Soma cada lado que nao possuir um @ adjacente
                    #Identifica se o no e um vertice ou nao:
                    if self.is_obstacle(j, i):
                        if i+1 < self.width:    #Caso o @ esteja no canto direito ele ainda pode ser um canto
                            if not self.is_obstacle(j, i+1):
                                sum += 1
                        else:
                            sum +=1
                        
                        if i-1 >= 0:           #Caso o @ esteja no canto esquerdo ele ainda pode ser um canto
                            if not self.is_obstacle(j , i-1):
                                sum += 1
                        else:
                            sum +=1

                        if j+1 < self.height:   #Caso o @ esteja no canto superior ele ainda pode ser um canto
                            if not self.is_obstacle(j+1, i):
                                sum += 1
                        else:
                            sum +=1

                        if j-1 >= 0:            #Caso o @ esteja no canto inferior ele ainda pode ser um canto
                            if not self.is_obstacle(j-1, i):
                                sum += 1
                        else:
                            sum +=1
                        if(sum > 2):           #Caso o @ seja um canto
                            self.nodes.append(Graph((j,i)))
        self.preprocess_map()

    def preprocess_map(self):
        print("Preprocessing map with {} nodes...".format(len(self.nodes)))
        for node in self.nodes:
            for visible_node in self.nodes:
                if self.valid_path(node.get_point(), visible_node.get_point()) and node != visible_node and node.not_in_paths(visible_node):
                    #Se o ponto for visivel a outro ponto, nao for o mesmo ponto e nao estiver na lista de vizinhos
                    #Adiciona o nodo a lista de vizinhos
                    node.add_path(visible_node)
        self.original_nodes = list(self.nodes)
        print("Mapa preprocessado")

    def reset_nodes(self):
        self.nodes = list(self.original_nodes)

    #Salva um txt com o mapa e os caminhos
    #Os caminhos serao salvos como uma sequencia de numeros
    def save_path(self, path):
        savefile = open("path.txt", "w")
        for n in range(len(path)):
            j,i = path[n]
            self.map[j] = self.map[j][:i] + str(n) + self.map[j][i+1:]

        for line in self.map:
            savefile.write(line)

    #Retorna verdadeiro se eh possivel acessar um ponto a partir de outro em bater em um obstaculo
    # @param p1: indice do ponto inicial
    # @param p2: indice do ponto final
    def valid_path(self, p1, p2):
        if p1 == p2:
            return False
        aux1 = p1
        aux2 = p2
        if type(p1) is Point:
            aux1 = aux1.getPoint()
        if type(p2) is Point:
            aux2 = aux2.getPoint()
        
        #Digital differential analyser
        dy = aux2[0] - aux1[0]
        dx = aux2[1] - aux1[1]
        step = 0

        if abs(dx) > abs(dy):
            step = abs(dx)
        else:
            step = abs(dy)

        dx = int(dx/step)                                        #Diferenca entre os pontos em x
        dy = int(dy/step)                                        #Diferenca entre os pontos em y

        #A diferenca precisa ser inteira pois eh uma posicao do vetor que sera acessada

        
        for i in range(step):
            #Se o ponto for um obstaculo, retorna falso
            if(self.is_obstacle(aux1[0]+dy, aux1[1]+dx) and aux1 != aux2):
                return False
            aux1 = (aux1[0]+dy, aux1[1]+dx)
        
        return True


    
    #Retorna verdadeiro se o ponto eh um obstaculo
    # @param i: indice da coluna
    # @param j: indice da linha
    def is_obstacle(self, j, i):
        if self.map[j][i] == '@':
            return True
        else:
            return False

    def distance(self, p1, p2):                                     #Calcula a distancia entre dois pontos
        aux1 = p1
        aux2 = p2
        if type(p1) is Point:
            aux1 = aux1.getPoint()
        if type(p2) is Point:
            aux2 = aux2.getPoint()
        return abs(aux1[0]-aux2[0]) + abs(aux1[1]-aux2[1])

    def generate_random_points(self, n):                            #Gera n pontos aleatorios
        points = []
        while len(points) < n:
            x1 = randint(0, self.width-1)
            y1 = randint(0, self.height-1)
            x2 = randint(0, self.width-1)
            y2 = randint(0, self.height-1)
            point_1 = Point(x1, y1)
            point_2 = Point(x2, y2)
            if self.is_obstacle(x1, y1) or self.is_obstacle(x2, y2):
                continue
            else:
                points.append((point_1,point_2))
        return points

    def connect_nodes(self, point):                                 #Conecta um ponto aos nodos visiveis
        n_node = Graph(point)                                       #Cria um nodo com o ponto
        for node in self.nodes:
            if self.valid_path(node.get_point(), n_node.get_point()) and node != n_node and node.not_in_paths(n_node):
                #Se o ponto for visivel a outro ponto, nao for o mesmo ponto e nao estiver na lista de vizinhos
                #Adiciona o nodo a lista de vizinhos
                node.add_path(n_node)
        return n_node

    #Busca um nodo com o ponto passado como parametro
    def search_node(self, point):
        for node in self.nodes:
            if node.get_point() == point:
                return node
        return None

    #Conecta caminhos unitarios (distancia = 1)
    def connect_unit_nodes(self, node_1, point):
        #Se o ponto ja estiver na lista de nodos, retorna ele
        node_2 = self.search_node(point)
        if node_2 != None and node_1.not_in_paths(node_2):
            node_2.add_path(node_1)
        else:
            node_2 = Graph(point)
            if node_1.not_in_paths(node_2):
                node_1.add_path(node_2)
                self.nodes.append(node_2)

    #Gera caminhos usando pontos adjacentes do mapa
    def generate_unit_paths(self, node):
        y,x = node.get_point()
        if y-1 >= 0 and self.is_obstacle(y-1, x) == False:
            self.connect_unit_nodes(node, (y-1, x))

        if y+1 < self.height and self.is_obstacle(y+1, x) == False:
            self.connect_unit_nodes(node, (y+1, x))

        if x-1 >= 0 and self.is_obstacle(y, x-1) == False:
            self.connect_unit_nodes(node, (y, x-1))
            
        if x+1 < self.width and self.is_obstacle(y, x+1) == False:
            self.connect_unit_nodes(node, (y, x+1))
