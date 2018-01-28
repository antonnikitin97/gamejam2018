import sys, pygame
from pygame.locals import *
import state_gameover
import state_house
import state_options
import state_journal
from house import House
from house_generator import *
import time
import math
from entity import Entity

class Player:
    def __init__(self, dimensionX, dimensionY):
        self.worldX = 3671
        self.worldY = 2085
        self.screenX = dimensionX / 2
        self.screenY = dimensionY / 2
        self.speed = 10
        self.orient = 0
        img = [pygame.transform.scale(pygame.image.load_extended('Assets\\Images\\Bird Frame {}.png'.format(i)).convert_alpha(),
                                      (204, 152)) for i in range(1, 6)]
        down_img = [pygame.transform.rotate(img[i], 90).convert_alpha() for i in range(len(img))]
        right_img = [pygame.transform.flip(img[i], True, False).convert_alpha() for i in range(len(img))]
        up_img = [pygame.transform.flip(down_img[i], False, True).convert_alpha() for i in range(len(img))]
        swimg = [pygame.transform.rotate(img[i], 45).convert_alpha() for i in range(len(img))]
        nwimg = [pygame.transform.rotate(img[i], 315).convert_alpha() for i in range(len(img))]
        neimg = [pygame.transform.rotate(up_img[i], 315).convert_alpha() for i in range(len(img))]
        seimg = [pygame.transform.rotate(up_img[i], 225).convert_alpha() for i in range(len(img))]
        self.spritearray = [img, down_img, right_img, up_img,
                            nwimg, swimg, neimg, seimg]
        self.frame = 0
        self.lastspritechangetime = 0
        self.visual = pygame.Rect((self.screenX - 76, self.screenY - 76, 152, 152))
        self.collision = pygame.Rect((self.worldX - 76, self.worldY - 76, 152, 152))
        self.projected_collision = pygame.Rect((self.worldX, self.worldY, 204, 152))
        self.current_transmissions = []
    
    def get_sprite(self):
        return self.spritearray[self.orient][self.frame]

    def add_transmission(self, dest, transmission):
        if (dest, transmission) in self.current_transmissions:
            return
        else:
            print(transmission)
            self.current_transmissions.append((dest, transmission[2:]))
    def get_transmission(self, dest):
        print(self.current_transmissions)
        for d in self.current_transmissions:
            if d[0] == dest:
                return d[1]
        return None
    
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
        if time.time() - self.lastspritechangetime > 0.02:
            self.frame = (self.frame + 1) % len(self.spritearray[0])
            self.lastspritechangetime = time.time()


