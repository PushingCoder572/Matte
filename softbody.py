import pygame
import math
import sys
from pygame.math import Vector2

pygame.init()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

LINE_WIDTH = 2
NODE_RADIUS = 4

SHAPE = [[0, 1, 1, 1, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 1, 0, 0]]


def remove_duplicates(lst):
    register = {}
    for item in lst:
        key = str(item.pos.x) + str(item.pos.y)
        if key not in register:
            register[key] = 1
        else:
            register[key] += 1

    print(register)


class QuadNode:
    def __init__(self, lst, index):
        self.node1 = lst[index[0]]
        self.node2 = lst[index[1]]
        self.node3 = lst[index[2]]
        self.node4 = lst[index[3]]


class Box:
    def __init__(self, shape, size=50):
        self.shape = shape
        self.size = size
        self.nodes = self.create_nodes()
        for i in self.nodes:
            print(i.pos.x, i.pos.y)
        self.edges = self.create_edges()

    def create_nodes(self):
        list_of_nodes = []

        y_offset = 50
        for line in self.shape:
            x_offset = 0
            for cube in line:
                if cube == 1:
                    for i in range(4):
                        if i == 0:
                            list_of_nodes.append(Node(x_offset, y_offset))
                        elif i == 1:
                            list_of_nodes.append(Node(x_offset + self.size, y_offset))
                        elif i == 2:
                            list_of_nodes.append(Node(x_offset, y_offset + self.size))
                        else:
                            list_of_nodes.append(Node(x_offset + self.size, y_offset + self.size))
                x_offset += self.size
            y_offset += self.size

        remove_duplicates(list_of_nodes)

        return list_of_nodes

    def create_edges(self):
        list_of_edges = []
        indices = [0, 1, 2, 3]
        while indices[3] < len(self.nodes):
            subject = QuadNode(self.nodes, indices)

            list_of_edges.append(Edge(subject.node1, subject.node2))
            list_of_edges.append(Edge(subject.node2, subject.node4))
            list_of_edges.append(Edge(subject.node3, subject.node4))

            indices[0] += 2
            indices[1] += 2
            indices[2] += 2
            indices[3] += 2

        return list_of_edges


class Node:
    def __init__(self, x, y):
        self.pos = Vector2(x, y)

    def draw(self, window):
        pygame.draw.circle(window, GREEN, (int(self.pos.x), int(self.pos.y)), NODE_RADIUS)


class Edge:
    def __init__(self, node1, node2):
        self.nodes = [node1, node2]
        self.ideal_length = self.get_length()

    def get_length(self):
        return math.sqrt(pow(self.nodes[1].pos.x - self.nodes[0].pos.x, 2) +
                         pow(self.nodes[1].pos.y - self.nodes[0].pos.y, 2))

    def draw(self, window):
        pygame.draw.line(window, BLUE, self.nodes[0].pos, self.nodes[1].pos)


class Game:
    def __init__(self, shape):
        self.window = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.shape = shape
        box = Box(self.shape)
        self.nodes = box.create_nodes()
        self.edges = box.create_edges()

    def run(self):
        for i in self.edges:
            i.draw(self.window)
        for i in self.nodes:
            i.draw(self.window)


game = Game(shape=SHAPE)
while 1:
    # Pygame event-system handling
    for event in pygame.event.get():
        # Checking for keyboard interaction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    game.run()

    # Refreshing the window
    pygame.display.flip()