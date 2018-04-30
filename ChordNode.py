##############################################################
#                                                            #
#           Chord Node - Quick Chord Simulation              #
#     Written By: Jason Lukose and Ganapathy Hari Narayan    #
#                                                            #
##############################################################

import random
import math

def keyInRange(kCheck, b1, b2):
    if (b2 > b1):
        if (kCheck > b1 and kCheck < b2):
            return True
    else:
        if (kCheck > b1 or kCheck < b2):
            return True
    return False
######################################################################################

##
## Entry Point for Successor Chord Ring
##

def successorOrderedChordRing(node):
    if (node == None):
        return "ChordRing is empty!"
    else:
        orderedList = []
        orderedList = orderedList + [node.id]
        orderedList = orderedList + appendSuccessor(node, node.successor)

    return orderedList

##
## Helper function to append the successor
##

def appendSuccessor(originalNode, currentNode):

    if (originalNode == currentNode):
        return [originalNode.id]
    else:
        return [currentNode.id] + appendSuccessor(originalNode, currentNode.successor)

    return None

##
## Entry Point for Predecessor Chord Ring
##

def predecessorOrderedChordRing(node):
    if (node == None):
        return "ChordRing is empty!"
    else:
        orderedList = []
        orderedList = orderedList + [node.id]
        orderedList = orderedList + appendPredecessor(node, node.predecessor)

    return orderedList

##
## Helper function to append the predecessor
##

def appendPredecessor(originalNode, currentNode):

    if (currentNode == None):
        return [None]
    if (originalNode == currentNode):
        return [originalNode.id]
    else:
        return [currentNode.id] + appendPredecessor(originalNode, currentNode.predecessor)

    return None

##
## Helper function to find Min Node of a Chord Ring
##

def findMinNode():
    minNode = None

    for node in ChordRing.getNodes():
        if minNode == None:
            minNode = node
        else:
            if node.id < minNode.id:
                minNode = node

    return minNode

######################################################################################

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
        self.reset_finger_table()

    def join(self, randNode):
        self.predecessor = None
        self.successor = randNode.find_successor(self.id)
        self.reset_finger_table()
        indToRm = []
        for i in range(0, len(self.successor.keys)):
            if self.successor.keys[i].id <= self.id:
                indToRm.append(i)
                self.keys.append(self.successor.keys[i])
        for i in indToRm:
            del self.successor.keys[i]
        return None

    def printFingerTable(self):
        for key, value in self.finger_table.items():
            print("Finger " + str(key) + " Value " + str(value.id))

    def printKeys(self):
        print("Keys for id: " + str(self.id))
        for k in self.keys:
            print(k.id)

    def printSuccPred(self):
        print(str(self.predecessor.id) + " -> " + str(self.id) + " -> " + str(self.successor.id))

    def stabilize(self):
        x = self.successor.predecessor
        if x != None:
            if self == self.successor or keyInRange(x.id, self.id, self.successor.id):
                self.successor = x
        self.successor.notify(self)

    def notify(self, notifyNode):
        if (self.predecessor == None or (notifyNode.id != self.predecessor)):
            if self != notifyNode:
                self.predecessor = notifyNode


    def reset_finger_table(self):
        for i in range(0, ChordRing.m):
            self.finger_table[i] = self.successor

    def fix_fingers(self):
        self.reset_finger_table()
        for i in range(0, ChordRing.m):
            succ = (self.id + (1 << i)) % (1 << ChordRing.m)
            self.finger_table[i] = self.find_successor(succ)

    def find_successor(self, id):
        if (id == self.id):
            return self
        if (self == self.successor):
            return self
        if (id < self.successor.id and self.successor.id <= self.id):
            return self.successor
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

    def insertKey(self, key):
        succ = self.find_successor(key.id)
        succ.keys.append(key)


class Key:
    def __init__(self, id):
        self.id = id

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
            # node.stabilize()
            # node.fix_fingers() 
            ChordRing.addNode(node)
        elif command[0] == "INSERT_NODE":
            node = ChordNode(id)
            node.join(ChordRing.getNodes()[random.randint(0, ChordRing.getNumNodes() - 1)])
            ChordRing.addNode(node)
            # node.stabilize()
            # node.fix_fingers() 
        elif command[0] == "INSERT_KEY":
            k = Key(id)
            node = ChordRing.getNodes()[random.randint(0, ChordRing.getNumNodes() - 1)]
            node.insertKey(k)
        else:
            pass
    
    flag = True
    i = 0
    while ( flag and ChordRing.getNumNodes() > 1 ):
        i = i+1
        r = list(range(ChordRing.getNumNodes()))
        random.shuffle(r)
        newR = r[0: int(math.ceil(ChordRing.getNumNodes()/2))]
        for j in newR:
            ChordRing.getNodes()[j].stabilize()

        random.shuffle(r)
        newR = r[0: int(math.ceil(ChordRing.getNumNodes()/2))]
        for k in newR:
            ChordRing.getNodes()[j].fix_fingers()

        flag = False
        for node in ChordRing.getNodes():
            if node.predecessor != None and node.successor != None:
                pass
            else:
                flag = True

    print ("Number of iterations to stabilize: " + str(i))
    for node in ChordRing.getNodes():
        # node.printSuccPred()
        node.printFingerTable()
        node.printKeys()

    print("Successor Ring : " + str(successorOrderedChordRing(findMinNode())) )
    print("Predecessor Ring : " + str(predecessorOrderedChordRing(findMinNode())) ) 



if __name__ == "__main__":
    readLog()
