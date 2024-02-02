import sys
import pygame as pg
from button import Button
from node import Node

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
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLDEN = (255, 215, 0)

# Button objects
# --- For intro screen.
lets_go_button = Button(screen, WIDTH/2 - 0.5 * 200, HEIGHT/2 - 0.5 * 100, 200, 100,
                        YELLOW, "Let's Go!!!")
# --- For user_input screen.
input_field = Button(screen, WIDTH/2 - 0.5 * 200, HEIGHT/2 - 0.5 * 100, 200, 100,
                     YELLOW, "")
enter_button = Button(screen, WIDTH/2 - 0.5 * 200, HEIGHT/2 - 0.5 * 100 + 100, 200, 100,
                      GREEN, "ENTER")
# --- For play screen.
back_button_play = Button(screen, WIDTH/10, HEIGHT - HEIGHT/4, 200, 100,
                          GOLDEN, "BACK")
start_button = Button(screen, WIDTH/10, HEIGHT - (3.7/4)*HEIGHT, 200, 100,
                      GREEN, "START")
end_button = Button(screen, WIDTH/10, HEIGHT - (3/4)*HEIGHT, 200, 100,
                    RED, "END")
block_button = Button(screen, WIDTH/10, HEIGHT - (2.3/4)*HEIGHT, 200, 100,
                      BLACK, "BLOCK")
start_the_simulator = Button(screen, WIDTH/2.5, HEIGHT - (1/4)*HEIGHT, 300, 100,
                             GOLDEN, "Start the Simulator")

# Stores all the grid boxes objects.
node = []
node_drawn = False


def main(node_drawn):
    # setting game states.
    intro = 0
    user_pick = 1
    play = 2
    end = 3
    game_state = intro

    grant_access = False
    valid_input = False

    start_pressed = False
    end_pressed = False
    block_pressed = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Took me long time to figure out, but it's UP not DOWN.
            if event.type == pg.MOUSEBUTTONUP:
                # Change game state to user_pick after Let's Go is clicked.
                if lets_go_button.button_hover() and game_state == intro:
                    screen.fill(WHITE)
                    game_state = user_pick

                # Condition to allow user to enter keys in input field only
                # if the user clicks inside the input field button first.
                if input_field.button_hover() and game_state == user_pick:
                    grant_access = True
                if not input_field.button_hover():
                    grant_access = False

                # Change game state to play if enter button clicked with valid input.
                if enter_button.button_hover() and valid_input == True and game_state == user_pick:
                    node.clear()
                    screen.fill(WHITE)
                    game_state = play

                # Go back to user_pick game stage from play state.
                if back_button_play.button_hover() and game_state == play:
                    node_drawn = False
                    game_state = user_pick

                # Start button:
                if start_button.button_hover() and game_state == play:
                    start_button.colour = GREY
                    start_pressed = True
                    print("Start PRESSED: ", start_pressed)

                # End button:
                if end_button.button_hover() and game_state == play:
                    end_button.colour = RED
                    end_pressed = True
                    print("END PRESSED: ", end_pressed)

                # Block button:
                if block_button.button_hover() and game_state == play:
                    block_button.colour = GREY
                    block_pressed = True
                    print("BLOCK PRESSED: ", block_pressed)

                # Checking if a node is clicked.
                for box in node:
                    if box.button_hover():
                        if start_pressed and not box.blocked and not box.end_point:
                            box.colour = GREEN
                            box.start_point = True
                            start_button.colour = GREEN
                            # Making sure that start button is set to false if a box is clicked.
                            start_pressed = False

                        elif block_pressed and not box.start_point and not box.end_point:
                            box.colour = BLACK
                            box.blocked = True
                            block_pressed = False

                        elif end_pressed and not box.blocked and not box.start_point:
                            box.colour = RED
                            box.end_point = True
                            end_pressed = False
                    else:
                        box.colour = RED
                    box.button_draw()

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

        # Displays intro screen.
        if game_state == intro:
            intro_draw()

        # Displays input_field screen.
        elif game_state == user_pick:
            user_pick_draw()

        # Displays grid in the screen.
        elif game_state == play:
            play_draw(node_drawn, start_pressed, end_pressed, block_pressed)

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
    screen.fill(WHITE)
    lets_go_button.hover_change_colour(GREY, YELLOW)
    lets_go_button.button_draw()
    pathfinding_text = display_text(WIDTH / 2, HEIGHT / 2 - 200, 100, "Grid Simulator", GOLDEN)
    screen.blit(pathfinding_text[0], pathfinding_text[1])


def user_pick_draw():
    screen.fill(WHITE)
    input_field.button_draw()
    enter_button.hover_change_colour(GREY, GREEN)
    enter_button.button_draw()


def play_draw(node_drawn, start_pressed, end_pressed, block_pressed):
    # Fix this back_button_play is created every iteration...
    back_button_play.hover_change_colour(GREY, GOLDEN)
    back_button_play.button_draw()
    start_the_simulator.button_draw()

    if not start_pressed:
        start_button.hover_change_colour(GREY, GREEN)
        start_button.button_draw()

    if not block_pressed:
        block_button.hover_change_colour(GREY, BLACK)
        block_button.button_draw()

    if not end_pressed:
        end_button.hover_change_colour(GREY, RED)
        end_button.button_draw()

    # Drawing the grids.
    x_coordinate = WIDTH / 3
    y_coordinate = HEIGHT / 10
    # Below variable is needed to reset y-coordinate value.
    temp_y = y_coordinate
    grid_size = 350

    if not node_drawn:
        N = int(input_field.text)
        box_size = grid_size / N
        for i in range(N):
            for j in range(N):
                sq_box = Node(screen, x_coordinate, y_coordinate, box_size, box_size, RED)
                node.append(sq_box)
                sq_box.button_draw()    # button_draw() overrides button class method.

                y_coordinate += box_size + box_size / 4

            x_coordinate += box_size + box_size / 4
            y_coordinate = temp_y
        node_drawn = True

    # This code is repeated. Make adjustments before making this repo public.
    for box in node:
        if box.blocked:
            box.colour = BLACK
        elif box.start_point:
            box.colour = GREEN
        elif box.end_point:
            box.colour = RED
        else:
            box.colour = RED
        box.hover_change_colour(GREY, RED)
        box.button_draw()


# This should display a pop up telling what error the user has done...
def apology(text=""):
    pass


if __name__ == '__main__':
    main(node_drawn)
