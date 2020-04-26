import pygame


class BlackPawn:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets/black.png')
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
