import pygame
from pygame.locals import *
import state_main, state_house, state_options, state_instr
from button import Button

class Menu:
    def __init__(self, screen, options):
        self.done = False
        self.nextstate = None
        self.screen = screen
        self.options = options
        self.dimensionX = screen.get_width()
        self.dimensionY = screen.get_height()
        self.gamestate = None
        self.game = None
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        textfont = pygame.font.Font('Assets\OpenSans-Regular.ttf', 30)
        # Standin for buttons as they come
        playbutton = textfont.render("PLAY", True, BLACK, WHITE)
        instrbutton = textfont.render("INSTRUCTIONS", True, BLACK, WHITE)
        optionsbutton = textfont.render("OPTIONS", True, BLACK, WHITE)
        quitbutton = textfont.render("QUIT", True, BLACK, WHITE)
        self.buttons = [Button(screen, self.dimensionX / 2, self.dimensionY/2 - 100, playbutton, self.startgame),
                        Button(screen, self.dimensionX / 2, self.dimensionY/2 - 50, instrbutton, self.instructions),
                        Button(screen, self.dimensionX / 2, self.dimensionY/2, optionsbutton, self.enteroptions),
                        Button(screen, self.dimensionX / 2, self.dimensionY/2 + 50, quitbutton, quit)]
        self.selectedbutton = 0
    def load_game(self):
        self.game = state_main.Game(self.screen, self.options)
    def startgame(self):
        self.screen.blit(pygame.font.Font('Assets\OpenSans-Regular.ttf', 30).render('Loading...', True, (0,0,0), (255, 255, 255)), (400, 600))
        pygame.display.flip()
        self.load_game()
        self.nextstate = self.game
        self.done = True
    
    def enteroptions(self):
        self.nextstate = state_options.Menu(self.screen, self.options, self, False)
        self.done = True
    def instructions(self):
        self.nextstate = state_instr.Instr(self.screen, self)
        self.done = True
    
    def main_loop(self):
        self.done = False
        while not self.done:
            self.screen.fill((255, 255, 255))
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
                        quit()
            pygame.display.flip()
        return self.nextstate
