import sys
import pygame as pg
from button import Button

clock = pg.time.Clock()
FPS = 60

pg.init()
WIDTH, HEIGHT = 500, 500            # 1280, 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Pathfinding Simulator')

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)  # Add a new color constant for purple

letsgo_button = Button(screen, 200, 100, 200,
                       100, "Let's Go!!!", BLACK)


def main():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill(WHITE)
        draw()
        pg.display.update()

        clock.tick(FPS)


def draw():
    letsgo_button.button_draw()
    if letsgo_button.button_pressed() == True:
        print("Button is clicked...")
        letsgo_button.b_colour = (25, 255, 100)
        letsgo_button.button_draw()


if __name__ == '__main__':
    main()
