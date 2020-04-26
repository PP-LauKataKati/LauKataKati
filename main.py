import pygame
import sys

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(background, (0, 0))

    for pos in black_pos:
        screen.blit(black, pos)

    for pos in white_pos:
        screen.blit(white, pos)

    pygame.display.update()
    clock.tick(60)
