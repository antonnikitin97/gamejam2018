import pygame
from pygame.locals import *
import state_menu
from button import Button

class Instr:
    def __init__(self, screen, backto):
        self.done = False
        self.screen = screen
        self.dimensionX = self.screen.get_width()
        self.dimensionY = self.screen.get_height()
        self.instr1 = pygame.image.load_extended('Assets\\Images\\instr.png')
        self.instr2 = pygame.image.load_extended('Assets\\Images\\instr2.png')
        self.backto = backto
        self.sndpage = False
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        textfont = pygame.font.Font('Assets\OpenSans-Regular.ttf', 30)
        # Standin for buttons as they come
        fullscreenbutton = textfont.render("PREV", True, BLACK, WHITE)
        menubutton = textfont.render("QUIT TO MAIN MENU", True, BLACK, WHITE)
    
    def tomainmenu(self):
        self.done = True
        self.nextstate = self.backto
    
    def main_loop(self):
        while not self.done:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.instr1 if self.sndpage is False else self.instr2, (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEMOTION:
                    self.selectedbutton = -1
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                       self.sndpage = False
                    if event.key == K_RIGHT:
                        self.sndpage = True
                    if event.key == K_ESCAPE:
                        self.tomainmenu()
            pygame.display.flip()
        return self.nextstate