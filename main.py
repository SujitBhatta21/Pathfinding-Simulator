import sys
import pygame as pg
from button import Button
from node import Node

clock = pg.time.Clock()
FPS = 60

# initialisation of pygame and screen setup.
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
default_end_colour = (255,165,0)        # Orange
default_start_colour = (64, 224, 208)   # Turquoise
default_block_colour = BLACK

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
                    default_end_colour, "END")
block_button = Button(screen, WIDTH/10, HEIGHT - (2.3/4)*HEIGHT, 200, 100,
                      BLACK, "BLOCK")
start_the_simulator = Button(screen, (WIDTH/2.5), HEIGHT - (1/4)*HEIGHT, 400, 100,
                             GOLDEN, "Start the Simulator")

# Stores all the grid boxes objects.
node = []
grid_drawn = False


def main():
    # setting game states.
    intro = 0
    user_pick = 1
    play = 2
    end = 3
    game_state = intro

    grant_access = False
    valid_input = False
    global grid_drawn

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
                    grid_drawn = False
                    game_state = user_pick

                # Start button:
                if start_button.button_hover() and game_state == play:
                    start_button.colour = GREY
                    start_pressed = True
                    end_pressed = False
                    end_button.colour = default_end_colour
                    block_pressed = False
                    block_button.colour = default_block_colour

                # End button:
                if end_button.button_hover() and game_state == play:
                    end_button.colour = GREY
                    end_pressed = True
                    start_button.colour = default_start_colour
                    block_button.colour = default_block_colour
                    start_pressed = False
                    block_pressed = False

                # Block button:
                if block_button.button_hover() and game_state == play:
                    block_button.colour = GREY
                    block_pressed = True
                    start_button.colour = default_start_colour
                    start_pressed = False
                    end_pressed = False
                    end_button.colour = default_end_colour

                # Checking if a node is clicked.
                for box in node:
                    if box.button_hover():
                        if start_pressed:
                            box.start_point = True
                            box.blocked = False
                            box.end_point = False
                            start_button.colour = default_start_colour
                            # Making sure that start button is set to false if a box is clicked.
                            start_pressed = False

                        elif block_pressed:
                            box.blocked = True
                            box.start_point = False
                            box.end_point = False
                            block_button.colour = default_block_colour
                            # Remodel this code as block_pressed should do something different not like start and end.
                            block_pressed = False

                        elif end_pressed:
                            box.end_point = True
                            box.start_point = False
                            box.blocked = False
                            end_button.colour = default_end_colour
                            end_pressed = False

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
            play_draw(start_pressed, end_pressed, block_pressed)

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
    pathfinding_text = display_text(WIDTH / 2, HEIGHT / 2 - 200, 100, "A* Pathfinding Simulator", GOLDEN)
    screen.blit(pathfinding_text[0], pathfinding_text[1])


def user_pick_draw():
    screen.fill(WHITE)
    input_field.button_draw()
    enter_button.hover_change_colour(GREY, GREEN)
    enter_button.button_draw()


def making_grid(grid_drawn):
    # Drawing the grids.
    x_coordinate = WIDTH / 2.5
    y_coordinate = HEIGHT / 10
    # Below variable is needed to reset y-coordinate value.
    temp_y = y_coordinate
    grid_size = 350

    if not grid_drawn:
        num = int(input_field.text)
        box_size = grid_size / num

        # Drawing the black rectangle below the grid.
        extra_size = box_size / 4
        rect_x = WIDTH / 2.5 - extra_size
        rect_y = HEIGHT / 10 - extra_size
        rect_width = (box_size * num + box_size / 4 * (num - 1)) + 2*extra_size
        rect_height = rect_width  # Making the rectangle a square.
        pg.draw.rect(screen, BLACK, pg.Rect(rect_x, rect_y, rect_width, rect_height))

        for i in range(num):
            for j in range(num):
                sq_box = Node(screen, x_coordinate, y_coordinate, box_size, box_size, WHITE)
                node.append(sq_box)

                y_coordinate += box_size + box_size / 4

            x_coordinate += box_size + box_size / 4
            y_coordinate = temp_y


def play_draw(start_pressed, end_pressed, block_pressed):
    # Fix this back_button_play is created every iteration...
    back_button_play.hover_change_colour(GREY, GOLDEN)
    back_button_play.button_draw()
    start_the_simulator.hover_change_colour(GREY, GOLDEN)
    start_the_simulator.button_draw()

    if not start_pressed:
        start_button.hover_change_colour(GREY, default_start_colour)
        start_button.button_draw()

    if not block_pressed:
        block_button.hover_change_colour(GREY, default_block_colour)
        block_button.button_draw()

    if not end_pressed:
        end_button.hover_change_colour(GREY, default_end_colour)
        end_button.button_draw()

    # Making the grid
    global grid_drawn
    making_grid(grid_drawn)
    grid_drawn = True

    # This code is repeated. Make adjustments before making this repo public.
    for box in node:
        if box.start_point:
            box.colour = default_start_colour
        elif box.end_point:
            box.colour = default_end_colour
        elif box.blocked:
            box.colour = default_block_colour
        else:
            box.colour = WHITE

        box.button_draw()

    print(node[0].start_point)


# This should display a pop-up telling what error the user has done...
def apology(text=""):
    pass


if __name__ == '__main__':
    main()
