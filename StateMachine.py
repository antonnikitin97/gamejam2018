import pygame
import state_menu, state_main


def run():
	pygame.init()

	screen = pygame.display.set_mode((960, 720))

	menustate = state_main.Game(screen)

	state = menustate
	while True:
		state = state.main_loop()

run()
