import pygame
from pygame.locals import *
import state_menu
from button import Button
import os

class Menu:
    def __init__(self, screen, options, statein, backtogame=True):
        self.done = False
        self.screen = screen
        self.options = options
        self.dimensionX = self.screen.get_width()
        self.dimensionY = self.screen.get_height()
        self.backgrd = pygame.image.load_extended(os.path.join('Assets','Images','Tree Translucent.png')).convert_alpha()
        self.backgrd = pygame.transform.scale(self.backgrd, (int(self.backgrd.get_width()/2.1), int(self.backgrd.get_height()/2.1)))
        self.prevstate = statein
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        textfont = pygame.font.Font(os.path.join('Assets','OpenSans-Regular.ttf'), 30)
        # Standin for buttons as they come
        fullscreenbutton = textfont.render("TOGGLE FULLSCREEN", True, BLACK, WHITE)
        menubutton = textfont.render("QUIT TO MAIN MENU", True, BLACK, WHITE)
        if backtogame:
            playbutton = textfont.render("RETURN TO GAME", True, BLACK, WHITE)
            self.buttons = [Button(screen, self.dimensionX * 0.2, self.dimensionY/2 - 50, fullscreenbutton, self.togglefullscreen),
                            Button(screen, self.dimensionX  * 0.2, self.dimensionY/2, menubutton,
                                   self.tomainmenu),
                            Button(screen, self.dimensionX * 0.2, self.dimensionY/2 + 50, playbutton, self.leaveoptions)]
            self.selectedbutton = len(self.buttons) - 1
        else:
            self.buttons = [
                Button(screen, self.dimensionX * 0.2, self.dimensionY/2 - 25, fullscreenbutton, self.togglefullscreen),
                Button(screen, self.dimensionX * 0.2, self.dimensionY/2 + 25, menubutton,
                       self.leaveoptions)]
            self.selectedbutton = -1

    def togglefullscreen(self):
        if self.options["FULLSCREEN"]:
            self.screen = pygame.display.set_mode((960, 720))
        else:
            self.screen = pygame.display.set_mode((960, 720), FULLSCREEN)
        self.options["FULLSCREEN"] = not self.options["FULLSCREEN"]

    def leaveoptions(self):
        self.done = True
        self.nextstate = self.prevstate

    def tomainmenu(self):
        self.done = True
        self.nextstate = state_menu.Menu(self.screen, self.options)

    def main_loop(self):
        while not self.done:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.backgrd, (self.dimensionX * 0.4, -190))
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
                    if event.key == K_ESCAPE:
                        self.leaveoptions()
            pygame.display.flip()
        return self.nextstate
