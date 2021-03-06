import pygame
from pygame.locals import *
import state_main, state_menu
from button import Button
import os


class EndScreen:
    def __init__(self, screen, options, victory, endtext="GOOD JOB, FINE AVIAN"):
        self.done = False
        self.nextstate = None
        self.screen = screen
        self.options = options
        print(options)
        self.dimensionX = screen.get_width()
        self.dimensionY = screen.get_height()
        self.victory = victory
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        textfont = pygame.font.Font(os.path.join('Assets','OpenSans-Regular.ttf'), 30)
        self.stamp = pygame.image.load_extended(os.path.join('Assets','Images','Bird standing.png'))  # Standin image
        self.scorestatement = [textfont.render(endtext, True, BLACK, WHITE),
                               textfont.render("{}/{} Symbols delivered correctly".format(self.options["CORRECT_SYM"],
                                                                                          self.options["TOTAL_SYM"]),
                                               True, BLACK, WHITE),
                               textfont.render("In a time of {:0.2f}".format(self.options["TIME"]), True, BLACK, WHITE),
                               textfont.render("FINAL SCORE: " + str(self.options["TOTAL"]), True, BLACK, WHITE)]
        # Standin for buttons as they come
        playbutton = textfont.render("PLAY AGAIN", True, BLACK, WHITE)
        menubutton = textfont.render("QUIT TO MENU", True, BLACK, WHITE)
        quitbutton = textfont.render("QUIT GAME", True, BLACK, WHITE)
        self.buttons = [Button(screen, int(self.dimensionX * 0.6), int(self.dimensionY*0.75 - 150), playbutton, self.startgame),
                        Button(screen, int(self.dimensionX * 0.6), int(self.dimensionY*0.75 - 100), menubutton, self.tomenu),
                        Button(screen, int(self.dimensionX * 0.6), int(self.dimensionY*0.75 - 50), quitbutton, quit)]
        self.selectedbutton = -1

    def startgame(self):
        self.nextstate = state_main.Game(self.screen, self.options)
        self.done = True

    def tomenu(self):
        self.nextstate = state_menu.Menu(self.screen, self.options)
        self.done = True

    def main_loop(self):
        while not self.done:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.stamp, (10, 10))
            for i, text in enumerate(self.scorestatement):
                self.screen.blit(text, (self.dimensionX * 0.45, 40 * (i + 5)))
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
        return self.nextstate
