import pygame as pg


class Button:
    def __init__(self, screen, x, y, width, height, colour, text=''):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.colour = colour
        self.rect_button = pg.Rect(self.x, self.y, self.width, self.height)

    def button_pressed(self):
        # This function returns true if button is pressed...
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect_button.collidepoint(mouse_pos):
                    print("Button is clicked...")
                    print(mouse_pos)
                    return True
                else:
                    return False

    def button_hover(self):
        mouse_pos = pg.mouse.get_pos()
        if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width:
            if mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
                return True
        return False

    def setColour(self, colour):
        self.colour = colour

    def button_draw(self):
        font = pg.font.Font(None, 70)
        pg.draw.rect(self.screen, self.colour, self.rect_button)

       # if (self.x <= mouse_pos[0] <= self.x + self.width) and (
        #        self.y <= mouse_pos[1] <= self.y + self.height):