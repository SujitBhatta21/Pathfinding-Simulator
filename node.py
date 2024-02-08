import pygame as pg
from button import Button


class Node:
    def __init__(self, screen, x, y, width, height, colour):

        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

        self.rect_button = pg.Rect(self.x, self.y, self.width, self.height)

        # Remove this blocked, start and end points as they can be called as functions for each node...
        self.blocked = False
        self.start_point = False
        self.end_point = False

        self.g = 0             # g --> Distance between start node and the current node.
        self.h = 0             # h --> Heuristic distance from the current node to the end node.
        self.f = 0
        self.parent = None     # Reference to the previous node in the optimal path
        self.previous = None
        self.neighbors = []    # List to store neighboring nodes

    def button_draw(self):
        pg.draw.rect(self.screen, self.colour, self.rect_button)

    def button_hover(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect_button.collidepoint(mouse_pos):
            return True
        else:
            return False

    def hover_change_colour(self, hover_colour, default_colour):
        if self.button_hover():
            self.colour = hover_colour
        else:
            self.colour = default_colour

    def f_cost(self):
        return self.g_cost + self.h_cost

    def reset_node_attributes(self):
        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')
        self.previous = None