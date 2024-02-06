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

    def button_draw(self):
        font = pg.font.Font(None, 40)
        text = font.render(self.text, True, (200, 30, 28))
        text_rect = text.get_rect(center=self.rect_button.center)  # Center the text
        pg.draw.rect(self.screen, self.colour, self.rect_button)
        self.screen.blit(text, text_rect)  # Draw the text onto the button
