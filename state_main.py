import sys, pygame
from pygame.locals import *
import state_gameover
from house import House
import state_house
from house_generator import *
from entity import Entity

class Player:
    def __init__(self, x, y):
        self.img = pygame.transform.scale(pygame.image.load_extended('Assets\\GameJam\\flyspritefill.png'), (204, 152))
        self.worldX = x / 2
        self.worldY = y / 2
        self.screenX = self.worldX
        self.screenY = self.worldY
        self.speed = 10
        self.orient = 0
        self.down_img = pygame.transform.rotate(self.img, 90)
        self.right_img = pygame.transform.flip(self.img, True, False)
        self.up_img = pygame.transform.flip(self.down_img, False, True)
        self.swimg = pygame.transform.rotate(self.img, 45)
        self.nwimg = pygame.transform.rotate(self.img, 315)
        self.neimg = pygame.transform.rotate(self.up_img, 315)
        self.seimg = pygame.transform.rotate(self.up_img, 225)
        self.visual = pygame.Rect((self.screenX, self.screenY, 204, 152))
        self.collision = pygame.Rect((self.worldX, self.worldY, 204, 152))
        self.projected_collision = pygame.Rect((self.worldX, self.worldY, 204, 152))
    
    def get_sprite(self):
        li = [self.img, self.down_img, self.right_img, self.up_img, self.nwimg, self.swimg, self.neimg, self.seimg]
        return li[self.orient]
    
    def move(self, pressed_keys, projected_box=None):
        self.collision = pygame.Rect((self.worldX, self.worldY, 204, 152))
        xdiff = 0
        ydiff = 0
        if pressed_keys[K_DOWN]:
            ydiff = self.speed
            self.orient = 1
        if pressed_keys[K_UP]:
            ydiff = -self.speed
            self.orient = 3
        if pressed_keys[K_LEFT]:
            xdiff = -self.speed
            self.orient = 0
            if pressed_keys[K_UP]:
                self.orient = 4
            if pressed_keys[K_DOWN]:
                self.orient = 5
        if pressed_keys[K_RIGHT]:
            xdiff = self.speed
            self.orient = 2
            if pressed_keys[K_UP]:
                self.orient = 6
            if pressed_keys[K_DOWN]:
                self.orient = 7
        self.projected_collision = pygame.Rect((self.worldX + xdiff, self.worldY + ydiff, 204, 152))
        if projected_box == None:
            self.worldX += xdiff
            self.worldY += ydiff
        elif projected_box.contains(self.projected_collision):
            self.worldX += xdiff
            self.worldY += ydiff


class Game:
    def __init__(self, screen):
        pygame.font.init()
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
        self.house_states = []
        self.generate_house_locations()
        self.textfont = pygame.font.Font('Assets/OpenSans-Regular.ttf', 30)
        self.danger = False

    def generate_house_locations(self):
        valid_points = generate_house_locations()
        for house in valid_points:
            tuple = (house.x, house.y)
            self.house_list.append(House(*tuple))
            self.house_states.append(state_house.HouseScreen(self.screen, self))
    
    def endgame(self, victory):
        self.nextstate = state_gameover.EndScreen(self.screen, victory, -1234567890)
        self.done = True
    
    def enterhouse(self, which):
        self.done = True
        print("Entered house", which)
        self.nextstate = self.house_states[which]

    def main_loop(self):
        self.done = False
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        while not self.done:
            self.screen.fill((38, 142, 143))
            self.screen.blit(self.map, ((self.dimensionX / 2) - self.player.worldX,
                                        (self.dimensionY / 2) - self.player.worldY))
            #pygame.draw.rect(self.screen, 255, self.player.visual)
            #wtf is this collision thing 
            #it's not right
            #collision_visual = pygame.Rect((self.player.worldX,
            #                                self.player.worldY, 10, 10))
            #pygame.draw.rect(self.screen, 255, collision_visual)

            for house in self.house_list:
                object_screen_x = house.worldX - self.player.worldX + (self.dimensionX / 2) - house.visual.width/2
                object_screen_y = house.worldY - self.player.worldY + (self.dimensionY / 2) - house.visual.height/2

                house.visual.x = object_screen_x
                house.visual.y = object_screen_y

                #pygame.draw.rect(self.screen, 255, house.visual)
                self.screen.blit(self.house, house.visual)

                # if self.player.worldX - self.dimensionX / 2 >= 0 and self.player.worldX - self.dimensionX / 2 <= 640 and \
                #         self.player.worldY - self.dimensionY / 2 >= 0 and self.player.worldY - self.dimensionY / 2 <= 480:
                color_pixel = self.screen.get_at((int(self.player.visual.centerx), int(self.player.visual.centery)))

                if color_pixel.r == 38 and color_pixel.g == 142 and color_pixel.b == 143:
                    self.danger = True
                    text_surface = self.textfont.render('DANGER!', False, WHITE, BLACK)
                    self.screen.blit(text_surface, (20,20))

            housecollide = self.player.visual.collidelist([house.visual for house in self.house_list])
            if housecollide != -1:
                text_surface = self.textfont.render('Press G to enter the house! :)', False, WHITE, BLACK)
                self.screen.blit(text_surface, (20, 20))
                if pygame.key.get_pressed()[K_g]:
                    self.enterhouse(housecollide)
            self.screen.blit(self.player.get_sprite(), self.player.visual)
            #pygame.draw.rect(self.screen, 255, self.player.visual)
            pressed_keys = pygame.key.get_pressed()
            self.player.move(pressed_keys)
            
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