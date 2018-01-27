import pygame
from pygame.locals import *
import main
from button import Button


class Menu:
    def __init__(self, screen):
        self.done = False
        self.nextstate = None
        self.screen = screen
        self.dimensionX = screen.get_width()
        self.dimensionY = screen.get_height()
        # Standin for buttons as they come
        WHITE = (255, 255, 255)
        textfont = pygame.font.Font('Assets\OpenSans-Regular.ttf', 30)
        playbutton = textfont.render("PLAY", True, WHITE)
        optionsbutton = textfont.render("OPTIONS", True, WHITE)
        quitbutton = textfont.render("QUIT", True, WHITE)
        self.buttons = [Button(screen, self.dimensionX / 2, self.dimensionY - 150, playbutton, self.startgame),
                        Button(screen, self.dimensionX / 2, self.dimensionY - 100, optionsbutton, self.enteroptions),
                        Button(screen, self.dimensionX / 2, self.dimensionY - 50, quitbutton, quit)]
        self.selectedbutton = -1
        
    def startgame(self):
        self.nextstate = main.Game(self.screen)
        self.done = True
    
    def enteroptions(self):
        print("ENTERED OPTIONS MENU")
    
    def main_loop(self):
        while True:
            if self.done:
                return self.nextstate
            self.screen.fill(0)
            for i, b in enumerate(self.buttons):
                b.show(self.selectedbutton == i)
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEMOTION:
                    self.selectedbutton = -1
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        if self.selectedbutton == -1:
                            self.selectedbutton = len(self.buttons) - 1
                        else:
                            self.selectedbutton = (self.selectedbutton - 1) % len(self.buttons)
                    if event.key == K_DOWN:
                        self.selectedbutton = (self.selectedbutton + 1) % len(self.buttons)
                    if event.key == K_RETURN:
                        self.buttons[self.selectedbutton].pressfunction()
            
            pygame.display.flip()
