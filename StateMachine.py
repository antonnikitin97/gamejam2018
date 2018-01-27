import pygame
import main, menu
pygame.init()

screen = pygame.display.set_mode((640, 480))

menustate = menu.Menu(screen)
mapstate = main.Game(screen)

state = menustate

while True:
    state = state.main_loop()
        
