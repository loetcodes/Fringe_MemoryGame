"""

Fringe Memory Game

"""
#!/bin/python3

import pygame, random, sys
# from image_tile import ImageTile
# from pygame.locals import *

# Original window width was 800 X 600

# Game constants
FPS = 30  # General speed of the program
WINDOW_WIDTH = 1000  # width of the overall window
WINDOW_HEIGHT = 800  # Height of the overall window

BOARD_WIDTH = 4  # No of columns of images
BOARD_HEIGHT = 4  # No of rows of images

TILE_WIDTH = 100  # Width of the tile
TILE_HEIGHT = 125  # Height of the tile
UNCOVER_SPEED = 10

LEFT_PANEL = 250
GAP_SIZE = 20  # Gap between each of the tiles width/height wise
BORDER_GAP_X = (WINDOW_WIDTH - LEFT_PANEL - (BOARD_WIDTH * TILE_WIDTH) - (BOARD_WIDTH - 1) * GAP_SIZE) / 2
BORDER_GAP_Y = (WINDOW_HEIGHT - (BOARD_HEIGHT * TILE_HEIGHT) - (BOARD_HEIGHT - 1) * GAP_SIZE) / 2

COL_0 = (0, 0, 0) # black
COL_1 = (0, 255, 0) # green
COL_2 = (81, 74, 0) # yellow
COL_3 = (0, 0, 255) # red
COL_4 = (255, 255, 255) # white
COL_5 = (9, 13, 20) # dark blue
COL_6 = (8, 11, 17) # dark blue
COL_7 = (33, 8, 38) # purple-ish
COL_8 = (0, 8, 38) # dark blue-ish
COL_9 = (54, 109, 108) # teal
COL_10 = (178, 178, 178)  # grey-ish
COL_11 = (96, 96, 96) # dark grey-ish
COL_12 = (34, 34, 34) # Dark grey-ish from fringe image


BG_COLOR = COL_0 # was COL_ before

TILE_FRONT_COL = COL_9
PANEL_COL = COL_10 # was col 10 before


# Load image paths and pass them to the variables
side_logo = 'images/Fringe-logo-430x247.png'
new_game_btn = "images/new_game_white.png"
img_1 = 'images/Fringe_apple.jpg'
img_2 = 'images/Fringe_butterfly.jpg'
img_3 = 'images/Fringe_frog.jpg'
img_4 = 'images/Fringe_hand.jpg'
img_5 = 'images/Fringe_leaf.jpg'
img_6 = 'images/Fringe_seahorse.jpg'
img_7 = 'images/Fringe_skull.jpg'
img_8 = 'images/Fringe_flower.jpg'
img_lst = [img_1,img_2, img_3, img_4, img_5, img_6, img_7, img_8]

