import pygame
import main

screen = pygame.display.set_mode((640, 480))

mapstate = main.Game(screen)

state = mapstate

while True:
    state = state.main_loop()
        
