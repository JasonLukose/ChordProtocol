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
        self.isEnd = False
        self.keys = []

## FUNCTIONS OF NODE HERE
    def create(self):
        self.predecessor = None
        self.successor = self
        return None 

    def join(self, randNode):
        self.predecessor = None
        print("JOINING NODE IS" + str(self.id) + "RAND NODE IS " + str(randNode.id))
        self.successor = randNode.find_successor(self.id)
        self.reset_finger_table()
        print("Sucessor is now " + str(self.successor.id) + "\n")
        return None

    def printFingerTable(self):
        for key in self.finger_table:
            print(self.finger_table[key].id)

    def stabilize(self):
        # print("STABILIZING NODE " + str(self.id))
        
        x = self.successor.predecessor
        if x != None:
            if self == self.successor or (x.id > self.id and x.id < self.successor.id):
                self.successor = x
        self.successor.notify(self)

    def notify(self, notifyNode):
        if self.id < notifyNode.id:
            self.predecessor = notifyNode

        if (self.predecessor == None or (notifyNode.id > self.predecessor.id and notifyNode.id < self.id)):
            if self != notifyNode:
                self.predecessor = notifyNode

        # print("Stab node's successor is " + str(notifyNode.successor.id))
        # if notifyNode.predecessor != None:
        #     print("Stab node's predecessor is " + str(notifyNode.predecessor.id))
        # else:
        #     print("Stab node's predecessor is None")


    def reset_finger_table(self):
        for i in range(0, ChordRing.m):
            self.finger_table[i] = self.successor
    def fix_fingers(self):
        self.reset_finger_table()
        for i in range(0, ChordRing.m):
            print("FIXING NODE" + str(self.id) + " FINGER TABLE ENTRY" + str(i))
            self.finger_table[i] = self.find_successor(self.id + (1 << i))

    def find_successor(self, id):
        ## Node chosen is the correct node to store key in
        print(str(id) + " " + str(self.id) + " " + str(self.successor.id))
        boo = False
        # print(self.printFingerTable())
        if (id == self.id):
            return self
        if (self == self.successor):
            return self
        if (id > self.id and self.successor.id <= self.id):
            return self.successor
        if (id > self.id and id <= self.successor.id):
            return self.successor
        else:
            newNode = self.closest_predecessor(id);
            if newNode == self:
                return newNode.successor.find_successor(id)
            else:
                return newNode.find_successor(id);

    def closest_predecessor(self, id):
        for i in range(ChordRing.m - 1, -1, -1):
            if (self.finger_table[i].id >= self.id and self.finger_table[i].id < id):
                return self.finger_table[i]
        return self
    def insertKey(self, id):
        return None


class ChordRing:
    m = 4
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
    ChordRing.setM(6)
    for line in f:
        command = line.rstrip().split(" ")
        id = int(command[1])
        if command[0] == "CREATE_NODE":
            node = ChordNode(id)
            node.create()
            ChordRing.addNode(node)
        elif command[0] == "INSERT_NODE":
            print("YO YO " + str(id))
            node = ChordNode(id)
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
        for node in ChordRing.getNodes():
            print("FIXING FINGER FOR NODE" + str(node.id))
            node.fix_fingers()

    # 23 -> 28 -> 45 -> 23
    for node in ChordRing.getNodes():
        print(str(node.predecessor.id) + " -> " + str(node.id) + " -> " + str(node.successor.id))


if __name__ == "__main__":
    readLog()
