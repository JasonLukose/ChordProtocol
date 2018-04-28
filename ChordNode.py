########################################
#
# Chord Node - Quick Chord Simulation
# Written By: Jason Lukose and Ganapathy Hari Narayan
#
########################################

class ChordNode:
	# Constructor
	def __init__(self, id, m):
		self.id = id
		self.successor = None
		self.predecessor = None
		self.finger_table = {}
		self.keys = []
		self.m = m

## FUNCTIONS OF NODE HERE
	def create(self):
		self.predecessor = None
		successor = self
		return None	

	def join(self, randNode):
		self.predecessor = None
		self.successor = randNode.find_successor(self.id)
		return None

	def stabilize(self):
		x = self.successor.predecessor
		if x.id > self.id and x.id < self.successor.id:
			self.successor = x
		self.successor.notify(self)
		return None

	def notify(self, notifyNode):
		if (self.predecessor == None or (notifyNode.id > self.predecessor.id and notifyNode.id < self.id)):
			self.predecessor = notifyNode

	def fix_fingers(self):
		return None

	def find_successor(self, id):
		## Node chosen is the correct node to store key in
		if (id == self.id):
			return self
		## end of the loop
		if (id > self.id and self.successor.id <= self.id):
			return self.successor
		if (id > self.id and id <= self.successor.id):
			return self.successor
		else:
			newNode = self.closest_predecessor(id);
			newNode.find_successor(id);
		return None

	def closest_predecessor(self, id):
		for i in range(0, self.m - 1):
			if (self.finger_table[m - i - 1].id >= self.id and 
				self.finger_table[m - i - 1].id < id):
				return self.finger_table[m - i - 1]
		return self


class ChordRing:
	m = 0
	nodeList = []
	@staticmethod
	def setM(m):
		ChordRing.m = m
	@staticmethod
	def getNodes():
		return ChordRing.nodeList
	@staticmethod
	def addNode(node):
		ChordRing.nodeList.append(node)

def main():
	print "hello";


if __name__ == "__main__": main()