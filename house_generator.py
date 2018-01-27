from math import sqrt
from random import randint
import random
from pyknon.genmidi import Midi
from pyknon.music import NoteSeq
import pygame
import time, numpy, pygame.mixer, pygame.sndarray
from scipy.signal import resample
import numpy as np

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

p1 = Point(10, 3)
p2 = Point(1, 0)


def distance(a, b):
    return sqrt((a.x-b.x)**2+(a.y-b.y)**2)

island_radius = 5000
n_houses = 20
min_house_dist = 200

def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(50)


def generate_house_locations():
	list_houses = []
	iter_num = 0
	for i in range(n_houses):
		#generate a house
		while iter_num < 1000:
			iter_num += 1
			loc = Point(random.randint(0, island_radius), random.randint(0, island_radius))
			if (loc.x - island_radius/2)**2 + (loc.y- island_radius/2)**2 > island_radius**2:
				print('out of circle')
				continue #out of the circle radius
			for house in list_houses:
				if distance(loc, house) < min_house_dist:
					print('too close')
					continue
			list_houses.append(loc)
			print('it worked')
			break
	print(list_houses)
	return list_houses

def get_location_encoding(place):
		return 0 #TODO

#protocol:
#header consisting of 0, 0
#location consisting of 3 parts
#message consisting of len parts
#end of message consisting of 0, 0
def generate_IP_message(len, to):
	return [0, 0] + get_location_encoding(to) + [int(random.random()*12) for _ in range(len+3)] + [0, 0]

def music_seq(length):
	#start on a random note
	#A-G = 0-7
	note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
	start = random.randint(0, 12)
	start_offset = 0
	
	curr_offset = start_offset
	notes = [start]
	for i in range(length):
		while True:
			step = random.choice([3, 5, 7])*random.choice([-1, 1])
			if len(notes) > 1 and (notes[-1] == notes[-2]) and step == 0:
				continue
			print(step)
			if abs(curr_offset + step) > 12:
				continue
			else:
				curr_offset = curr_offset + step
				notes.append(curr_offset + start)
				break
	#notes = [random.randint(-6, 7) for _ in range(length)]
	return [note_names[n % 12]+str(3 if n < 0 else (5 if n == 12 else 4)) for n in notes]

if __name__ == "__main__":
	#generate_house_locations()
	#generate_IP_message(10)
	print(music_seq(6))
	notes1 = NoteSeq(" ".join(music_seq(6)))
	midi = Midi(1, tempo=90)
	midi.seq_notes(notes1, track=0)
	midi.write("demo.mid")
	freq = 44100    # audio CD quality
	bitsize = -16   # unsigned 16 bit
	channels = 2    # 1 is mono, 2 is stereo
	buffer = 1024    # number of samples
	pygame.mixer.init(freq, bitsize, channels, buffer)
	# optional volume 0 to 1.0
	music_file = "demo.mid"
	pygame.mixer.music.set_volume(0.8)
	'''
	try:
	    play_music(music_file)
	except KeyboardInterrupt:
	    # if user hits Ctrl/C then exit
	    # (works only in console mode)
	    pygame.mixer.music.fadeout(1000)
	    pygame.mixer.music.stop()
	    raise SystemExit
	'''
	# choose a file and make a sound object
	sound_file = "bir2.wav"
	sound = pygame.mixer.Sound(sound_file)

	# load the sound into an array
	snd_array = pygame.sndarray.array(sound)

	# resample. args: (target array, ratio, mode), outputs ratio * target array.
	# this outputs a bunch of garbage and I don't know why.
	sounds = []
	for i in range(12):
			snd_resample = resample(snd_array, int(42404*(2**(i/12)))).astype(np.int16, order='C')
			sounds = sounds + [pygame.sndarray.make_sound(snd_resample)]

	# take the resampled array, make it an object and stop playing after 2 seconds.
	for snd in sounds:
			snd.play()
			time.sleep(2)