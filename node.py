import pygame as pg
from button import Button


class Node(Button):
    def __init__(self, screen, x, y, width, height, colour):
        super().__init__(screen, x, y, width, height, colour)

        self.rect_button = pg.Rect(self.x, self.y, self.width, self.height)

        # Remove this blocked, start and end points as they can be called as functions for each node...
        self.blocked = False
        self.start_point = False
        self.end_point = False

        self.f = 0  # f --> Total cost of the node.
        self.g = 0  # g --> Distance between start node and the current node.
        self.h = 0  # h --> Heuristic distance from the current node to the end node.

    def button_draw(self):
        pg.draw.rect(self.screen, self.colour, self.rect_button)


