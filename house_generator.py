from math import sqrt
import random

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

def generate_house_locations():
	list_houses = []
	iter_num = 0
	for i in range(n_houses):
		#generate a house
		while iter_num < 1000:
			iter_num += 1
			loc = Point(random.random()*island_radius, random.random()*island_radius)
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

if __name__ == "__main__":
	generate_house_locations()