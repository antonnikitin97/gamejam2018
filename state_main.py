import sys, pygame
from pygame.locals import *
import state_gameover
from house import House
from house_generator import *


class Player:
    def __init__(self, x, y):
        self.worldX = x / 2
        self.worldY = y / 2
        self.screenX = x / 2
        self.screenY = y / 2
        self.speed = 10
        self.orient = 0
        self.img = pygame.transform.scale(pygame.image.load_extended('Assets\\GameJam\\flyspritefill.png'), (204, 152))
        self.down_img = pygame.transform.rotate(self.img, 90)
        self.right_img = pygame.transform.flip(self.img, True, False)
        self.up_img = pygame.transform.flip(self.down_img, False, True)
        self.swimg = pygame.transform.rotate(self.img, 45)
        self.nwimg = pygame.transform.rotate(self.img, 315)
        self.neimg = pygame.transform.rotate(self.up_img, 315)
        self.seimg = pygame.transform.rotate(self.up_img, 225)
        self.visual = pygame.Rect((self.screenX, self.screenY, 204, 152))
    def get_sprite(self):
        li = [self.img, self.down_img, self.right_img, self.up_img, self.nwimg, self.swimg, self.neimg, self.seimg]
        return li[self.orient]

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.nextstate = None
        self.dimensionX = screen.get_width()
        self.dimensionY = screen.get_height()
        self.screen_dimensions = (self.dimensionX, self.dimensionY)
        self.map = pygame.transform.scale(pygame.image.load_extended('Assets\GameJam\map.jpg'), (3000, 2550))
        self.house = pygame.image.load_extended('Assets\\GameJam\\house.png')
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
            self.screen.fill((38, 142, 143))
            self.screen.blit(self.map, (- self.player.worldX + self.dimensionX/2, - self.player.worldY  + self.dimensionY/2))
            #pygame.draw.rect(self.screen, 255, self.player.visual)
            #wtf is this collision thing 
            #it's not right
            #collision_visual = pygame.Rect((self.player.worldX,
            #                                self.player.worldY, 10, 10))
            #pygame.draw.rect(self.screen, 255, collision_visual)

            for house in self.house_list:
                object_screen_x = house.worldX - self.player.worldX + (self.dimensionX / 2) - house.size/2
                object_screen_y = house.worldY - self.player.worldY + (self.dimensionY / 2) - house.size/2

                house.visual.x = object_screen_x
                house.visual.y = object_screen_y
                self.screen.blit(self.house, house.visual)
            self.screen.blit(self.player.get_sprite(), self.player.visual)
            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_DOWN]:
                self.player.worldY += self.player.speed
                self.player.orient = 1
            if pressed_keys[K_UP]:
                self.player.worldY -= self.player.speed
                self.player.orient = 3
            if pressed_keys[K_LEFT]:
                self.player.worldX -= self.player.speed
                self.player.orient = 0
                if pressed_keys[K_UP]:
                    self.player.orient = 4
                if pressed_keys[K_DOWN]:
                    self.player.orient = 5
            if pressed_keys[K_RIGHT]:
                self.player.worldX += self.player.speed
                self.player.orient = 2
                if pressed_keys[K_UP]:
                    self.player.orient = 6
                if pressed_keys[K_DOWN]:
                    self.player.orient = 7
                print(self.player.worldX, self.player.worldY)

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

import StateMachine
StateMachine.run()