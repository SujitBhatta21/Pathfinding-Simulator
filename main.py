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
default_end_colour = (255, 165, 0)        # Orange
default_start_colour = (64, 224, 208)     # Turquoise
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
grid = []
grid_drawn = False
run_simulator = False


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
    global run_simulator

    start_pressed = False
    end_pressed = False
    block_pressed = False
    block_on = False
    mouse_button_pressed = False

    # Variables to track start and end nodes
    start_node = None
    end_node = None

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # Took me long time to figure out, but it's UP not DOWN.
            elif event.type == pg.MOUSEBUTTONUP:
                mouse_button_pressed = False

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
                if enter_button.button_hover() and valid_input and game_state == user_pick:
                    grid.clear()
                    screen.fill(WHITE)
                    game_state = play

                # Go back to user_pick game stage from play state.
                if back_button_play.button_hover() and game_state == play:
                    grid_drawn = False
                    game_state = user_pick
                    block_pressed = False

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
                    if not block_on:
                        block_button.colour = GREY
                        block_pressed = True
                        start_button.colour = default_start_colour
                        start_pressed = False
                        end_pressed = False
                        end_button.colour = default_end_colour
                        block_on = True
                    else:
                        block_pressed = False
                        block_button.colour = default_block_colour
                        block_on = False

                if start_the_simulator.button_hover() and game_state == play:
                    start_point_count = 0
                    end_point_count = 0
                    for row in grid:
                        for node in row:
                            if node.start_point:
                                start_point_count += 1
                            if node.end_point:
                                end_point_count += 1

                    if start_point_count == 1 and end_point_count == 1:

                        run_simulator = True
                    else:
                        run_simulator = False

                # Checking if a node is clicked.
                # Checking if a node is clicked.
                for row in grid:
                    for node in row:
                        if node.button_hover():
                            if start_pressed:
                                # Reset the previous start node
                                if start_node:
                                    start_node.start_point = False

                                node.start_point = True
                                node.blocked = False
                                node.end_point = False
                                start_button.colour = default_start_colour
                                # Making sure that start button is set to false if a box is clicked.
                                start_pressed = False
                                start_node = node

                            # this button is different from other button.
                            elif block_pressed and block_on:
                                node.blocked = True
                                node.start_point = False
                                node.end_point = False

                            elif end_pressed:
                                # Reset the previous end node
                                if end_node:
                                    end_node.end_point = False

                                node.end_point = True
                                node.start_point = False
                                node.blocked = False
                                end_button.colour = default_end_colour
                                end_pressed = False
                                end_node = node

            # Key pressed event displayed inside input_field button. Only integers are allowed to enter.
            elif event.type == pg.KEYDOWN and grant_access:
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

            # Mouse button down event
            elif event.type == pg.MOUSEBUTTONDOWN:
                if block_button.button_hover() and game_state == play:
                    mouse_button_pressed = True

            # Mouse motion event
            elif event.type == pg.MOUSEMOTION and mouse_button_pressed:
                for row in grid:
                    for node in row:
                        if node.button_hover():
                            node.blocked = True
                            node.start_point = False
                            node.end_point = False

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
    global grid  # Declaring grid as a global variable

    x_coordinate = WIDTH / 2.5
    y_coordinate = HEIGHT / 10
    grid_size = 350

    if not grid_drawn:
        num = int(input_field.text)
        box_size = grid_size / num

        pg.draw.rect(screen, BLACK, pg.Rect(WIDTH / 2.5 - box_size / 4, HEIGHT / 10 - box_size / 4,
                                            box_size * num + box_size / 4 * (num - 1) + 2 * box_size / 4,
                                            box_size * num + box_size / 4 * (num - 1) + 2 * box_size / 4))

        # Update the global grid variable
        grid = [[Node(screen, x_coordinate + i * (box_size + box_size / 4),
                      y_coordinate + j * (box_size + box_size / 4),
                      box_size, box_size, WHITE) for j in range(num)] for i in range(num)]

        for i in range(num):
            for j in range(num):
                node = grid[i][j]
                node.button_draw()

                # Add valid neighbors to the current node, including diagonals
                for ni in range(i - 1, i + 2):
                    for nj in range(j - 1, j + 2):
                        if 0 <= ni < num and 0 <= nj < num and (ni != i or nj != j):
                            node.neighbors.append(grid[ni][nj])

    # Continue with the rest of the function


def play_draw(start_pressed, end_pressed, block_pressed):
    global grid_drawn
    global run_simulator
    global grid

    making_grid(grid_drawn)

    grid_drawn = True
    start_node = None
    end_node = None

    for row in grid:
        for node in row:
            if node.start_point:
                node.colour = default_start_colour
                start_node = node
            elif node.end_point:
                node.colour = default_end_colour
                end_node = node
            elif node.blocked:
                node.colour = default_block_colour
            elif node.colour != BLUE:  # Skip updating the color for nodes in the path
                node.colour = WHITE

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

    if start_pressed:
        start_button.colour = GREY
        start_button.button_draw()

    # Draw the nodes first
    for row in grid:
        for node in row:
            node.button_draw()

    if run_simulator:

        path = a_star(start_node, end_node)

        # Update the display with the path
        for node in path:
            if node.colour != BLUE:  # Skip updating the color for nodes in the path
                node.colour = BLUE
                node.button_draw()

        run_simulator = False

    # Draw the buttons on top of the nodes
    for row in grid:
        for node in row:
            node.button_draw()


def a_star(start, end):
    # Reset colors of all nodes
    for row in grid:
        for node in row:
            node.colour = WHITE

    open_set = [start]
    closed_set = []

    while open_set:
        current = min(open_set, key=lambda node: node.f)

        if current == end:
            path = []
            path.append(current)
            while current.previous:
                path.append(current.previous)
                current = current.previous

            print("Path is: ", path)
            return path

        open_set.remove(current)
        closed_set.append(current)

        neighbors = current.neighbors

        for neighbor in neighbors:

            if neighbor in closed_set or neighbor.blocked:
                continue

            temp_g = current.g + 1

            if neighbor not in open_set or temp_g < neighbor.g:
                neighbor.g = temp_g
                neighbor.h = heuristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.previous = current

                if neighbor not in open_set:
                    open_set.append(neighbor)

    print("No path found")
    return []


def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


if __name__ == '__main__':
    main()
