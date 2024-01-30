import sys
import pygame as pg
from button import Button
from grid import Grid

clock = pg.time.Clock()
FPS = 60

pg.init()
WIDTH, HEIGHT = 1280, 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('A* Pathfinding Simulator')

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GOLDEN = (255, 215, 0)

# Button objects
lets_go_button = Button(screen, WIDTH/2 - 0.5 * 200, HEIGHT/2 - 0.5 * 100, 200, 100,
                        YELLOW, "Let's Go!!!")
input_field = Button(screen, WIDTH/2 - 0.5 * 200, HEIGHT/2 - 0.5 * 100, 200, 100,
                     YELLOW, "")
enter_button = Button(screen, WIDTH/2 - 0.5 * 200, HEIGHT/2 - 0.5 * 100 + 100, 200, 100,
                      GREEN, "ENTER")
back_button_play = Button(screen, WIDTH/10, HEIGHT - HEIGHT/4, 200, 100,
                          BLACK, "BACK")

grid = []

def main():
    # setting game states.
    intro = 0
    user_pick = 1
    play = 2
    end = 3
    game_state = intro

    grant_access = False
    valid_input = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Took me long time to figure out, but it's UP not DOWN.
            if event.type == pg.MOUSEBUTTONUP:
                # Change game state to user_pick after Let's Go is clicked.
                if lets_go_button.button_hover():
                    lets_go_button.colour = (25, 255, 100)
                    game_state = user_pick

                # Condition to allow user to enter keys in input field only
                # if the user clicks inside the input field button first.
                if input_field.button_hover():
                    grant_access = True
                if not input_field.button_hover():
                    grant_access = False

                # Change game state to play if enter button clicked with valid input.
                if enter_button.button_hover() and valid_input == True:
                    game_state = play

                # Go back to user_pick game stage from play state.
                if back_button_play.button_hover():
                    game_state = user_pick

            # Key pressed event displayed inside input_field button. Only integers are allowed to enter.
            if event.type == pg.KEYDOWN and grant_access == True:
                # Backspace feature to remove the latest last no. entered.
                if event.key == pg.K_BACKSPACE:
                    input_field.text = input_field.text[:-1]
                elif event.unicode.isdigit():

                    # Allow numbers with length less than or equal to 2
                    if len(input_field.text) < 2:
                        valid_input = True
                        input_field.text += event.unicode

                    else:
                        valid_input = False

        screen.fill(WHITE)

        # Displays intro screen.
        if game_state == intro:
            pathfinding_text = display_text(WIDTH/2, HEIGHT/2 - 200, 100, "A* Pathfinding Simulator", GOLDEN)
            screen.blit(pathfinding_text[0], pathfinding_text[1])
            intro_draw()

        # Displays input_field screen.
        elif game_state == user_pick:
            user_pick_draw()

        # Displays grids screen.
        elif game_state == play:
            play_draw()

        # Displays endgame screen.
        elif game_state == end:
            pass

        # Lines below refreshes screen FPS=60 frames per second.
        pg.display.update()
        clock.tick(FPS)


# Function that displays text msg. in screen on specific coordinate.
def display_text(x, y, size, text, colour):
    font = pg.font.Font(None, size)
    text = font.render(text, True, colour)
    text_rect = text.get_rect()
    # set the center of the rectangular object.
    text_rect.center = (x, y)
    return text, text_rect                         # See game_state == intro to see its use-case.


def intro_draw():
    if lets_go_button.button_hover():
        lets_go_button.colour = BLACK
    else:
        lets_go_button.colour = YELLOW

    lets_go_button.button_draw()


def user_pick_draw():
    screen.fill(WHITE)
    input_field.button_draw()
    enter_button.button_draw()


def play_draw():
    screen.fill(WHITE)
    back_button_play.button_draw()

    # Drawing the grids.
    grid_drawn = False
    x_coordinate = WIDTH / 3
    y_coordinate = HEIGHT / 10
    # Below variable is needed to reset y-coordinate value.
    temp_y = y_coordinate
    grid_size = 350

    if not grid_drawn:
        N = int(input_field.text)
        box_size = grid_size / N
        for i in range(N):
            for j in range(N):
                sq_box = Grid(screen, x_coordinate, y_coordinate, box_size, box_size, RED)
                sq_box.button_draw()    # button_draw() overrides button class method.
                grid.append(sq_box)
                y_coordinate += box_size + box_size / 4

            x_coordinate += box_size + box_size / 4
            y_coordinate = temp_y
        grid_drawn = True

    # This part is not working properly...??? Figure out...
    for box in grid:
        if box.button_hover():
            box.colour = GREY
        else:
            box.colour = YELLOW


if __name__ == '__main__':
    main()
