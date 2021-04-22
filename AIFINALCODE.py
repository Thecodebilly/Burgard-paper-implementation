import math

import pygame, random

from scipy.spatial import distance


def calculatealgo(tile, bot):
    return tile.utilitycost - coordconstant * euclidiandistance(divcoordsbyscale(tile.coords), divcoordsbyscale(bot.CL))


def assignutilityradius(point, dist):
    for s in range(dist, 0, -1):
        for x in range(width):
            for y in range(height):
                if distance.chebyshev(point, [x, y]) <= s:
                    arr[x][y].utilitycost = s * arr[x][y].utilitycost / dist


def pavelot(point, size):
    for s in range(size):
        for x in range(width):
            for y in range(height):
                if distance.chebyshev(point, [x, y]) <= s:
                    arr[x][y].setobstacleparkinglot()


def euclidiandistance(point1, point2):
    return math.sqrt((math.pow((point2[0] - point1[0]), 2)) + (math.pow((point2[1] - point1[1]), 2)))


def divcoordsbyscale(points):
    newx = int(points[0] / scale)
    newy = int(points[1] / scale)
    newpoint = (newx, newy)
    return newpoint


def multcoordsbyscale(points):
    newx = int(points[0] * scale)
    newy = int(points[1] * scale)
    newpoint = (newx, newy)
    return newpoint


############### NUMBER OF BOTS TO BE TURNED ON ###############
# 1-5
numbots = 5
##############################################################

############# RANGE AT WHICH UTILITY IS DAMPENED #############
# What range would you like to use for the utility calculation, 1-10? (The higher the range the slower the program)
spacingdistance = 2
##############################################################

#################### COORDINATION CONSTANT ###################
#paper reccomends .01-50
coordconstant = 1.5
##############################################################

######################### ENVIORNMENT ########################
#1 or 2
enviornment = 1
##############################################################

xscaled = 0
yscaled = 0
width = 50
height = 50
scale = 10
unit = scale - 1
pygame.init()
arenasize = scale * width + 1
screen = pygame.display.set_mode((arenasize, arenasize))
pygame.display.set_caption('Lawn ' + str(random.randint(1000, 10000)))
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (164, 74, 74)
GREEN = (0, 255, 0)
GRASS = (30, 200, 0)
ORANGE = (255, 69, 0)
GRAY = (128, 128, 128)
BROWN = (205, 133, 63)
screen.fill(WHITE)
discoverednodes = 0
discoveredlist = []
obstacles = 0


