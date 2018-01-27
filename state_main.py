import sys, pygame
from pygame.locals import *
import state_gameover
from house import House
from house_generator import *

class Player:
    def __init__(self, x, y):
        self.worldX = 0
        self.worldY = 0
        self.screenX = x / 2
        self.screenY = y / 2
        self.visual = pygame.Rect((self.screenX, self.screenY, 10, 10))


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.nextstate = None
        self.dimensionX = screen.get_width()
        self.dimensionY = screen.get_height()
        self.screen_dimensions = (self.dimensionX, self.dimensionY)
        self.map = pygame.image.load_extended('Assets\GameJam\map.jpg')
        self.player = Player(self.dimensionX, self.dimensionY)
        self.house_list = []
    
    def endgame(self, victory):
        self.nextstate = state_gameover.EndScreen(self.screen, victory, -1234567890)
        self.done = True

    def generate_house_locations(self):
        valid_points = generate_house_locations()
        for house in valid_points:
            tuple = (house.x, house.y)
            self.house_list.append(House(*tuple))

    def main_loop(self):
        self.generate_house_locations()
        while not self.done:
            self.screen.blit(self.map, (self.player.worldX, self.player.worldY))
            pygame.draw.rect(self.screen, 255, self.player.visual)
            collision_visual = pygame.Rect((self.player.worldX,
                                            self.player.worldY, 10, 10))
            pygame.draw.rect(self.screen, 255, collision_visual)

            for house in self.house_list:
                object_screen_x = -house.worldX + self.player.worldX + (self.dimensionX / 2)
                object_screen_y = -house.worldY + self.player.worldY + (self.dimensionY / 2)

                house.visual.x = object_screen_x
                house.visual.y = object_screen_y
                pygame.draw.rect(self.screen, 255, house.visual)

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
                if event.type == QUIT:
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        # temporary death function
                        self.endgame(False)
                    if event.key == K_2:
                        # temporary victory function
                        self.endgame(True)

            pygame.display.flip()
        return self.nextstate
