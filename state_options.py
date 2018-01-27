import pygame
from pygame.locals import *
from button import Button

class Menu:
    def __init__(self, screen, statein):
        self.done = False
        self.screen = screen
        self.prevstate = statein
    
    def leaveoptions(self):
        self.done = True
        self.nextstate = self.prevstate
    
    def main_loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.leaveoptions()
        return self.nextstate