import pygame as pg
from button import Button


class Grid(Button):
    def __init__(self, screen, x, y, width, height, colour):
        super().__init__(screen, x, y, width, height, colour)

        self.rect_button = pg.Rect(self.x, self.y, self.width, self.height)
        self.blocked = False
        self.start_point = False
        self.end_point = False

    def button_draw(self):
        pg.draw.rect(self.screen, self.colour, self.rect_button)
