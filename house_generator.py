from math import sqrt
from random import randint
import random
import pygame
import time, numpy, pygame.mixer, pygame.sndarray

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


def generate_house_locations(housesprite, islecentrex, islecentrey, islerad, n_houses=20):
    min_house_dist = max(housesprite.get_width(), housesprite.get_height())
    list_houses = []
    for i in range(n_houses):
        #generate a house
        while True:
            loc = Point(random.randint(-islerad, islerad), random.randint(-islerad, islerad))
            if distance(Point(0, 0), loc) > islerad:
                print('out of circle')
                continue #out of the circle radius
            loc = Point(islecentrex + loc.x, islecentrey + loc.y)
            isclear = True
            for house in list_houses:
                if distance(loc, house) < min_house_dist:
                    print('too close')
                    isclear = False
                    break
                print(distance(loc, house))
            if isclear:
                list_houses.append(loc)
                break
    print(list_houses)
    return list_houses

def get_location_encoding(place):
        return [0, 3, 6]

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
	
	curr_offset = start
	notes = [start]
	for i in range(length):
		while True:
			step = random.choice([3, 5, 7])*random.choice([-1, 1])
			if len(notes) > 1 and (notes[-1] == notes[-2]) and step == 0:
				continue
			print(step)
			if abs(curr_offset + step) > 8:
				continue
			else:
				curr_offset = curr_offset + step
				notes.append(curr_offset + start)
				break
	#notes = [random.randint(-6, 7) for _ in range(length)]
	#return [note_names[n % 12]+str(3 if n < 0 else (5 if n == 12 else 4)) for n in notes]
	return [n+7 for n in notes]
def load_bird_noises():
	return [pygame.mixer.Sound("Assets\\Audio\\bird" + str(i) + ".wav") for i in range(16)]

if __name__ == "__main__":
	#generate_house_locations()
	#generate_IP_message(10)
	print(music_seq(6))

	#notes1 = NoteSeq(" ".join(music_seq(6)))
	#midi = Midi(1, tempo=90)
	#midi.seq_notes(notes1, track=0)
	#midi.write("demo.mid")

	# optional volume 0 to 1.0
	#music_file = "demo.mid"
	#pygame.mixer.music.set_volume(0.8)
	
	#try:
	#    play_music(music_file)
	#except KeyboardInterrupt:
	    # if user hits Ctrl/C then exit
	    # (works only in console mode)
	#    pygame.mixer.music.fadeout(1000)
	#    pygame.mixer.music.stop()
	#    raise SystemExit
	# choose a file and make a sound object
	freq = 44100    # audio CD quality
	bitsize = -16   # unsigned 16 bit
	channels = 2    # 1 is mono, 2 is stereo
	buffer = 1024    # number of samples
	pygame.mixer.init(freq, bitsize, channels, buffer)
	noises = load_bird_noises()
	seq = music_seq(8)
	for n in seq:
		print(n)
		noises[n].play()
		time.sleep(2)
	'''
	sound_file =  "bir2.wav"
	sound = pygame.mixer.Sound(sound_file)
	sound.play()
	time.sleep(1)

	# load the sound into an array
	snd_array = pygame.sndarray.array(sound)
	
	# resample. args: (target array, ratio, mode), outputs ratio * target array.
	# this outputs a bunch of garbage and I don't know why.
	sounds = []
	for i in range(23):
			snd_resample = resample(snd_array, int(42404*(2**((-i)/12)))).astype(np.int16, order='C')
			print('i')
			sounds = sounds + [pygame.sndarray.make_sound(snd_resample)]

	# take the resampled array, make it an object and stop playing after 2 seconds.
	for i in range(len(sounds)):
		snd = sounds[i]
		snd.play()
		time.sleep(1)
		sfile = wave.open('Assets\\Audio\\bird' + str(i) +'.wav', 'w')
		# sampling frequency (in Herz: the number of samples per second)
		SAMPLINGFREQ = 80000
		# the number of channels (1=mono, 2=stereo)
		NCHANNELS = 1

		# set the parameters
		sfile.setframerate(SAMPLINGFREQ)
		sfile.setnchannels(NCHANNELS)
		sfile.setsampwidth(2)

		# write raw PyGame sound buffer to wave file
		sfile.writeframesraw(snd.get_raw())

		# close file
		sfile.close()
	'''