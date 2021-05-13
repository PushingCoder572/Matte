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


def index_nodes(nodes):
    for y, row in enumerate(nodes):
        for x, node in enumerate(row):
            if node != 0:
                node.array_pos.x = x
                node.array_pos.y = y


def make_connections(start_node, nodes):
    adj_nodes = start_node.get_adj_nodes(nodes)

    print(len(adj_nodes), len(start_node.edge_connections))
    print(start_node.pos.x, start_node.pos.y)
    if len(adj_nodes) == len(start_node.edge_connections):
        return False

    for node in adj_nodes:
        connection_id = pow(start_node.array_pos.x + node.array_pos.x, start_node.array_pos.y + node.array_pos.y)
        if not node.check_edge_by_id(connection_id):
            start_node.connect_with_node(node, connection_id)
            if not make_connections(node, nodes):
                break


class Box:
    def __init__(self, shape, size=50):
        self.shape = shape
        self.size = size

    def create_nodes(self):
        list_of_nodes = []

        first_row = True
        y_offset = 50
        for row_index, row in enumerate(self.shape):
            node_row = []
            x_offset = 50
            if first_row:
                for index, cube in enumerate(row):
                    if cube == 1:
                        node_row.append(Node(x_offset, y_offset))
                        if row[index + 1] == 0:
                                node_row.append(Node(x_offset + self.size, y_offset))
                    else:
                        node_row.append(0)
                        node_row.append(0)

                    x_offset += self.size
                first_row = False
                list_of_nodes.append(node_row)
            
            node_row = []
            x_offset = 50
            for index, cube in enumerate(row):
                if cube == 1:
                    node_row.append(Node(x_offset, y_offset + self.size))
                    if row[index + 1] == 0:
                        node_row.append(Node(x_offset + self.size, y_offset + self.size))
                else:
                    node_row.append(0)
                    node_row.append(0)

                x_offset += self.size

            if first_row:
                first_row = False

            y_offset += self.size
            list_of_nodes.append(node_row)           

        return list_of_nodes

    def create_edges(self, nodes):
        list_of_edges = []

        start_node = 0
        break_all = False
        for row in nodes:
            for node in row:
                if node != 0:
                    start_node = node
                    break_all = True
                    break

            if break_all:
                break
        
        make_connections(start_node, nodes)

        for row in nodes:
            for node in row:
                if node != 0:
                    for edge in node.edge_connections:
                        list_of_edges.append(edge)
                        

        return list_of_edges


class Node:
    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.array_pos = Vector2(0, 0)
        self.edge_connections = []

    def draw(self, window):
        pygame.draw.circle(window, GREEN, (int(self.pos.x), int(self.pos.y)), NODE_RADIUS)

    def get_adj_nodes(self, nodes):
        adj_const = [
            (1, -1),
            (1, 0),
            (1, 1),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 0),
            (-1, 1)
        ]

        adj_nodes = []

        for x, y in adj_const:
            try:
                value_y = int(self.array_pos.y + y)
                value_x = int(self.array_pos.x + x)
                test_node = nodes[value_y][value_x]
                if test_node != 0:
                    if value_y > -1 and value_x > -1:
                        adj_nodes.append(test_node)
            except:
                pass
        
        return adj_nodes

    def get_edge_by_id(self, id):
        for edge in self.edge_connections:
            if edge.id == id:
                return edge
        
        return -1

    def connect_with_node(self, node, id):
        self.edge_connections.append(Edge(self, node, id))

    def check_edge_by_id(self, id):
        for edge in self.edge_connections:
            if edge.id == id:
                return True
        
        return False


class Edge:
    def __init__(self, node1, node2, e_id):
        self.nodes = [node1, node2]
        self.ideal_length = self.get_length()
        self.id = e_id

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
        index_nodes(self.nodes)
        self.edges = box.create_edges(self.nodes)

    def run(self):
        for i in self.edges:
            i.draw(self.window)

        for i in self.nodes:
            for j in i:
                if j != 0:
                    j.draw(self.window)
                
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