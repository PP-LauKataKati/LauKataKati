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

black_pos = [[85, 55], [351, 55], [618, 55], [177, 155], [351, 155], [529, 155], [262, 255], [351, 255], [440, 255]]
white_pos = [[85, 655], [351, 655], [618, 655], [177, 555], [351, 555], [529, 555], [262, 455], [351, 455], [440, 455]]
all_pos = [[85, 55], [351, 55], [618, 55], [177, 155], [351, 155], [529, 155], [262, 255], [351, 255], [440, 255],
           [85, 655], [351, 655], [618, 655], [177, 555], [351, 555], [529, 555], [262, 455], [351, 455], [440, 455], [351,  355]]

black_pawns = []
white_pawns = []

for pos in black_pos:
    pioneczek = black_pawn.BlackPawn(pos[0], pos[1])
    black_pawns.append(pioneczek)

for pos in white_pos:
    pioneczek = white_pawn.WhitePawn(pos[0], pos[1])
    white_pawns.append(pioneczek)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            xMouse = event.pos[0]
            yMouse = event.pos[1]
            print(xMouse, yMouse)
            for pawn in white_pawns:
                print(pawn.x, pawn.y)
                if pawn.rect.collidepoint(xMouse, yMouse):
                    pawn.x = xMouse
                    pawn.y = yMouse

    screen.blit(background, (0, 0))

    for pawn in black_pawns:
        screen.blit(pawn.image, (pawn.x, pawn.y))

    for pawn in white_pawns:
        screen.blit(pawn.image, (pawn.x, pawn.y))

    pygame.display.update()
    clock.tick(60)
