"""

Fringe Memory Game

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
UNCOVER_SPEED = 9

LEFT_PANEL = 250
GAP_SIZE = 20  # Gap between each of the tiles width/height wise
BORDER_GAP_X = (WINDOW_WIDTH - LEFT_PANEL - (BOARD_WIDTH * TILE_WIDTH) - (BOARD_WIDTH - 1) * GAP_SIZE) / 2
BORDER_GAP_Y = (WINDOW_HEIGHT - (BOARD_HEIGHT * TILE_HEIGHT) - (BOARD_HEIGHT - 1) * GAP_SIZE) / 2

COL_0 = (0, 0, 0) # black
COL_1 = (0, 255, 0) # green
COL_2 = (255, 255, 0) # yellow
COL_3 = (0, 0, 255) # red
COL_4 = (255, 255, 255) # white

COL_5 = (9, 13, 20) # dark blue
COL_6 = (8, 11, 17) # dark blue
COL_7 = (33, 8, 38) # purple-ish
COL_8 = (0, 8, 38) # dark blue-ish
COL_9 = (54, 109, 108) # teal

BG_COLOR = COL_8
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
    #print(revealed_sects)

    exposeStartGameboard(game_board)

    #Insert text to show the user can now begin the game choosing boxes

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

        # Print frame rate and playtime in title bar.
        text = " Fringe Memory Game FPS: {0:.2f}   Playtime: {1:.2f}".format(fps_clock.get_fps(), playtime)
        pygame.display.set_caption(text)

        drawBoard(game_board, revealed_sects)

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

    # Expose certain number of tiles
    drawBoard(board, game_tiles)

    # Create sections to be revealed from the random tiles
    box_groups = []
    for i in range(0, len(tiles), 4):
        sect = tiles[i: i + 4]
        box_groups.append(sect)

    for boxes in box_groups:
        reveal_card_slide(board, boxes)
        cover_card_slide(board, boxes)


def reveal_card_slide(board, cards):
    for width in range(TILE_WIDTH, (-UNCOVER_SPEED) - 1, -UNCOVER_SPEED):
        draw_board_covers(board, cards, width)


def cover_card_slide(board, cards):
    for width in range(0, (TILE_WIDTH + UNCOVER_SPEED), UNCOVER_SPEED):
        draw_board_covers(board, cards, width)


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


def drawBoard(board, exposed):
    """ Draws the board in its state
    For now draw the board with all the images loaded
    board: list of image locations
    """
    for dummy_row in range(BOARD_HEIGHT):
        for dummy_col in range(BOARD_WIDTH):
            top_x = (LEFT_PANEL + BORDER_GAP_X + dummy_col * (TILE_WIDTH + GAP_SIZE))
            top_y = (BORDER_GAP_Y + dummy_row * (TILE_HEIGHT + GAP_SIZE))
            if not exposed[dummy_row][dummy_col]:
                pygame.draw.rect(screen, COL_9,(top_x, top_y, TILE_WIDTH, TILE_HEIGHT))
            else:
                draw_board_icons(board, dummy_row, dummy_col, top_x, top_y)
    pygame.display.update()


def draw_board_icons(board, row, col,top_x_coord, top_y_coord):
    """ Draws the images/icons that are to be revealed on the board.
    Precondition: This function is called when exposed is True
    """
    board_image = pygame.image.load(board[row][col]).convert()
    board_image = pygame.transform.scale(board_image, (TILE_WIDTH, TILE_HEIGHT))
    screen.blit(board_image, (top_x_coord, top_y_coord))
    #return board_image


def draw_board_covers(board, cards, width=TILE_WIDTH):
    """ Draws the covers that hide the icons/images on the board
    Precondition: This function is called when exposed is False
    """
    for card in cards:
        top_x = (LEFT_PANEL + BORDER_GAP_X + card[0] * (TILE_WIDTH + GAP_SIZE))
        top_y = (BORDER_GAP_Y + card[1] * (TILE_HEIGHT + GAP_SIZE))
        draw_board_icons(board, card[0], card[1], top_x, top_y)
        if width > 0:
            pygame.draw.rect(screen, COL_9,(top_x, top_y, width, TILE_HEIGHT))
    pygame.display.update()
    fps_clock.tick(FPS)


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