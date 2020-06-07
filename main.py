import pygame
import sys
import time
import white_pawn
import black_pawn

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Lau kata kati')

background = pygame.image.load('assets/board.png').convert()
white = pygame.image.load('assets/white.png')
black = pygame.image.load('assets/black.png')

clock = pygame.time.Clock()

board = ['black', 'black', 'black',
         'black', 'black', 'black',
         'black', 'black', 'black',
         'X', None, 'X',
         'white', 'white', 'white',
         'white', 'white', 'white',
         'white', 'white', 'white']

board_copy = [None] * 21

# Flaga ruchu, 0 - ruch biały, 1 - ruch czarny
color = 0

black_pos = [[133, 100], [400, 100], [666, 100],
              [222, 200], [400, 200], [578, 200],
              [310, 300], [400, 300], [490, 300]]

white_pos = [[310, 500], [400, 500], [490, 500],
              [222, 600], [400, 600], [578, 600],
              [133, 700], [400, 700], [666, 700]]

# all_pos = [[110, 70], [368, 70], [630, 70],
#            [190, 170], [368, 170], [545, 170],
#            [279, 270], [368, 270], [457, 270],
#            [110, 670], [368, 670], [630, 670],
#            [190, 570], [368, 570], [545, 570],
#            [279, 470], [368, 470], [457, 470]]

fields_pos = [[133, 100], [400, 100], [666, 100],
              [222, 200], [400, 200], [578, 200],
              [310, 300], [400, 300], [490, 300],
              [320, 400], [400, 400], [480, 400],
              [310, 500], [400, 500], [490, 500],
              [222, 600], [400, 600], [578, 600],
              [133, 700], [400, 700], [666, 700]]

available_moves = [[1, 3], [0, 2, 4], [1, 5],
                   [0, 4, 6], [1, 3, 5, 7], [2, 4, 8],
                   [3, 7, 10], [4, 6, 8, 10], [5, 7, 10],
                   [None], [6, 7, 8, 12, 13, 14], [None],
                   [10, 13, 15], [10, 12, 14, 16], [10, 13, 17],
                   [12, 16, 18], [13, 15, 17, 19], [14, 16, 20],
                   [15, 19], [16, 18, 20], [17, 19]]

available_captures = [[2, 6], [7], [0, 8],
                      [5, 10], [10], [3, 10],
                      [0, 8, 14], [1, 13], [2, 6, 12],
                      [None], [3, 4, 5, 15, 16, 17], [None],
                      [8, 14, 18], [7, 19], [6, 12, 20],
                      [10, 17], [10], [10, 15],
                      [12, 20], [13], [14, 18]]

jumps = [[1, 3], [4], [1, 5],
         [4, 6], [7], [4, 8],
         [3, 7, 10], [4, 10], [5, 7, 10],
         [None], [6, 7, 8, 12, 13, 14], [None],
         [10, 13, 15], [10, 16], [10, 13, 17],
         [12, 16], [13], [14, 16],
         [15, 19], [16], [17, 19]]

black_pawns = []
white_pawns = []

clicked_white = []
clicked_black = []

done = False

def find_fields():
    for field in fields_pos:
        if (yMouse2 > (field[0] - 30)) and (yMouse2 < (field[0] + 30)) and (xMouse2 > (field[1] - 30)) and (
                xMouse2 < (field[1] + 30)):
            position = fields_pos.index(field)
            if color == 0:
                board[position] = 'white'
            else:
                board[position] = 'black'

    # x zamieniony z y
    for field2 in fields_pos:
        if (yMouse > (field2[1] - 30)) and (yMouse < (field2[1] + 30)) and (xMouse > (field2[0] - 30)) and (
                xMouse < (field2[0] + 30)):
            position2 = fields_pos.index(field2)
            board[position2] = None


