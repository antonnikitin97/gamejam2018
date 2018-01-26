import sys
import pygame


class Game():

    def __init__(self):
        pygame.init()
        self.done = False
        self.dimensionX = 640
        self.dimensionY = 480
        self.screen_dimensions = tuple([self.dimensionX, self.dimensionY])
        self.screen = pygame.display.set_mode(self.screen_dimensions)

    def main_loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            pygame.display.flip()


game = Game()
game.main_loop()