# Texts to be displayed on screen
left_txt1 = 'Memory game based on the hit'
left_txt2 = 'sci-fi series Fringe.'
left_txt3 = 'Using the shows "not-so-hidden"'
left_txt4 = 'glyphs, match the images to'
left_txt5 = 'uncover the tiles...'
left_txt6 = ''
left_panel_texts = [left_txt1, left_txt2, left_txt3, left_txt4, left_txt5]

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

    # Draw the control panel
    drawControlPanel(PANEL_COL, LEFT_PANEL, WINDOW_HEIGHT)

    x_mouse_pos = 0
    y_mouse_pos = 0
    choice_one = None

    # game_board = createRandomBoard()
    # revealed_sects = initializeExposed(False)
    # #print(revealed_sects)
    #
    # exposeStartGameboard(game_board)

    game_board, revealed_sects = newGame()

    #Insert text to show the user can now begin the game choosing boxes

    mainloop = True
    playtime = 0

    while mainloop:
        # Do not go faster than this frame rate.
        milliseconds = fps_clock.tick(FPS)
        playtime += milliseconds / 1000.0
        mouseClicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                mainloop = False
            elif event.type == pygame.MOUSEMOTION:
                x_mouse_pos, y_mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                x_mouse_pos, y_mouse_pos = event.pos
                mouseClicked = True
                print("Mouse clicked at:", x_mouse_pos, y_mouse_pos)


        # Print frame rate and playtime in title bar.
        text = " Fringe Memory Game FPS: {0:.2f}   Playtime: {1:.2f}".format(fps_clock.get_fps(), playtime)
        pygame.display.set_caption(text)

        #drawControlPanel()
        drawBoard(game_board, revealed_sects)

        tile_pos = getTileAtPos(x_mouse_pos, y_mouse_pos)
        if tile_pos[0] is not None and tile_pos[1] is not None:
            if not revealed_sects[tile_pos[0]][tile_pos[1]] and mouseClicked:
                reveal_card_slide(game_board, [tile_pos])
                revealed_sects[tile_pos[0]][tile_pos[1]] = True
                if choice_one == None and choice_one != tile_pos:
                    #checks that choice one is the first tile and also accounts for one re-clicking the same tile
                    choice_one = tile_pos
                    drawBoard(game_board, revealed_sects)
                else:
                    first_tile = game_board[choice_one[0]][choice_one[1]]
                    second_tile = game_board[tile_pos[0]][tile_pos[1]]
                    print("first tile is ", first_tile)
                    print("second tile is ", second_tile)

                    if first_tile != second_tile:
                        #Then images are not the same and therefore, cover them up
                        pygame.time.wait(800)
                        cover_card_slide(game_board, [choice_one, tile_pos])
                        revealed_sects[choice_one[0]][choice_one[1]] = False
                        revealed_sects[tile_pos[0]][tile_pos[1]] = False
                        #deduct a score at this point - 2 points
                        #add an else that adds a score point when the images are uncovered - 5 points
                    elif gameComplete(revealed_sects):
                        print("The game is complete!")
                        #print("Revealed sections are:", revealed_sects)


                        #revealed_sects = initializeExposed(False)
                        gameWon(game_board)
                        revealed_sects = initializeExposed(False)
                        drawBoard(game_board, revealed_sects, TILE_WIDTH, BG_COLOR)
                        pygame.time.wait(2000)

                        # Show you won text for a short time

                        pygame.time.wait(800)
                        # Reset the board for a new game
                        game_board, revealed_sects = newGame()

                    drawBoard(game_board, revealed_sects)
                    choice_one = None

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
    #print (tiles)

    drawBoard(board, game_tiles)

    # Create sections to be revealed from the random tiles
    box_groups = []
    for i in range(0, len(tiles), 4):
        sect = tiles[i: i + 4]
        box_groups.append(sect)

    for boxes in box_groups:
        reveal_card_slide(board, boxes)
        cover_card_slide(board, boxes)


def gameWon(board):
    # Expose certain number of tiles
    game_tiles = initializeExposed(True)
    tiles = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            tiles.append((x, y))
    #random.shuffle(tiles)
    #print(tiles)

    drawBoard(board, game_tiles, color=BG_COLOR)

    # Create sections to be revealed from the random tiles
    box_groups = []
    for i in range(0, len(tiles), 4):
        sect = tiles[i: i + 4]
        box_groups.append(sect)

    for boxes in box_groups:
        cover_card_slide(board, boxes, BG_COLOR)


def reveal_card_slide(board, cards):
    """
    Reveals the cards at a certain speed.
    :param board: the board that is passed on
    :param cards: the cards images to revealed
    """
    for width in range(TILE_WIDTH, (-UNCOVER_SPEED), -UNCOVER_SPEED):
        draw_board_covers(board, cards, width)


def cover_card_slide(board, cards, color=TILE_FRONT_COL):
    """
    Covers revealed cards at the same speed used to cover them.
    :param board: the board that is passed on
    :param cards: the cards images to revealed
    """
    for width in range(0, TILE_WIDTH + 1, UNCOVER_SPEED):
        draw_board_covers(board, cards, width, color)


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


