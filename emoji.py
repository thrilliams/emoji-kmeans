from math import sqrt
from random import uniform
from sys import argv

class Point:
	def __init__(self, d):
		self.name = d[0]
		self.vector = [float(d[i]) for i in range(1, len(d))]
		self.parent = None
	def __repr__(self):
		return "{}: {}".format(self.name, self.vector)
	def dist(self, p):
		v = 0
		for i in range(len(self.vector)):
			v += (self.vector[i] - p.vector[i]) ** 2
		return sqrt(v)
	def findParent(self, crosses):
		if self.parent:
			self.parent.children.remove(self)
		d = []
		for i in crosses:
			d.append(self.dist(i))
		self.parent = crosses[d.index(min(d))]
		self.parent.children.append(self)

class Cross(Point):
	def __init__(self, n):
		self.name = n
		self.vector = [uniform(-0.5, 0.5) for _ in range(300)]
		self.children = []
	def __repr__(self):
		return "Group {}\nChildren: {}".format(self.name, "".join([lookup[i.name[4::]] for i in self.children]))
	def move(self):
		p = [0] * 300
		for i in range(len(p)):
			for e in self.children:
				p[i] += e.vector[i]
			p[i] /= len(self.children)
		self.vector = p

points = []
crosses = [Cross(i) for i in range(10)]

file_object = open("emoji.txt", "r")
data = file_object.read().split("\n")[1:]
for e in data:
	d = e.split()
	points.append(Point(d))
file_object.close()

file_object = open("emoji_lookup.tsv", "r")
data = file_object.read().split("\n")
lookup = {}
for i in data:
	i = i.split("\t")
	lookup[i[0]] = i[1]
file_object.close()

def iterate(n=1):
	for j in range(n):
		print('Loop ' + str(j + 1))
		for i in points:
			i.findParent(crosses)
		for i in crosses:
			i.move()

if len(argv) > 1:
	iterate(int(argv[1]))
else:
	iterate(100)
print("\n\n".join([i.__repr__() for i in crosses]))