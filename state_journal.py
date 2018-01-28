import pygame
import os
from pygame.locals import *

class Book:
    def __init__(self, screen, options, statein, map, houses, player):
        self.done = False
        self.screen = screen
        self.player = player
        self.dimensionX = screen.get_width()
        self.dimensionY = screen.get_height()
        self.textfont = pygame.font.Font(os.path.join('Assets','OpenSans-Regular.ttf'), 30)
        self.bigfont = pygame.font.Font(os.path.join('Assets','OpenSans-Regular.ttf'), 200)
        self.map = map.copy()
        self.houses = houses
        for i, house in enumerate(self.houses):
            pygame.draw.circle(self.map, (0, 0, 0),
                               (int(house.worldX + house.visual.width/2), int(house.worldY + house.visual.height/2)),
                               300)
            number = self.bigfont.render(str(i), True, (255, 255, 255)).convert_alpha()
            self.map.blit(number, (house.worldX + (house.visual.width - number.get_width())/2,
                                   house.worldY + (house.visual.height - number.get_height())/2))
        self.options = options
        self.prevstate = statein
        self.page = pygame.Surface((self.dimensionX/2, self.dimensionY)).convert_alpha()
        self.page.fill((255, 255, 255))
        pygame.draw.line(self.page, (0, 0, 0), (0, 0), (0, self.dimensionY), 4)
        pygame.draw.line(self.page, (0, 0, 0), (self.dimensionX/2 - 2, 0), (self.dimensionX/2 - 2, self.dimensionY), 4)
        self.symbols = [pygame.image.load_extended(os.path.join('Assets','symbols/{}.png'.format(i))) for i in range(1, 21)]
        self.bigsymbols = [pygame.transform.scale(symbol, (100, 100)).convert_alpha() for symbol in self.symbols]
        self.smallsymbols = [pygame.transform.scale(symbol, (50, 50)).convert_alpha() for symbol in self.symbols]
        titles = ["PostCodes 1", "PostCodes 2", "Island Map West", "Island Map East", "Current Jobs"]
        self.pages = [self.page.copy() for i in range(len(titles))]
        for i in range(5):
            self.pages[0].blit(self.bigsymbols[0], (10, 100 + i * 110))
            self.pages[0].blit(self.bigsymbols[int(i % 5)], (110, 100 + i * 110))
            self.pages[0].blit(self.textfont.render("House " + str(i), True, (0, 0, 0)), (210, 100 + i * 110))
            self.pages[1].blit(self.bigsymbols[1], (10, 100 + i * 110))
            self.pages[1].blit(self.bigsymbols[int((i + 5) % 5)], (110, 100 + i * 110))
            self.pages[1].blit(self.textfont.render("House " + str(i + 5), True, (0, 0, 0)), (210, 100 + i * 110))
        westmap = pygame.transform.scale(self.map.subsurface((0, 0, self.map.get_width()/2, self.map.get_height())),
                                                  (int(self.map.get_width()/20), int(self.map.get_height()/10))).convert_alpha()
        eastmap = pygame.transform.scale(self.map.subsurface((self.map.get_width() / 2, 0, self.map.get_width() / 2, self.map.get_height())),
                                                  (int(self.map.get_width() / 20), int(self.map.get_height()/10))).convert_alpha()
        self.pages[2].blit(westmap, (self.dimensionX/2 - westmap.get_width() - 5, 50))
        self.pages[3].blit(eastmap, (5, 50))
        #print(self.player.current_transmissions)
        pygame.draw.line(self.pages[4], (0, 0, 0), (130, 0), (130, self.dimensionY))
        for i, transmission in enumerate(self.player.current_transmissions):
            id = transmission[0]
            self.pages[4].blit(self.smallsymbols[int((id - (id % 5)) / 5)], (10, 150 + i * 60))
            self.pages[4].blit(self.smallsymbols[int(id % 5)], (65, 150 + i * 60))
            for j, no in enumerate(transmission[1]):
                self.pages[4].blit(self.smallsymbols[no], (150 + j * 55, 150 + i * 60))
        for i in range(len(self.pages)):
            self.pages[i].blit(self.textfont.render(titles[i], True, (0, 0, 0), (255, 255, 255)), (10, 10))
            self.pages[i].blit(self.textfont.render("Pg. " + str(i + 1), True, (0, 0, 0), (255, 255, 255)), (10, self.dimensionY - 45))
        self.pageselector = 0
        self.pagebckgrd = pygame.Surface((self.dimensionX, self.dimensionY))
        self.pagebckgrd.fill((255, 255, 255))
        leftpage = pygame.transform.scale(pygame.image.load_extended(os.path.join('Assets','Images','Page 1.png')),
                                          (int(self.dimensionX/2), self.dimensionY))
        rightpage = pygame.transform.scale(pygame.image.load_extended(os.path.join('Assets','Images','Page 2.png')),
                                           (int(self.dimensionX / 2), self.dimensionY))
        self.pagebckgrd.blit(leftpage, (self.dimensionX/2 - leftpage.get_width(), 0))
        self.pagebckgrd.blit(rightpage, (self.dimensionX / 2, 0))
        self.pagebckgrd = self.pagebckgrd.convert_alpha()

    def leavejournal(self):
        self.done = True
        self.nextstate = self.prevstate

    def main_loop(self):
        self.done = False
        while not self.done:
            self.screen.blit(self.pagebckgrd, (0, 0))
            leftpage = self.pages[self.pageselector]
            rightpage = self.pages[(self.pageselector + 1) % len(self.pages)]
            self.screen.blit(pygame.transform.scale(leftpage, (leftpage.get_width() - 200, leftpage.get_height() - 100)),
                             (100, 100))
            self.screen.blit(pygame.transform.scale(rightpage, (rightpage.get_width() - 200, rightpage.get_height() - 100)),
                             (self.dimensionX / 2 + 100, 100))
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == QUIT:
                    quit()
                if e.type == KEYDOWN:
                    if e.key in [K_ESCAPE, K_j]:
                        self.leavejournal()
                    if e.key == K_LEFT:
                        self.pageselector -= 1
                    if e.key == K_RIGHT:
                        self.pageselector += 1
                    self.pageselector = min(max(self.pageselector, 0), len(self.pages) - 2)
        return self.nextstate

"""I think Anton is the best and he should be given many doggos
~ S T A Y  I N S P I R E D ~"""
