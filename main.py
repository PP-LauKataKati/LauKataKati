import pygame
import sys
import white_pawn
import black_pawn

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Lau kata kati')

background = pygame.image.load('assets/board.png').convert()
white = pygame.image.load('assets/white.png')
black = pygame.image.load('assets/black.png')

clock = pygame.time.Clock()

board = [None] * 21
board[9] = 'X'
board[11] = 'X'

black_pos = [[110, 70], [368, 70], [630, 70], [190, 170], [368, 170], [545, 170], [279, 270], [368, 270], [457, 270]]
white_pos = [[110, 670], [368, 670], [630, 670], [190, 570], [368, 570], [545, 570], [279, 470], [368, 470], [457, 470]]
all_pos = [[110, 70], [368, 70], [630, 70], [190, 170], [368, 170], [545, 170], [279, 270], [368, 270], [457, 270],
           [110, 670], [368, 670], [630, 670], [190, 570], [368, 570], [545, 570], [279, 470], [368, 470], [457, 470]]

black_pawns = []
white_pawns = []

done = False

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

            clicked_white = [p for p in white_pawns if p.rect.collidepoint(xMouse, yMouse)]
            clicked_black = [p for p in black_pawns if p.rect.collidepoint(xMouse, yMouse)]

            if len(clicked_white) == 1:
                clicked_pawn = clicked_white[0]

            elif len(clicked_black) == 1:
                clicked_pawn = clicked_black[0]

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
            clicked_pawn.x = xMouse2
            clicked_pawn.y = yMouse2
            clicked_pawn.rect.center = (clicked_pawn.x, clicked_pawn.y)

    screen.blit(background, (0, 0))

    for pawn in black_pawns:
        screen.blit(pawn.image, (pawn.x, pawn.y))

    for pawn in white_pawns:
        screen.blit(pawn.image, (pawn.x, pawn.y))

    pygame.display.update()
    clock.tick(60)
