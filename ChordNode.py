##############################################################
#                                                            #
#           Chord Node - Quick Chord Simulation              #
#     Written By: Jason Lukose and Ganapathy Hari Narayan    #
#                                                            #
##############################################################

import random
import math
import sys

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
                indToRm.append(self.successor.keys[i])
                self.keys.append(self.successor.keys[i])
        for i in indToRm:
            self.successor.keys.remove(i)
        return None

    def printFingerTable(self):
        print("Finger table for ID IS: " + str(self.id))
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

    def leave(self):
        if (self.predecessor != None):
            self.predecessor.successor = self.successor
        self.successor.predecessor = None
        self.successor.receiveKeys(self.keys)

    def closest_predecessor(self, id):
        for i in range(ChordRing.m - 1, -1, -1):
            if (self.finger_table[i].id >= self.id and self.finger_table[i].id < id):
                return self.finger_table[i]
        return self

    def insertKey(self, key):
        succ = self.find_successor(key.id)
        succ.keys.append(key)

    def receiveKeys(self, predecessorKeys):
        for key in predecessorKeys:
            self.keys.append(key)

    def containsKey(self, key):
        for k in self.keys:
            if k.id == key.id:
                return True
        return False

    def lookup(self, lookupKey):
        succ = self.find_successor(lookupKey.id)
        for key in succ.keys:
            if (key.id == lookupKey.id):
                return (True, succ.id)
        return (False, None)


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

def ringStabilise():
    flag = True
    i = 0
    while ( flag and ChordRing.getNumNodes() > 1 ):
        i = i+1
        r = list(range(ChordRing.getNumNodes()))
        random.shuffle(r)
        newR = r[0: int(math.ceil(ChordRing.getNumNodes()))]
        for j in newR:
            ChordRing.getNodes()[j].stabilize()

        random.shuffle(r)
        newR = r[0: int(math.ceil(ChordRing.getNumNodes()))]
        for k in newR:
            ChordRing.getNodes()[k].fix_fingers()

        flag = False
        for node in ChordRing.getNodes():
            if node.predecessor != None and node.successor != None:
                pass
            else:
                flag = True

def readLog():
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = "log_file.txt"
        
    f = open(file, "r")
    ChordRing.setM(6)
    # stabilizeRing()
    for line in f:
        command = line.rstrip().split(" ")
        id = int(command[1])
        if command[0] == "CREATE_NODE":
            node = ChordNode(id)
            node.create()
            ChordRing.addNode(node)
        elif command[0] == "INSERT_NODE":
            node = ChordNode(id)
            node.join(ChordRing.getNodes()[random.randint(0, ChordRing.getNumNodes() - 1)])
            node.stabilize()
            node.fix_fingers()
            # for n in ChordRing.getNodes():
            #     n.stabilize()
            #     n.fix_fingers()
            ChordRing.addNode(node)
            
        elif command[0] == "INSERT_KEY":
            k = Key(id)
            node = ChordRing.getNodes()[random.randint(0, ChordRing.getNumNodes() - 1)]
            ringStabilise()
            node.insertKey(k)

        elif command[0] == "LEAVE_NODE":
            currNode = None
            for node in ChordRing.getNodes():
                if node.id == id:
                    currNode = node
            if currNode != None:
                ringStabilise()
                currNode.leave()
                ChordRing.getNodes().remove(currNode)
                # for n in ChordRing.getNodes():
                #     n.stabilize()
                #     n.fix_fingers()

        else:
            pass


    ringStabilise()

    for node in ChordRing.getNodes():
        node.printFingerTable()
        node.printKeys()

    print("Successor Ring : " + str(successorOrderedChordRing(findMinNode())) )
    print("Predecessor Ring : " + str(predecessorOrderedChordRing(findMinNode())) )
    if ChordRing.getNumNodes() >= 1:
        findKeysList = [17, 14, 1, 13, 12]
        for key in findKeysList:
            print("Finding key: " + str(key))
            node = ChordRing.getNodes()[random.randint(0, ChordRing.getNumNodes() - 1)]
            keyExists, nodeID = node.lookup(Key(key))
            print(str(keyExists) + " " + str(nodeID) )



# def stabilizeRing():
#     print(time.ctime())
#     flag = False
#     for node in ChordRing.getNodes():
#         if node.successor != None and node.predecessor != None:
#             pass
#         else:
#             flag = True
#         node.stabilize()
#         node.fix_fingers()
#     if flag == False and mainFlag == True:
#         pass
#     else:
#         threading.Timer(0.05, stabilizeRing).start()


if __name__ == "__main__":
    readLog()
