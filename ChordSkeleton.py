##############################################################
#                                                            #
#           Chord Node - Quick Chord Simulation              #
#     Written By: Jason Lukose and Ganapathy Hari Narayan    #
#                                                            #
##############################################################

import random
import math

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

##############################################################
#                                                            #
#                   NO CODE ABOVE THIS BOX                   #
#                                                            #
##############################################################

class ChordNode:
    # Constructor
    def __init__(self, id):
        self.id = id
        self.successor = None
        self.predecessor = None
        self.finger_table = {}
        self.isEnd = False
        self.keys = []

    def printFingerTable(self):
        for key, value in self.finger_table.items():
            print("Key " + str(key) + " Value " + str(value.id))

    def printKeys(self):
        print("Keys for id: " + str(self.id))
        for k in self.keys:
            print("Key is " + str(k.id))

    def printSuccPred(self):
        print(str(self.predecessor.id) + " -> " + str(self.id) + " -> " + str(self.successor.id))

    ## A function that creates the node ring with the node that calls this function
    def create(self):
        return None

    ## A function that allows a node to join the ring. The node that calls the function joins 
    ## the ring
    ## randNode: is a random node out of all the nodes in your ChordRing
    def join(self, randNode):
        return None

    ## A function that stabilizes the node that calls it
    def stabilize(self):
        return None

    ## A function that notifies the node that calls the function
    ## notifyNode: is the node that notifies the node that called the function
    def notify(self, notifyNode):
        return None

    ## Resets the finger table to make all the node's entries the successor
    def reset_finger_table(self):
        for i in range(0, ChordRing.m):
            self.finger_table[i] = self.successor

    ## Walks through the finger table for a node and fixes each entry to the correct node
    ## in the Chord ring
    def fix_fingers(self):
        return None

    ## finds the successor of a specific id in the Chord ring
    ## Uses the node that calls this to find the successor of the id in the parameter
    ## id: the id to the find the successor for
    def find_successor(self, id):
        return None

    ## Given an id, finds the closest predecessor node of that id
    ## id: the id to find the closest predecessor node
    def closest_predecessor(self, id):
        return None

    ## Inserts a key into the correct node
    def insertKey(self, key):
        return None


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

        ## What happens when the log file is creating a node
        if command[0] == "CREATE_NODE":
            node = ChordNode(id)
            ### FILL IN YOUR CODE#####

            ##########################
            ChordRing.addNode(node)

        ## What happens when the log file wants to insert a node
        elif command[0] == "INSERT_NODE":
            node = ChordNode(id)
            randNode = ChordRing.getNodes()[random.randint(0, ChordRing.getNumNodes() - 1)]
            ### FILL IN YOUR CODE#####

            ##########################
            ChordRing.addNode(node)

        ## What happens when log file wants to insert a key
        elif command[0] == "INSERT_KEY":
            k = Key(id)
            ### FILL IN YOUR CODE#####

            ##########################

    ### Prints out the final chord ring according to final structure:
    ### node.predecessor -> node -> node.successor
    ### Prints the finger table according to following structure:
    ### Key "id" Value "nodeId"
    ### Prints the keys within each node according to the following structure:
    ### Key is "keyId"...
    for node in ChordRing.getNodes():
        node.printSuccPred()
        node.printFingerTable()
        node.printKeys()



if __name__ == "__main__":
    readLog()