class Game:
    def __init__(self, screen, options):
        self.screen = screen
        self.options = options
        self.options["TOTAL"] = 0
        self.options["DELIVERED"] = 0
        self.options["TIME"] = 0
        self.done = False
        self.nextstate = None
        self.dimensionX = screen.get_width()
        self.dimensionY = screen.get_height()
        self.screen_dimensions = (self.dimensionX, self.dimensionY)
        self.islandmap = pygame.image.load_extended('Assets\Images\WorldMap.png').convert_alpha()
        self.oceantile = pygame.image.load_extended('Assets\Images\WavesSolo.png').convert_alpha()
        self.oceanborderx = 1035
        self.oceanbordery = 987
        self.islandrect = pygame.Rect(self.oceanborderx, self.oceanbordery,
                                      self.islandmap.get_width(), self.islandmap.get_height())
        self.map = pygame.Surface((self.islandmap.get_width() + self.oceanborderx * 2,
                                   self.islandmap.get_height() + self.oceanbordery * 2)).convert_alpha(self.islandmap)
        self.map.fill((0, 0, 0, 0))
        for i in range(0, self.map.get_width(), self.oceantile.get_width()):
            for j in range(0, self.map.get_height(), self.oceantile.get_height()):
                self.map.blit(self.oceantile, (i, j))
        self.map.blit(self.islandmap, (self.oceanborderx, self.oceanbordery))
        self.house = pygame.transform.scale(pygame.image.load_extended('Assets\\Images\\Exterior.png'),
                                            (int(860/2), int(878/2))).convert_alpha()
        self.tree = pygame.transform.scale(pygame.image.load_extended('Assets\\Images\\Tree Translucent.png'),
                                           (int(2421/5), int(1977/5))).convert_alpha()
        self.player = Player(self.dimensionX, self.dimensionY)
        self.player.worldX += self.oceanborderx
        self.player.worldY += self.oceanbordery
        self.house_list = []
        self.house_states = []
        self.generate_terrain()
        self.textfont = pygame.font.Font('Assets/OpenSans-Regular.ttf', 30)
        self.arrow = pygame.image.load_extended('Assets\\Images\\arrow.png').convert_alpha()
        self.arrow2 = pygame.transform.scale(pygame.image.load_extended('Assets\\GameJam\\arrow2.png'),
                                             (100, 100)).convert_alpha()
        self.broadcast = pygame.transform.scale(pygame.image.load_extended('Assets\\broadcast.png'),
                                                (int(417/2.5), int(188/2.5))).convert_alpha()
        self.danger = False
        self.transmission_time = 30
        self.transmission_event = pygame.USEREVENT + 5
        self.initial = True
        pygame.time.set_timer(self.transmission_event, self.transmission_time * 1000)
        self.start = 0
        self.paused = False
        self.journalstate = state_journal.Book(self.screen, self.options, self, self.map, self.house_list)
        
    def rotatePoint(self, centerPoint, point, angle):
        """Rotates a point around another centerPoint. Angle is in degrees.
        Rotation is counter-clockwise"""
        angle = math.radians(angle)
        temp_point = point[0] - centerPoint[0] , point[1] - centerPoint[1]
        temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
        temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
        return temp_point

    def generate_terrain(self):
        # Houses
        valid_points = generate_house_locations(self.house,
                                                self.map.get_width() / 2, self.map.get_height() / 2,
                                                min(self.islandmap.get_width(), self.islandmap.get_height()) / 2 - 400,
                                                10)
        for i, house in enumerate(valid_points):
            tuple = (house.x, house.y)
            self.house_list.append(House(*tuple, self.house))
        #print(self.house_list)
        self.house_list = sorted(self.house_list, key=lambda house: house.worldY)
        #print(self.house_list)
        self.house_states = []
        self.house_assets = (pygame.transform.scale(pygame.image.load_extended('Assets\\Images\\Interior2.png'),
                                                    (int(1045 * 0.9), int(888 * 0.9))).convert_alpha(),
                             pygame.image.load_extended('Assets\\GameJam\\speech.png').convert_alpha(),
                             pygame.transform.scale(pygame.image.load_extended('Assets\\GameJam\\robobirb.png'),
                                                    (int(594/5), int(841/5))).convert_alpha(),
                             pygame.image.load_extended('Assets\\Images\\symbutt.png'),
                             pygame.font.Font('Assets\\OpenSans-Regular.ttf', 30), pygame.image.load_extended('Assets\\Images\\tick.png'),
                             pygame.image.load_extended('Assets\\Images\\cross.png'))
        for i, house in enumerate(self.house_list):
            self.map.blit(self.house, (house.worldX, house.worldY))
            self.house_states.append(state_house.HouseScreen(self.screen, self.options, self, i, self.house_list[i], self.house_assets))
        # Trees
        for pos in generate_house_locations(self.tree, self.islandmap.get_width() * 0.7 + self.oceanborderx,
                                                       self.islandmap.get_height() * 0.3 + self.oceanbordery,
                                            self.islandmap.get_height() * 0.3, 3):
            self.map.blit(self.tree, (pos.x, pos.y))
    
    def fire_transmission(self):
        self.initial = False
        print('fired')
        #pick a house that isn't currently broadcasting - NB this can be a house expecting to receive a broadcast
        curr_house_pick = -1
        while True:
            curr_house_pick = random.choice(self.house_list)
            if curr_house_pick.broadcast_status[0]:
                continue
            break
        curr_house_pick.broadcast_status = (True, curr_house_pick.broadcast_status[1])
        #set it to be currently broadcasting
    
    def endgame(self, victory):
        self.nextstate = state_gameover.EndScreen(self.screen, self.options, victory, time.time() - self.start)
        self.done = True
    
    def enterhouse(self, which):
        self.done = True
        print("Entered house", which)
        self.nextstate = self.house_states[which]
        self.pause()
    
    def enteroptions(self):
        self.done = True
        self.nextstate = state_options.Menu(self.screen, self.options, self)
        self.pause()
    
    def enterjournal(self):
        self.done = True
        self.nextstate = self.journalstate
        self.pause()
        
    def pause(self):
        self.options["TIME"] += time.time() - self.start
        print("Timer paused at", self.options["TIME"])
        self.paused = True
    
    def unpause(self):
        self.start = time.time()
        print("Timer unpaused at", self.options["TIME"])
        self.paused = False

    def main_loop(self):
        self.done = False
        #on the first run, immediately run a transmission and start the timer
        if self.initial:
            self.fire_transmission()
            self.initial = False
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        self.unpause()
        while not self.done:
            self.screen.fill((38, 142, 143))
            self.screen.blit(self.map, ((self.dimensionX / 2) - self.player.worldX,
                                        (self.dimensionY / 2) - self.player.worldY))
                   
            if not self.islandrect.colliderect(self.player.collision):
                self.danger = True
                text_surface = self.textfont.render('DANGER!', False, WHITE, BLACK).convert_alpha()
                self.screen.blit(text_surface, (20,20))

            # if we have transmissions, add an arrow
            broadcasting = [i for i in self.house_list if i.broadcast_status[0]]
            if len(broadcasting):
                for house in broadcasting:
                    if distance(Point(house.worldX, house.worldY),
                                Point(self.player.worldX, self.player.worldY)) + 300 < math.sqrt(
                            (self.dimensionX / 2) ** 2 + (self.dimensionY / 2) ** 2):
                        self.screen.blit(self.broadcast, (
                        house.worldX - self.player.worldX + (self.dimensionX + house.visual.width) / 2 - 109,
                        house.worldY - self.player.worldY + 150 + (self.dimensionY - house.visual.height) / 2 + 65))
                # find nearest house
                nearest = min(broadcasting, key=lambda h: distance(Point(h.worldX, h.worldY),
                                                                   Point(self.player.worldX, self.player.worldY)))
                # find rotation
                rot = -math.degrees(
                    math.atan2(nearest.worldY - self.player.worldY, nearest.worldX - self.player.worldX)) % 360
                if distance(Point(nearest.worldX, nearest.worldY),
                            Point(self.player.worldX, self.player.worldY)) + 300 > math.sqrt(
                        (self.dimensionX / 2) ** 2 + (self.dimensionY / 2) ** 2):
                    self.screen.blit(pygame.transform.rotate(self.arrow2, rot + 90).convert_alpha(),
                                     self.rotatePoint((self.dimensionX / 2, self.dimensionY / 2),
                                                      (int(self.dimensionX / 2) - 50, 100), - rot + 90))

                # TODO: if any house on screen is broadcasting, don't show an arrow

            housecollide = [-1, self.dimensionX]
            for i, house in enumerate(self.house_list):
                house.visual.x = house.worldX - self.player.worldX + (self.dimensionX) / 2
                house.visual.y = house.worldY - self.player.worldY + (self.dimensionY) / 2
                #self.screen.fill(0, house.visual)  # for debugging hitboxes
                if self.player.visual.colliderect(house.visual):
                    d = sqrt((self.player.worldX - house.worldX) ** 2 +
                             (self.player.worldY - house.worldY) ** 2)
                    if housecollide[1] > d:
                        housecollide = [i, d]
            if housecollide[0] != -1:
                house = self.house_list[housecollide[0]]
                arrowx = house.worldX - self.player.worldX + (self.dimensionX - self.arrow.get_width() + house.visual.width)/2
                arrowy = house.worldY - self.player.worldY - 50 + (self.dimensionY - self.arrow.get_height())/2
                numberarrow = self.arrow.copy()
                number = self.textfont.render(str(housecollide[0]), True, BLACK).convert_alpha()
                numberarrow.blit(number, ((self.arrow.get_width() - number.get_width())/2 + 5,
                                          (self.arrow.get_height() - number.get_height())/2))
                self.screen.blit(numberarrow, (arrowx, arrowy))
                if pygame.key.get_pressed()[K_g]:
                    self.enterhouse(housecollide[0])
                text_surface = self.textfont.render('Press G to enter house {}'.format(housecollide[0]),
                                                    False, WHITE, BLACK).convert_alpha()
                self.screen.blit(text_surface, (20, 20))
            #self.screen.fill(0, self.player.visual)  # for debugging hitboxes
            pressed_keys = pygame.key.get_pressed()
            self.player.move(pressed_keys)
            
            playersprite = self.player.get_sprite()
            self.screen.blit(playersprite, ((self.dimensionX - playersprite.get_width())/2,
                                            (self.dimensionY - playersprite.get_height())/2))
            
            scoretext = self.textfont.render("Score: {}/{}".format(self.options["DELIVERED"], self.options["TOTAL"]),
                                             True, BLACK, WHITE).convert_alpha()
            scoretext = self.textfont.render("Score: " + str(self.options["TOTAL"]), True, BLACK, WHITE).convert_alpha()
            scoretext2 = self.textfont.render("Delivered: {}/{}".format(self.options["DELIVERED"], self.options["OUT_OF"]), True, BLACK, WHITE).convert_alpha()
            scoretext3 = self.textfont.render("Accuracy: {0:.0f}%".format(self.options["CORRECT_SYM"]*100/(self.options["TOTAL_SYM"] \
             if self.options["TOTAL_SYM"] != 0 else 1)), True, BLACK, WHITE).convert_alpha()
            timetext = self.textfont.render("Time: {:0.2f}".format(self.options["TIME"] + (time.time() - self.start) * (not self.paused)),
                                            True, BLACK, WHITE).convert_alpha()
            self.screen.blit(scoretext, (self.dimensionX - scoretext.get_width() - 5, 5))
            self.screen.blit(scoretext2, (self.dimensionX - scoretext2.get_width() - 5, 40))
            self.screen.blit(scoretext3, (self.dimensionX - scoretext2.get_width() - 5, 75))
            self.screen.blit(timetext, (self.dimensionX - timetext.get_width() - 5, 115))
            
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
                    if event.key == K_ESCAPE:
                        self.enteroptions()
                    if event.key == K_w:
                        self.enterjournal()
                if event.type == self.transmission_event:
                    #print('THIS WORKED')
                    self.fire_transmission()

            pygame.display.flip()
            pygame.time.wait(3)
        return self.nextstate
