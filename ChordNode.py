########################################
#
# Chord Node - Quick Chord Simulation
# Written By: Jason Lukose and Ganapathy Hari Narayan
#
########################################

import random

class ChordNode:
    # Constructor
    def __init__(self, id):
        self.id = id
        self.successor = None
        self.predecessor = None
        self.finger_table = {}
        self.keys = []

## FUNCTIONS OF NODE HERE
    def create(self):
        self.predecessor = None
        self.successor = self
        return None 

    def join(self, randNode):
        self.predecessor = None
        print("JOINING NODE IS" + self.id + "RAND NODE IS " + randNode.id)
        self.successor = randNode.find_successor(self.id)
        print("Sucessor is now " + self.successor.id + "\n")
        return None

    def stabilize(self):
        print("STABILIZING NODE " + self.id)
        
        x = self.successor.predecessor
        if x != None:
            print("BEFORE: " + self.id + " " + x.id)
        if x != None and x.id > self.successor.id and x != self:
            self.successor = x
        if x != None and x.id > self.id and x.id <= self.successor.id:
            self.successor = x
        self.successor.notify(self)

    def notify(self, notifyNode):
        if notifyNode.id > notifyNode.successor.id:
            self.predecessor = notifyNode
        elif (self.predecessor == None or (notifyNode.id > self.predecessor.id and notifyNode.id < self.id)):
            self.predecessor = notifyNode

        print("Stab node's successor is " + notifyNode.successor.id)
        if notifyNode.predecessor != None:
            print("Stab node's predecessor is " + notifyNode.predecessor.id)
        else:
            print("Stab node's predecessor is None")


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
        for i in range(0, ChordRing.m - 1):
            if (self.finger_table[m - i - 1].id >= self.id and 
                self.finger_table[m - i - 1].id < id):
                return self.finger_table[m - i - 1]
        return self
    def insertKey(self, id):
        return None


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
    @staticmethod
    def getNumNodes():
        return len(ChordRing.nodeList)

def readLog():
    f = open("log_file.txt", "r")
    print(ChordRing.m)
    for line in f:
        command = line.rstrip().split(" ")
        if command[0] == "CREATE_NODE":
            node = ChordNode(command[1])
            node.create()
            ChordRing.addNode(node)
        elif command[0] == "INSERT_NODE":
            node = ChordNode(command[1])
            node.join(ChordRing.getNodes()[random.randint(0, ChordRing.getNumNodes() - 1)])
            ChordRing.addNode(node)
        elif command[0] == "INSERT_KEY":
            return None
        else:
            return None

        for node in ChordRing.getNodes():
            node.stabilize()

        for node in ChordRing.getNodes():
            node.stabilize()

    ## 23 -> 28 -> 45 -> 23
    for node in ChordRing.getNodes():
        print(node.predecessor.id + " -> " + node.id + " -> " + node.successor.id)


if __name__ == "__main__":
    readLog()
