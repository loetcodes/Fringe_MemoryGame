"""

Fringe Memory Game - Pygame version

"""
#!/bin/python3

import pygame, random, sys
# from image_tile import ImageTile
# from pygame.locals import *

# Game constants
FPS = 30  # General speed of the program
WINDOW_WIDTH = 800  # width of the overall window
WINDOW_HEIGHT = 600  # Height of the overall window

BOARD_WIDTH = 4  # No of columns of images
BOARD_HEIGHT = 4  # No of rows of images

TILE_WIDTH = 100  # Width of the tile
TILE_HEIGHT = 125  # Height of the tile

LEFT_PANEL = 250
GAP_SIZE = 20  # Gap between each of the tiles width/height wise
BORDER_GAP_X = (WINDOW_WIDTH - LEFT_PANEL - (BOARD_WIDTH * TILE_WIDTH) - (BOARD_WIDTH - 1) * GAP_SIZE) / 2
BORDER_GAP_Y = (WINDOW_HEIGHT - (BOARD_HEIGHT * TILE_HEIGHT) - (BOARD_HEIGHT - 1) * GAP_SIZE) / 2

BG_COLOR = (0, 255, 0)  # Green
TILE_FRONT_COL = (255, 255, 0)  # Yellow

# Load image paths and pass them to the variables
img_1 = 'images/Fringe_apple.jpg'
img_2 = 'images/Fringe_butterfly.jpg'
img_3 = 'images/Fringe_frog.jpg'
img_4 = 'images/Fringe_hand.jpg'
img_5 = 'images/Fringe_leaf.jpg'
img_6 = 'images/Fringe_seahorse.jpg'
img_7 = 'images/Fringe_skull.jpg'
img_8 = 'images/Fringe_flower.jpg'
img_lst = [img_1,img_2, img_3, img_4, img_5, img_6, img_7, img_8]

# Game global variables
score = 0
trial_turns = 0
exposed = []
flipped_tiles = []
card_centres = []
turns = 0


def main():
    global screen, fps_clock

    pygame.init()

    fps_clock = pygame.time.Clock()
    text = " Fringe Memory Game"
    pygame.display.set_caption(text)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(BG_COLOR)

    background = pygame.Surface(screen.get_size())
    background.fill(BG_COLOR)

    x_mouse_pos = 0
    y_mouse_pos = 0

    game_board = createRandomBoard()
    revealed_sects = initializeExposed(False)
    print(revealed_sects)

    exposeStartGameboard(game_board)

    mainloop = True
    playtime = 0

    while mainloop:
        # Do not go faster than this frame rate.
        milliseconds = fps_clock.tick(FPS)
        playtime += milliseconds / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False

                    # Print framerate and playtime in titlebar.
        text = " Fringe Memory Game FPS: {0:.2f}   Playtime: {1:.2f}".format(fps_clock.get_fps(), playtime)
        pygame.display.set_caption(text)

        draw(game_board)

        # Update pygame display.
        pygame.display.flip()


def exposeStartGameboard(board):
    """ Exposes the start game board by showing all the images then covering them.
    Randomly exposes certain number of tiles for a fragment of time before covering them again.
    """
    game_tiles = initializeExposed(False)
    tiles = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            tiles.append((x,y))
    random.shuffle(tiles)
    print (tiles)

    # Expose certain number of tiles then set them back to False


def createRandomBoard():
    """ Creates a random board of image tiles.
    """
    all_images = img_lst * 2
    random.shuffle(all_images)

    # Create the board structure with all the images
    game_board = [] # Initialize the empty board
    for y in range(BOARD_HEIGHT):
        row = []
        # Assign and remove items as they are assigned to prevent duplication
        for x in range(BOARD_WIDTH):
            row.append(all_images[0])
            del all_images[0]
        game_board.append(row)
    return game_board


def initializeExposed(val):
    """ Sets the state of the board cards as exposed or unexposed.
    False: the images are covered
    True: the images are uncovered
    returns: a board initialized to the same state.
    """
    exposed = []
    for y in range(BOARD_HEIGHT):
        exposed.append([val] * BOARD_WIDTH)
    return exposed


def draw(board):
    """ Draws the board in its state
    For now draw the board with all the images loaded
    """

    for dummy_row in range(BOARD_HEIGHT):
        for dummy_col in range(BOARD_WIDTH):
            img_top_x = (LEFT_PANEL + BORDER_GAP_X + dummy_col * (TILE_WIDTH + GAP_SIZE))
            img_top_y = (BORDER_GAP_Y + dummy_row * (TILE_HEIGHT + GAP_SIZE))
            img_display = pygame.image.load(board[dummy_row][dummy_col]).convert()
            img_display = pygame.transform.scale(img_display, (TILE_WIDTH, TILE_HEIGHT))
            screen.blit(img_display, (img_top_x, img_top_y))
    pygame.display.update()


def game_state():
    """ Monitors the game state of the tiles and determines if matched tiles have been drawn or not
    """
    pass


def new_game():
    """ Starts a new game with all variables changed and game state reset
    """
    pass


if __name__ == '__main__':
    main()