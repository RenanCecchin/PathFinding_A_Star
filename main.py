from map import Map
from pathfinding import Pathfinding


#Funcao main
def main():
    tmap = Map("Berlin_0_1024.map")
    tmap.read_map()
    points = tmap.generate_random_points(100)
    for point in points:
        Pathfinding(point[0], point[1], tmap, False)    #Start, End, Map
        Pathfinding(point[0], point[1], tmap, True)    #Start, End, Map

if __name__ == '__main__':
    main()