def move():
    for i in range(len(board)):
        board_copy[i] = board[i]

    position2 = 0

    # x = pozycja wyjściowa w available_captures, np. dla pozycji wejściowej 0 może być 2 lub 6
    x = 0

    for field in fields_pos:
        if (yMouse2 > (field[1] - 10)) and (yMouse2 < (field[1] + 10)) and (xMouse2 > (field[0] - 10)) and (
                xMouse2 < (field[0] + 10)):
            position = fields_pos.index(field)

    # x zamieniony z y
    for field2 in fields_pos:
        if (yMouse > (field2[1] - 10)) and (yMouse < (field2[1] + 10)) and (xMouse > (field2[0] - 10)) and (
                xMouse < (field2[0] + 10)):
            position2 = fields_pos.index(field2)

    #gdzie
    #print(position)

    #skad
    #print(position2)

    #print(board_copy)
    #print()

    if position in available_moves[position2] and board_copy[position] == None:
        print('POPRAWNY RUCH')
        board_copy[position2] = None
        if color == 0:
            board_copy[position] = 'white'
            print(board_copy)
            print()
        else:
            board_copy[position] = 'black'
            print(board_copy)
            print()

    for inner in available_captures[position2]:
            if inner == position:
                x = available_captures[position2].index(inner)

    s = jumps[position2][x]
    print('S: ', s)

    if color == 0 and board_copy[s] == 'black' or color == 1 and board_copy[s] == 'white':
        print('POPRAWNE BICIE')
        board_copy[position2] = None
        board_copy[s] = None
        if color == 0:
            board_copy[position] = 'white'
            coordinatesX_black = fields_pos[s][0]
            coordinatesY_black = fields_pos[s][1]

            for pawn in black_pawns:
                if (pawn.x < coordinatesX_black + 8) and (pawn.x > coordinatesX_black - 8):
                    if (pawn.y < coordinatesY_black + 8) and (pawn.y > coordinatesY_black - 8):
                        pawn.x = 0
                        pawn.y = 0
                        pawn.rect.center = (0, 0)

        else:
            board_copy[position] = 'black'
            coordinatesX_white = fields_pos[s][0]
            coordinatesY_white = fields_pos[s][1]

            for pawn in white_pawns:
                if (pawn.x < coordinatesX_white + 8) and (pawn.x > coordinatesX_white - 8):
                    if (pawn.y < coordinatesY_white + 8) and (pawn.y > coordinatesY_white - 8):
                        pawn.x = 0
                        pawn.y = 0
                        pawn.rect.center = (0, 0)

    for i in range(len(board_copy)):
        board[i] = board_copy[i]

    for white in white_pawns:
        print(white.x, white.y)

    print()

    for black in black_pawns:
        print(black.x, black.y)


for pos in black_pos:
    pawn = black_pawn.BlackPawn(pos[0], pos[1])
    black_pawns.append(pawn)

for pos in white_pos:
    pawn = white_pawn.WhitePawn(pos[0], pos[1])
    white_pawns.append(pawn)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not done:
            done = True
            xMouse = event.pos[0]
            yMouse = event.pos[1]
            print(xMouse, yMouse)

            #clicked_white = [p for p in white_pawns if p.rect.collidepoint(xMouse, yMouse)]
            #clicked_black = [p for p in black_pawns if p.rect.collidepoint(xMouse, yMouse)]

            index = None

            for p in white_pawns:
                if p.rect.collidepoint(xMouse, yMouse):
                    clicked_white.append(p)
                    index = white_pawns.index(p)

            for p in black_pawns:
                if p.rect.collidepoint(xMouse, yMouse):
                    clicked_black.append(p)
                    index = black_pawns.index(p)

            if len(clicked_white) == 1:
                print('BIAŁY ZŁAPANY')
                clicked_pawn = clicked_white[0]
                color = 0

            elif len(clicked_black) == 1:
                print('CZARNY HEHE ZŁAPANY')
                clicked_pawn = clicked_black[0]
                color = 1

            # for pawn in white_pawns:
            #     print(pawn.x, pawn.y)
            #     if pawn.rect.collidepoint(xMouse, yMouse):
            #         pawn.x = xMouse
            #         pawn.y = yMouse
            #         pawn.rect.center = (pawn.x, pawn.y)

        elif event.type == pygame.MOUSEBUTTONDOWN and done:
            done = False
            xMouse2 = event.pos[0]
            yMouse2 = event.pos[1]
            #clicked_pawn.x = xMouse2
            #clicked_pawn.y = yMouse2

            if color == 0:
                white_pawns[index].x = xMouse2
                white_pawns[index].y = yMouse2
                white_pawns[index].rect.center = (xMouse2, yMouse2)

            elif color == 1:
                black_pawns[index].x = xMouse2
                black_pawns[index].y = yMouse2
                black_pawns[index].rect.center = (xMouse2, yMouse2)

            # clicked_pawn.rect.center = (clicked_pawn.x, clicked_pawn.y)
            move()

            clicked_white = []
            clicked_black = []

    screen.blit(background, (0, 0))

    # for pawn in black_pawns:
    #     screen.blit(pawn.image, (pawn.x-32.5, pawn.y-32.5))
    #
    # for pawn in white_pawns:
    #     screen.blit(pawn.image, (pawn.x-32.5, pawn.y-32.5))

    for x in range(len(board)):
        if board[x] == 'white':
            screen.blit(white, (fields_pos[x][0]-32.5, fields_pos[x][1]-32.5))
        elif board[x] == 'black':
            screen.blit(black, (fields_pos[x][0] - 32.5, fields_pos[x][1] - 32.5))

        # if pawn == 'white':
        #     print(x)
        #     screen.blit(white, (fields_pos[x][0]-32.5, fields_pos[x][1]-32.5))
        # elif pawn == 'black':
        #     print(x)
        #     screen.blit(black, (fields_pos[x][0] - 32.5, fields_pos[x][1] - 32.5))

    print(board)
    pygame.display.update()
    clock.tick(60)
    time.sleep(0.5)
