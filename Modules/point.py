import pygame


# define the points class
class Point:
    #each point is drawn at it's given (x,y)
    def __init__(self, x, y):
        self.image = pygame.image.load("Resources\\Point.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
