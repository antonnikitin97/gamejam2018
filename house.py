from entity import Entity
import pygame

class House(Entity):
    def __init__(self, x, y, sprite):
        super().__init__(x, y)
        self.visual = pygame.Rect((0, 0,
                                   sprite.get_width(),
                                   sprite.get_height()))
        self.size = max(sprite.get_width(), sprite.get_height())