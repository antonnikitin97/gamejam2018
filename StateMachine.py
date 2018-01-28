import pygame
import state_menu, state_main
from pygame.locals import *
from state_main import *

screen = None

def fadeout():
	DONE = False
	alphaSurface = pygame.Surface((960,720)) # The custom-surface of the size of the screen.
	alphaSurface.fill((255,255,255)) # Fill it with whole white before the main-loop.
	alphaSurface.set_alpha(0) # Set alpha to 0 before the main-loop. 
	alph = 0 # The increment-variable.
	while not DONE:
		alph += 0.1 # Increment alpha by a really small value (To make it slower, try 0.01)
		alphaSurface.set_alpha(alph) # Set the incremented alpha-value to the custom surface.
		screen.blit(alphaSurface,(0,0)) # Blit it to the screen-surface (Make them separate)
		# Trivial pygame stuff.
		if pygame.key.get_pressed()[K_ESCAPE]:
			DONE = True
		for ev in pygame.event.get():
			if ev.type == QUIT:
				DONE = True
		#print(alph)
		if alph > 10:
			break
		pygame.display.flip() # Flip the whole screen at each frame.

def run():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((960, 720))
    initialoptions = {"FULLSCREEN": False,
                      "SOUND": True,
                      "TOTAL": 0,     # number of packets given
                      "DELIVERED": 0, # number delivered correctly
                      "TIME": 0,
                      "WRONG" : 0}      # time taken to do so
    menustate = state_menu.Menu(screen, initialoptions)
    state = menustate
    while True:
        state = state.main_loop()
        fadeout()

run()