class Tile:
    visited = False
    Frontier = False
    frontiercost = 0
    utilitycost = 1
    obstacle = 0
    coords = (0, 0)
    CurrentBOT = None

    def setobstacleparkinglot(self):
        global obstacles
        self.obstacle = 1
        pygame.draw.rect(screen, GRAY, (self.coords[0] + 1, self.coords[1] + 1, unit, unit))


    def setobstaclefence(self):
        global obstacles
        self.obstacle = 1
        pygame.draw.rect(screen, GRAY, (self.coords[0] + 1, self.coords[1] + 1, unit, unit))
        obstacles += 1

    def visitmarker(self):
        global discoveredlist
        global discoverednodes
        pygame.draw.rect(screen, BROWN, (self.coords[1] + 1, self.coords[0] + 1, unit, unit))
        if not self.visited:
            discoverednodes += 1
            self.visited = True

    def frontiermarker(self):
        global Frontiernodes
        if not self.Frontier and not self.visited:
            self.Frontier = True
            self.utilitycost = 1
            divcoord = divcoordsbyscale(self.coords)
            Frontiernodes.append(arr[divcoord[0]][divcoord[1]])
            # pygame.draw.rect(screen, GREEN, (self.coords[0] + 1, self.coords[1] + 1, unit, unit))

    def setcoords(self, coords):
        self.coords = coords
        pygame.draw.rect(screen, GRASS, (self.coords[0] + 1, self.coords[1] + 1, unit, unit))

    def robotinator(self, ROBOT):

        if self.CurrentBOT is None:

            pygame.draw.rect(screen, BROWN, (ROBOT.CL[0] + 1, ROBOT.CL[1] + 1, unit, unit))


        else:
            pygame.draw.rect(screen, GRAY, (ROBOT.CL[0] + 1, ROBOT.CL[1] + 1, unit, unit))
            print("A loud crash was heard at", self.CurrentBOT.CL)

        self.CurrentBOT = ROBOT

        self.frontierNodes = self.getadjacentnodes()

        for x in self.frontierNodes:

            if not x.Frontier and not x.visited and x.obstacle is not 1:
                x.frontiermarker()

                Frontiernodes.append(x)
            # if (not Tile.visited):

    def derobotinator(self):
        self.CurrentBOT = None
        self.visitmarker()

    def getadjacentnodes(self):
        thelist = []
        global arr
        if int(self.coords[0] / scale) - 1 >= 0 and int(self.coords[1] / scale) - 1 >= 0:
            thelist.append(arr[int(self.coords[0] / scale) - 1][int(self.coords[1] / scale) - 1])

        if int(self.coords[0] / scale) - 1 >= 0 and int(self.coords[1] / scale) + 1 < height:
            thelist.append(arr[int(self.coords[0] / scale) - 1][int(self.coords[1] / scale) + 1])

        if int(self.coords[1] / scale) - 1 >= 0:
            thelist.append(arr[int(self.coords[0] / scale)][int(self.coords[1] / scale) - 1])

        if int(self.coords[1] / scale) + 1 < height:
            thelist.append(arr[int(self.coords[0] / scale)][int(self.coords[1] / scale) + 1])

        if int(self.coords[0] / scale) + 1 < width and int(self.coords[1] / scale) + 1 < height:
            thelist.append(arr[int(self.coords[0] / scale) + 1][int(self.coords[1] / scale) + 1])

        if (int(self.coords[0] / scale) + 1) < width and int(self.coords[1] / scale) - 1 >= 0:
            thelist.append(arr[int(self.coords[0] / scale) + 1][int(self.coords[1] / scale) - 1])

        if int(self.coords[0] / scale) + 1 < width:
            thelist.append(arr[int(self.coords[0] / scale) + 1][int(self.coords[1] / scale)])

        if int(self.coords[0] / scale) - 1 >= 0:
            thelist.append(arr[int(self.coords[0] / scale) - 1][int(self.coords[1] / scale)])

        return thelist

    def getadjacentpoints(self):
        thelist = []

        if int(self.coords[0] / scale) - 1 >= 0 and int(self.coords[1] / scale) - 1 >= 0:
            point = arr[int(self.coords[0] / scale) - 1][int(self.coords[1] / scale) - 1].coords
            thelist.append(divcoordsbyscale(point))
        if int(self.coords[0] / scale) - 1 > 0:
            point = arr[int(self.coords[0] / scale) - 1][int(self.coords[1] / scale)].coords
            thelist.append(divcoordsbyscale(point))
        if int(self.coords[0] / scale) - 1 >= 0 and int(self.coords[1] / scale) + 1 < height:
            point = arr[int(self.coords[0] / scale) - 1][int(self.coords[1] / scale) + 1].coords
            thelist.append(divcoordsbyscale(point))
        if int(self.coords[1] / scale) - 1 >= 0:
            point = arr[int(self.coords[0] / scale)][int(self.coords[1] / scale) - 1].coords
            thelist.append(divcoordsbyscale(point))
        if int(self.coords[1] / scale) + 1 < height:
            point = arr[int(self.coords[0] / scale)][int(self.coords[1] / scale) + 1].coords
            thelist.append(divcoordsbyscale(point))
        if int(self.coords[0] / scale) + 1 < width and int(self.coords[1] / scale) + 1 < height:
            point = arr[int(self.coords[0] / scale) + 1][int(self.coords[1] / scale) + 1].coords
            thelist.append(divcoordsbyscale(point))
        if (int(self.coords[0] / scale) + 1) < width and int(self.coords[1] / scale) - 1 >= 0:
            point = arr[int(self.coords[0] / scale) + 1][int(self.coords[1] / scale) - 1].coords
            thelist.append(divcoordsbyscale(point))
        if int(self.coords[0] / scale) + 1 < width:
            point = arr[int(self.coords[0] / scale) + 1][int(self.coords[1] / scale)].coords
            thelist.append(divcoordsbyscale(point))
        return thelist

    def __init__(self):
        self.coords = (0, 0)
        self.CurrentBOT = None


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class BOT:
    CL = (0, 0)
    CLTile = Tile()
    frontierNodes = []

    def __init__(self, coords):
        self.CL = coords
        arr[int(coords[0] / scale)][int(coords[1] / scale)].robotinator(self)
        self.CLTile = arr[int(coords[0] / scale)][int(coords[1] / scale)]

    def setlocation(self, coords):

        self.CL = coords

    def pathfinder(self, maze, end):
        start = divcoordsbyscale(self.CL)

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1),
                                 (1, 1)]:  # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


