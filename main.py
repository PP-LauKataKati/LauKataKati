import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Lau kata kati')

background = pygame.image.load("assets/board.png").convert()

clock = pygame.time.Clock()

board = [None] * 21
board[9] = 'X'
board[11] = 'X'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(background, (0, 0))
    pygame.display.update()
    clock.tick(60)
