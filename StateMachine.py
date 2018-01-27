import pygame
import state_menu
pygame.init()

screen = pygame.display.set_mode((640, 480))

menustate = state_menu.Menu(screen)

state = menustate

while True:
    state = state.main_loop()