x, y = 0, 0
Frontiernodes = []
arr = [[Tile() for x in range(width)] for y in range(height)]

# define the array
for x in range(width):
    for y in range(height):
        xscaled = x * scale
        yscaled = y * scale
        arr[y][x].setcoords([xscaled, yscaled])



if enviornment is 1:
    pavelot((42, 42), 5)
    pavelot((8, 8), 5)
    obstacles=162

else:
    pavelot((24, 24), 10)
    obstacles=361



#print(obstacles)
# for a in range (24):
# arr[a][20].setobstaclefence()
# for a in range (21):
# if a is not 15 and a is not 16 and a is not 17:
# arr[24][a].setobstaclefence()


pygame.display.update()

# insert a bot


ROBOTS = []
ROBOT1 = BOT((random.randint(0,49) * scale, random.randint(0,49) * scale))
ROBOT2 = BOT((random.randint(0,49) * scale, random.randint(0,49) * scale))
ROBOT3 = BOT((random.randint(0,49) * scale, random.randint(0,49) * scale))
ROBOT4 = BOT((random.randint(0,49) * scale, random.randint(0,49) * scale))
ROBOT5 = BOT((random.randint(0,49) * scale, random.randint(0,49) * scale))
ROBOTOS = [ROBOT1, ROBOT2, ROBOT3, ROBOT4, ROBOT5]
for i in range(numbots):
    ROBOTS.append(ROBOTOS[i])

patharr = [[int for x in range(width)] for y in range(height)]

for x in range(width):
    for y in range(height):
        patharr[x][y] = arr[x][y].obstacle

# for w in ROBOT1.frontierNodes:
# print(w.coords)
skip = False
pygame.display.update()
while discoverednodes+obstacles < (width * height):

    for b in ROBOTS:

        assignutilityradius(divcoordsbyscale(b.CL), spacingdistance)
        if not Frontiernodes:
            skip = True

        if not skip:
            goalnode = Frontiernodes[0]

            for f in Frontiernodes:
                # if not f.visited:
                # pygame.draw.rect(screen, GREEN, (f.coords[0] + 1, f.coords[1] + 1, unit, unit))

                if calculatealgo(f, b) > calculatealgo(goalnode, b):
                    goalnode = f

            Frontiernodes.pop(Frontiernodes.index(goalnode))

            print("Lawn mower sounds")
            print(discoverednodes)
            route = b.pathfinder(patharr, divcoordsbyscale(goalnode.coords))


            for r in route:
                arr[r[0]][r[1]].derobotinator()

                b.setlocation(multcoordsbyscale(r))

                arr[r[0]][r[1]].robotinator(b)

            for x in range(width):
                for y in range(height):
                    arr[x][y].utilitycost = 1

    pygame.display.update()

print(discoverednodes, "grasses mowed")

# slow the searching?
# clock = pygame.time.Clock()
# clock.tick(60)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

# Works when set is used, make a setfrontier funct that is the same exact thing
# def setfrontier(self, frontierlist):
# for x in frontierlist:
# if (not self.visited and not self.Frontier):
# self.Frontier = True
# pygame.draw.rect(screen, FRONTIER, (self.coords[0] + 1, self.coords[1] + 1, unit, unit))
# pygame.display.update()
