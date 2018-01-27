import pygame
from entity import Entity


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.visual = pygame.Rect((self.screenX, self.screenY, 10, 10))
        # self.visual_representation =