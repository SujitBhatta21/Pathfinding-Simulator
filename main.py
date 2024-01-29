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
YELLOW = (255, 255, 0)  # Add a new color constant for purple

letsgo_button = Button(screen, WIDTH/2, HEIGHT/2, 200,100, YELLOW,"Let's Go!!!")


def main():
    # bools
    intro = 0
    play = 1
    end = 2
    game_state = intro

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Took me long time to figure out, but it's UP not DOWN.
            if event.type == pg.MOUSEBUTTONUP:
                if letsgo_button.button_pressed():
                    letsgo_button.colour = (25, 255, 100)
                    game_state = play

        screen.fill(WHITE)
        
        if game_state == intro:
            intro_draw()
        
        if game_state == play:
            play_draw()
        
        if game_state == end:
            pass
        
        pg.display.update()
        clock.tick(FPS)


def intro_draw():
    letsgo_button.button_draw()


def play_draw():
    screen.fill(YELLOW)


if __name__ == '__main__':
    main()
