import pygame
from pygame.locals import *

class Book:
    def __init__(self, screen, options, statein):
        self.done = False
        self.screen = screen
        self.dimensionX = screen.get_width()
        self.dimensionY = screen.get_height()
        self.options = options
        self.prevstate = statein
        self.page = pygame.Surface((self.dimensionX/2, self.dimensionY)).convert_alpha()
        self.page.fill((255, 255, 255))
        pygame.draw.line(self.page, (0, 0, 0), (0, 0), (0, self.dimensionY), 4)
        pygame.draw.line(self.page, (0, 0, 0), (self.dimensionX/2 - 2, 0), (self.dimensionX/2 - 2, self.dimensionY), 4)
        self.symbols = [pygame.transform.scale(pygame.image.load_extended('Assets/symbols/{}.png'.format(i)),
                                               (100, 100)).convert_alpha()
                        for i in range(1, 21)]
        self.textfont = pygame.font.Font('Assets/OpenSans-Regular.ttf', 30)
        titles = ["PostCodes 1", "PostCodes 2", "Island Map West", "Island Map East", "Current Jobs"]
        self.pages = [self.page.copy() for i in range(len(titles))]
        for i in range(len(self.pages)):
            self.pages[i].blit(self.textfont.render(titles[i], True, (0, 0, 0)), (10, 10))
            self.pages[i].blit(self.textfont.render("Pg. " + str(i + 1), True, (0, 0, 0)), (10, self.dimensionY - 45))
        for i in range(5):
            self.pages[0].blit(self.symbols[0], (10, 100 + i * 110))
            self.pages[0].blit(self.symbols[int(i % 5)], (110, 100 + i * 110))
            self.pages[1].blit(self.symbols[1], (10, 100 + i * 110))
            self.pages[1].blit(self.symbols[int((i + 5) % 5)], (110, 100 + i * 110))
        self.pageselector = 0
    
    def leavejournal(self):
        self.done = True
        self.nextstate = self.prevstate
    
    def main_loop(self):
        self.done = False
        while not self.done:
            self.screen.blit(self.pages[self.pageselector], (0, 0))
            self.screen.blit(self.pages[(self.pageselector + 1) % len(self.pages)], (self.dimensionX / 2, 0))
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == QUIT:
                    quit()
                if e.type == KEYDOWN:
                    if e.key in [K_ESCAPE, K_s]:
                        self.leavejournal()
                    if e.key == K_a:
                        self.pageselector -= 1
                    if e.key == K_d:
                        self.pageselector += 1
                    self.pageselector = min(max(self.pageselector, 0), len(self.pages) - 2)
        return self.nextstate
