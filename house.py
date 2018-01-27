from entity import Entity
import pygame

class House(Entity):
    def __init__(self, x, y, sprite):
        super().__init__(x, y)
        self.visual = pygame.Rect((self.worldX, self.worldY,
                                   sprite.get_width(),
                                   sprite.get_height()))
        self.size = max(sprite.get_width(), sprite.get_height())
        # self.visual_representation =