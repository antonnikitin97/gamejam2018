from random import randint
import random
import time
import pygame
import state_main
import copy
from pygame.locals import *

TRANSMISSION_EVENT = 10000
num_houses = 15
sound_endevent = pygame.event.Event(TRANSMISSION_EVENT)
noises = 0
symbols = 0
transmission_offset = 100
class HouseScreen:
    def __init__(self, screen, overworld, which):
        self.screen = screen
        self.done = False
        self.house = which
        self.waiting_sounds = []
        self.current_channel = pygame.mixer.Channel(0)
        global noises
        global symbols
        if noises == 0:
            freq = 44100    # audio CD quality
            bitsize = -16   # unsigned 16 bit
            channels = 2    # 1 is mono, 2 is stereo
            buffer = 1024    # number of samples
            pygame.mixer.init(freq, bitsize, channels, buffer)
            noises = self.load_bird_noises()
            print(len(noises))
            symbols = self.load_symbols()
            print(len(symbols))
        self.noises = noises
        self.symbols = symbols
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        self.textfont = pygame.font.Font('Assets\\OpenSans-Regular.ttf', 30)
        self.transmission = []
        self.transmission_received = False
        self.map = pygame.transform.scale(pygame.image.load_extended('Assets\\GameJam\\Interior2.png'), (960, 720))
        self.bubble = pygame.image.load_extended('Assets\\GameJam\\speech.png')
        self.router_birb = pygame.transform.scale(pygame.image.load_extended('Assets\\GameJam\\robobirb.png'), (int(594/5), int(841/5)))
        self.bounding_collider = pygame.Rect((200, 200, self.map.get_width() - 400, self.map.get_height() - 300))
        self.doormat_collider = pygame.Rect((300, 610, self.map.get_width() - 600, 20))
        self.overworld = overworld
        self.player2 = copy.copy(overworld.player)
        self.is_bubble_displayed = 0

    def load_bird_noises(self):
        return [pygame.mixer.Sound("Assets\\Audio\\bird" + str(i) + ".wav") for i in range(21)]

    def load_symbols(self):
        scale_const = 0.4
        imgs = [pygame.image.load_extended('Assets\\symbols\\' + str(i) + '.png') for i in range(1, 20)]
        return [pygame.transform.scale(img, (int(img.get_width() * scale_const),
                                             int(img.get_height() * scale_const))) for img in imgs]
    
    #TODO: each location should make a unique triplet or so from its settlement and number
    def get_location_encoding(self, id):
        loc_code = [int((id - (id % 5)) / 5), id % 5]
        print(id, loc_code)
        return loc_code

    def music_seq(self, length):
        #start on a random note
        #A-G = 0-7
        note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
        start = random.randint(0, 12)
        
        curr_offset = start - 6
        notes = [start]
        for i in range(length - 1):
            while True:
                step = random.choice([3, 5, 7])*random.choice([-1, 1])
                if len(notes) > 1 and (notes[-1] == notes[-2]) and step == 0:
                    continue
                #print(step)
                if abs(curr_offset + step) > 9:
                    continue
                else:
                    curr_offset = curr_offset + step
                    notes.append(curr_offset)
                    break
        #notes = [random.randint(-6, 7) for _ in range(length)]
        #return [note_names[n % 12]+str(3 if n < 0 else (5 if n == 12 else 4)) for n in notes]
        return [n + 7 for n in notes]

    #chooses a random house and makes a sequence of a given length along with a predefined header and end
    def make_transmission(self, from_id, length):
        while True:
            destination = random.randint(0, num_houses)
            if destination != from_id:
                break
        return self.get_location_encoding(destination) + self.music_seq(length)

    def start_receiving_transmission(self):
        #make a new transmission
        transmission = self.make_transmission(self.house, 5)
        print(transmission)
        #copy it over
        for note in transmission:
            #print('hi')
            self.waiting_sounds.append(note)
        #start off displaying the parts of the transmission
        print(self.noises)
        self.transmission_received = True
        self.is_bubble_displayed = -1
        self.display_next_sequence()

    def display_next_sequence(self):
        if len(self.waiting_sounds) == 0:
            return
        element = self.waiting_sounds.pop(0)
        # somehow draw a picture of the element here
        # e = self.symbols[element]
        
        self.current_channel.play(self.noises[element])
        self.transmission.append(element)
        
    def leavehouse(self):
        self.nextstate = self.overworld
        self.done = True

    def main_loop(self):
        chan = None
        self.player2.worldX = 400
        self.player2.worldY = 400
        self.player2.orient = 0
        self.done = False
        while not self.done:
            pressed_keys = pygame.key.get_pressed()
            self.player2.move(pressed_keys, self.bounding_collider)
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.map, (0, 0))
            self.screen.blit(self.router_birb, (transmission_offset + 480, transmission_offset + 180))
            # pygame.draw.rect(self.screen, 255, self.bounding_collider)
            # pygame.draw.rect(self.screen, 255, self.doormat_collider)
            if self.bounding_collider.contains(self.player2.collision):
                self.screen.blit(self.player2.get_sprite(), (self.player2.worldX, self.player2.worldY))
            if self.is_bubble_displayed != 0:
                self.screen.blit(self.bubble, (transmission_offset - 30, transmission_offset - 50))
            offs = 0
            for i in range(len(self.transmission)):
                thissymbol = self.symbols[self.transmission[i]]
                self.screen.blit(thissymbol, (transmission_offset + offs, transmission_offset))
                offs += thissymbol.get_width() + 5
            if self.doormat_collider.colliderect(self.player2.collision):
                self.leavehouse()
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_g:
                        if not len(self.waiting_sounds):
                            if not self.transmission_received:
                                chan = self.start_receiving_transmission()
                            else:
                                self.waiting_sounds = self.transmission.copy()
                                self.transmission = []
                                self.display_next_sequence()
                    if event.key == K_w:
                        self.leavehouse()

            while not self.current_channel.get_busy() and len(self.waiting_sounds):
                #print('aaaaa')
                self.display_next_sequence()
            pygame.display.flip()
        return self.nextstate