def drawBoard(board, exposed,  width=TILE_WIDTH, color=TILE_FRONT_COL):
    """ Draws the board in its state based on the values in exposed grid.
    When values in exposed are false, the card cover is drawn, when true the image below is drawn.
    board: list of image locations
    exposed: boolean values for each of the image tiles
    """
    for dummy_row in range(BOARD_HEIGHT):
        for dummy_col in range(BOARD_WIDTH):
            card = (dummy_row, dummy_col)
            coord_pos = topCoords(card)
            if not exposed[dummy_row][dummy_col]:
                pygame.draw.rect(screen, color, (coord_pos[0], coord_pos[1], width , TILE_HEIGHT))
            else:
                draw_board_icons(board, dummy_row, dummy_col, coord_pos)
    pygame.display.update()


def draw_board_icons(board, row, col, coord_pos):
    """ Draws the images/icons that are to be revealed on the board.
    Precondition: This function is called when exposed is True
    """
    board_image = pygame.image.load(board[row][col]).convert()
    board_image = pygame.transform.scale(board_image, (TILE_WIDTH, TILE_HEIGHT))
    screen.blit(board_image, coord_pos)
    #return board_image


def draw_board_covers(board, cards, width=TILE_WIDTH, color=TILE_FRONT_COL):
    """ Draws the covers that hide the icons/images on the board
    Precondition: This function is called when exposed is False
    """
    for card in cards:
        coord_pos = topCoords(card)
        draw_board_icons(board, card[0], card[1], coord_pos)
        if width > 0:
            pygame.draw.rect(screen, color, (coord_pos[0], coord_pos[1], width, TILE_HEIGHT))
    pygame.display.update()
    fps_clock.tick(FPS)


def topCoords(card):
    """
    Obtains the top coordinates for the card covers
    :param card: card position tuple in the board
    :return: the top left x and y coordinates
    """
    top_x = (LEFT_PANEL + BORDER_GAP_X + card[0] * (TILE_WIDTH + GAP_SIZE))
    top_y = (BORDER_GAP_Y + card[1] * (TILE_HEIGHT + GAP_SIZE))
    return (top_x, top_y)


def getTileAtPos(pos_x, pos_y):
    """
    Retrieves the tile located at the pos_x and pos_y coordinates passed into the function.
    :param pos_x: x coordinate
    :param pos_y: y coordinate
    :return: board pos in x and y that is located at that point or none if not hovered over a box
    """
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            top_x, top_y = topCoords((x, y))
            card_rect = pygame.Rect(top_x, top_y, TILE_WIDTH, TILE_HEIGHT)
            if card_rect.collidepoint(pos_x, pos_y):
                return (x, y)
    return (None, None)


def gameComplete(revealed_sect):
    """
    Plays a game animation to show the level/game is over
    :param board: passes in the board with True/False values for the entire game
    :return: True or False whether all the tiles have been revealed or not
    """
    for item in revealed_sect:
        if False in item:
            return False
    return True


def drawControlPanel(color, width, height):
    """ Draws the side control panel for the game
    """
    #pygame.draw.rect(screen, color, (0, 0, width, height))
    top_logo = pygame.image.load(side_logo).convert()
    top_logo = pygame.transform.scale(top_logo, (width, 150))
    new_game_logo = pygame.image.load(new_game_btn).convert()
    new_game_logo = pygame.transform.scale(new_game_logo, (width - 50 , 65))
    top_logo_x = 0
    top_logo_y = 0
    new_logo_x = 20
    new_logo_y = WINDOW_HEIGHT - 200
    screen.blit(top_logo, (top_logo_x, top_logo_y))
    screen.blit(new_game_logo, (new_logo_x, new_logo_y))

    # left panel text
    font = pygame.font.Font("freesansbold.ttf", 16)
    text_x = font.render(LEFT_TXT_1, True, COL_4, COL_0)
    textRect = text_x.get_rect()
    textRect.center = (LEFT_PANEL - 25, 200)
    screen.blit(text_x, textRect)



def newGame():
    """ Starts a new game with all variables changed and game state reset
    """
    board = createRandomBoard()
    revealed_sects = initializeExposed(False)
    exposeStartGameboard(board)
    return board, revealed_sects


if __name__ == '__main__':
    main()