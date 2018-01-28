from random import randint
import random
import time
import pygame
import state_options
import copy
import button
from pygame.locals import *

TRANSMISSION_EVENT = 10000
num_houses = 15
sound_endevent = pygame.event.Event(TRANSMISSION_EVENT)
noises = 0
symbols = 0
transmission_offset = 100
class HouseScreen:
    def __init__(self, screen, options, overworld, which, which_obj, house_assets):
        self.screen = screen
        self.options = options
        self.done = False
        self.house = which
        self.house_obj = which_obj
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
        self.transmission = []
        self.transmission_received = False
        self.map, self.bubble, self.router_birb, self.button_back, self.textfont = house_assets
        self.bounding_collider = pygame.Rect((200, 200, self.map.get_width() - 400, self.map.get_height() - 300))
        self.doormat_collider = pygame.Rect((300, 610, self.map.get_width() - 600, 20))
        self.overworld = overworld
        self.player2 = copy.copy(overworld.player)
        self.is_bubble_displayed = 0
        button_offset = 400
        self.buttons = []
        self.currently_entered_sequence = []
        self.is_in_receive = False
        self.has_finished_inputting = False
    def load_bird_noises(self):
        return [pygame.mixer.Sound("Assets\\Audio\\bird" + str(i) + ".wav") for i in range(21)]

    def load_symbols(self):
        scale_const = 0.4
        imgs = [pygame.image.load_extended('Assets\\symbols\\' + str(i) + '.png').convert_alpha() for i in range(1, 20)]
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

    def generate_offered_sequence(self, expected_transmission):
        def get_options(given):
            a, b = -1, -1
            while True:
                a, b = random.randint(0, 18), random.randint(0, 18)
                if a == given or a == b or b == given:
                    continue
                break
            print(a, b)
            li = [a, b, given]
            random.shuffle(li)
            return li
        return [get_options(e) for e in expected_transmission]
    def start_delivering_transmission(self):       
        #to deliver a transmission, the player is presented with 3 options
        #each option has a symbol and a noise
        #click the symbol to add it to the transmission
        #then compare the two?
        self.is_in_receive = True
        expected_transmission = []
        if self.house_obj.broadcast_status[1]:
            expected_transmission = self.overworld.player.get_transmission(self.house)
        else:
            #no match, so give it at random
            expected_transmission = self.music_seq(5)
        print(expected_transmission)
        offered_sequence = self.generate_offered_sequence(expected_transmission)
        print(offered_sequence)
        self.display_delivery_options(offered_sequence[0])
        return offered_sequence[1:]

    def optionselected(self, id):
        self.currently_entered_sequence.append(id)
        print(self.currently_entered_sequence)
        #should also add it to a big speech bubble thing

        if len(self.current_delivery) != 0:
            next_entry = self.current_delivery.pop(0)
            self.display_delivery_options(next_entry)
        else:
            self.has_finished_inputting = True


        #todo: put 
    def display_delivery_options(self, options):
        butts = []
        for i in range(len(options)):
            b1 = button.ButtonWithStuffOn(self.screen, int(i*self.overworld.dimensionX/3) + self.button_back.get_width()/2, 480, self.button_back, self.symbols[options[i]], \
                self.noises[options[i]], self.optionselected, options[i])
            butts.append(b1)
        self.buttons = butts
        print('added butts')

    #chooses a random house and makes a sequence of a given length along with a predefined header and end
    def make_transmission(self, from_id, length):
        while True:
            destination = random.randint(0, num_houses)
            if destination != from_id:
                break
        return destination, self.get_location_encoding(destination) + self.music_seq(length)

    def start_receiving_transmission(self):
        #make a new transmission
        dest, transmission = self.make_transmission(self.house, 5)
        self.overworld.player.add_transmission(dest, transmission)
        self.overworld.house_list[dest].broadcast_status = (self.overworld.house_list[dest].broadcast_status[0], True)
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
        
    def enteroptions(self):
        self.done = True
        self.nextstate = state_options.Menu(self.screen, self.options, self)
    
    def leavehouse(self):
        self.nextstate = self.overworld
        self.is_in_receive = False
        self.currently_entered_sequence = []
        self.done = True

    def main_loop(self):
        chan = None
        self.player2.worldX = 400
        self.player2.worldY = 400
        self.player2.orient = 0
        self.done = False
        while not self.done:
            pressed_keys = pygame.key.get_pressed()
            if not self.is_in_receive:
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
                            if not self.transmission_received and self.house_obj.broadcast_status[0] and not self.is_in_receive:
                                chan = self.start_receiving_transmission()
                            else:
                                self.waiting_sounds = self.transmission.copy()
                                self.transmission = []
                                self.display_next_sequence()
                    if event.key == K_d and not self.current_channel.get_busy():
                        self.current_delivery = self.start_delivering_transmission()
                        if not self.house_obj.broadcast_status[1]:
                            print('wrong house')
                        else:
                            print('right house')
                    if event.key == K_w:
                        self.leavehouse()
            while not self.current_channel.get_busy() and len(self.waiting_sounds):
                #print('aaaaa')
                self.display_next_sequence()
            if self.is_in_receive:
                for i, b in enumerate(self.buttons):
                    if not self.has_finished_inputting:
                        b.show(0)
                self.screen.blit(pygame.transform.flip(self.bubble, True, False), (transmission_offset - 30, transmission_offset - 90))
                for i in range(len(self.currently_entered_sequence)):
                    thissymbol = self.symbols[self.currently_entered_sequence[i]]
                    self.screen.blit(thissymbol, (transmission_offset + offs + 200, transmission_offset - 30))
                    offs += thissymbol.get_width() + 5

            pygame.display.flip()
        return self.nextstate