from tree import Tree
from time import time

class Pathfinding:                          #Algoritmo A* de pathfinding
    def __init__(self, start, end, map, pixel):
        #Acha os nodos mais proximos ao nodo inicial e final no grafo de visibilidade
        self.map = map
        print(len(map.nodes))
        self.start = self.map.connect_nodes(start.getPoint())
        self.end = self.map.connect_nodes(end.getPoint())
        self.start.calculate_heuristic(self.end)

        self.pixel = pixel #Booleano que indica se o mapa usa os pixels ou o grafo de visibilidade

        self.tree = Tree(self.start)
        self.closed = []
        self.open = []
        self.open.append(self.tree)

        #Cria o arquivo de saida e salva o tempo inicial para medir o tempo de processamento
        self.initial_time = time()
        self.savefile = open("results.txt", 'a')
        strg = "Inicio: " + str(self.start) + " Fim: " + str(self.end) + "\n"        #String que mostra o estado atual do problema

        if(self.pixel):    #Se estiver no modo pixel gera os caminhos adjacentes ao ponto inicial no mapa
            self.map.generate_unit_paths(self.start)
            strg += "Mapa usando pixels\n"
        else:
            strg += "Mapa usando grafo de visibilidade\n"

        print(strg)                                                                       #Printa a string
        self.savefile.write(strg)                                                         #Salva a string no arquivo

        self.find_path()

    def find_path(self):
        while(len(self.open) > 0):
            #Retira o elemento com menor custo + heuristica da fila de nodos abertos
            current_node = min(self.open, key=lambda x: x.data.get_heuristic() + x.get_cost())        
            self.open.remove(current_node)
            current_map = current_node.data

            if current_map.get_point() == self.end.get_point():                                                         #Se o nodo atual for o nodo final, retorna o caminho
                print("Caminho:")
                self.savefile.write("Caminho: \n")
                stack = []
                while current_node.parent is not None:                                                                  #Percorre a arvore até o nó inicial e coloca em uma pilha
                    stack.append(current_node)
                    current_node = current_node.parent
                stack.append(current_node)   

                for movement in reversed(stack):                                                                         #Desempilha para mostrar a sequencia certa de movimentos
                    strg = str(movement.data) + "\n"
                    print(strg)
                    self.savefile.write(strg)

                strg = "Numero de nodos abertos: " + str(len(self.closed) + len(self.open)) + "\n"                      #Salva no arquivo o numero de nodos abertos e fechados
                strg +=("Tempo de execucao: " + str(time() - self.initial_time) + "\n")                                 #Salva no arquivo o tempo de execucao
                self.savefile.write(strg)
                self.savefile.close()
                self.map.reset_nodes()
                return True
            
            if(self.pixel):
                self.generate_new_pixel_nodes(current_node)
            else:
                self.generate_new_nodes(current_node)                                                                       #Gera os novos nodos filhos do nodo atual
            self.closed.append(current_node)                                                                             #Adiciona o nodo atual na lista de nodos fechados

        strg = "Impossivel encontrar caminho\n" + "Numero de nodos abertos: " + str(len(self.closed) + len(self.open))  + "\n"
        strg += ("Tempo de execucao: " + str(time() - self.initial_time) + "\n")
        self.savefile.write(strg)
        return False
        


    #Funcao que refatora as listas de nodos abertos e fechados
    # @param point: ponto que sera verificado se esta na lista de nodos abertos ou fechados
    # @return: True se o ponto estiver na lista de nodos abertos ou fechados, False caso contrario
    def refactorLists(self, point):
        found = False
        for i in range(0, len(self.open)):
            if self.open[i].data.get_point() == point.get_point():                         #Procura o elemento na lista dos nodos abertos 
                found = True
                if point.get_heuristic() < self.open[i].data.get_heuristic():         #Se encontrar e o custo for menor, retira o elemento
                    self.open.pop(i)

        for i in range(0, len(self.closed)):    
            if self.closed[i].data.get_point() == point.get_point():                       #Procura o elemento na lista dos nodos fechados
                found = True
                if point.get_heuristic() < self.closed[i].data.get_heuristic():       #Se encontrar e o custo for menor, retira o elemento
                    self.closed.pop(i)
        return found

    #Gera novos nodos utilizando o grafo de visibilidade
    def generate_new_nodes(self, current_node):
        #Pega os nodos vizinhos do nodo atual
        visible_paths = current_node.data.get_paths()

        for path in visible_paths:                                                         #Verifica todos os vizinhos do nodo
            child = path
            child.calculate_heuristic(self.end)                                            #Calcula a heuristica do nodo filho
            if not self.refactorLists(child):                                              #Se o ponto nao estiver na lista de nodos abertos ou fechados, adiciona na lista de abertos
                child = Tree(child, current_node)
                child.add_cost(current_node.data.get_distance(child.data))
                self.open.append(child)

    def generate_new_pixel_nodes(self, current_node):
        #Gera os caminhos adjacentes
        self.map.generate_unit_paths(current_node.data)

        #Pega os nodos vizinhos do nodo atual
        visible_paths = current_node.data.get_paths()

        for path in visible_paths:                                                         #Verifica todos os vizinhos do nodo
            child = path
            child.calculate_pixel_heuristic(self.end)                                            #Calcula a heuristica do nodo filho
            if not self.refactorLists(child):                                              #Se o ponto nao estiver na lista de nodos abertos ou fechados, adiciona na lista de abertos
                child = Tree(child, current_node)
                child.add_cost(1)                                                          #O custo sempre sera 1 pois o movimento eh unitario
                self.open.append(child)

