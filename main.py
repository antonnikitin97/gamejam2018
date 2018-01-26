import sys
import pygame
from pygame.locals import *

class Player:

    def __init__(self, x, y):
        self.worldX = 0
        self.worldY = 0
        self.screenX = x / 2
        self.screenY = y / 2
        self.visual = pygame.Rect((self.screenX, self.screenY, 10, 10))


class Game:



    def __init__(self):
        pygame.init()
        self.done = False
        self.dimensionX = 640
        self.dimensionY = 480
        self.screen_dimensions = (self.dimensionX, self.dimensionY)
        self.screen = pygame.display.set_mode(self.screen_dimensions)

        self.map = pygame.image.load('Assets\GameJam\map.jpg')
        self.player = Player(self.dimensionX, self.dimensionY)

    def main_loop(self):
        while not self.done:
            self.screen.blit(self.map, (self.player.worldX, self.player.worldY))
            pygame.draw.rect(self.screen, 255, self.player.visual)
            collision_visual = pygame.Rect((self.player.screenX - self.player.worldX, self.player.screenY - self.player.worldY, 10, 10))
            pygame.draw.rect(self.screen, 255, collision_visual)

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_DOWN]:
                self.player.worldY -= 2
            if pressed_keys[K_UP]:
                self.player.worldY += 2
            if pressed_keys[K_LEFT]:
                self.player.worldX += 2
            if pressed_keys[K_RIGHT]:
                self.player.worldX -= 2

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            pygame.display.flip()


game = Game()
game.main_loop()
