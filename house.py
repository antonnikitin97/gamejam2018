from entity import Entity
import pygame

class House(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.visual = pygame.Rect((self.worldX, self.worldY,150, 200))
        self.size = 200
        # self.visual_representation =