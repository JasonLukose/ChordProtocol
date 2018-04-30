########################################
#
# Chord Node - Quick Chord Simulation
# Written By: Jason Lukose and Ganapathy Hari Narayan
#
########################################

import random

def key_in_range(check, bound1, bound2, half):
    if (bound1 > bound2):
        if (half):
            if (check <= bound2 or check > bound1):
                return True
        else:
            if ( check < bound2 or check > bound1):
                return True
    else:
        if (half):
            if ( check > bound1 and check <= bound2 ):
                return True
        else:
            if (check > bound1 and check < bound2):
                return True
    return False

class ChordNode:
    # Constructor
    def __init__(self, id):
        self.id = id
        self.successor = None
        self.predecessor = None
        self.finger_table = {}
        self.keys = []
        self.successorListSize = 4
        self.successors = [0] * self.successorListSize


    def create(self):
        self.predecessor = None
        self.successor = self

    def join(self, existingNode):
        self.predecessor = None
        self.successor = existingNode.find_successor(self.id)

    def stabilize(self):
        successor = self.successor
        x = self.successor.predecessor
        i = 0

      #  while( successor != None and i < self.successorListSize ):
       #     self.successors[i] = successor
        #    successor = successor.successor
         #   i = i + 1

        if (x != None):
            if ((self == self.successor) or (key_in_range(x.id, self.id, self.successor.id, False))):
                self.successor = x

        self.successor.notify(self)
  
    def notify(self, checkNode):
        if ((self.predecessor == None) or (key_in_range(checkNode.id, self.predecessor.id, self.id, False)) ):
            self.predecessor = checkNode
        
    def reset_finger_table(self):
        for i in range(0, ChordRing.m):
            self.finger_table[i] = self.successor

    def fix_fingers(self):
        self.reset_finger_table()
        for i in range(0, ChordRing.m):
            finger_start = (self.id + (1 << i)) % (1 << ChordRing.m)
            self.finger_table[i] = self.find_successor(finger_start)

    # def find_successor_impl(self, originalNode, id, depth):
    #     closest_preceding_node = None
    #     depth = depth + 1

    #     if (depth > ChordRing.m * 2):
    #         return originalNode.successor.find_successor(id)

    #     if ((key_in_range(id, self.id, self.successor.id, True)) or self == self.successor):
    #         return self.successor
    #     else:
    #         closest_preceding_node = self.closest_preceding_node(id)
    #         if closest_preceding_node == self:
    #             return self.successor.find_successor_impl(originalNode, id, depth)
    #         return closest_preceding_node.find_successor_impl(originalNode, id, depth)


    # def find_successor(self, id):
    #     return self.find_successor_impl(self, id, 0)
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

    # def closest_preceding_node(self, id):
    #     for i in range(ChordRing.m - 1, -1, -1):
    #         if ( key_in_range(self.finger_table[i].id, self.id, id, False) ):
    #             return self.finger_table[i]
    #     return self

    def insertKey(self, id):
        return None
    
    def printFingerTable(self):
        #print("Printing " + str(self.id) + " Finger Table")
        for key, value in self.finger_table.items():
            print("Key " + str(key) + " Value " + str(value.id))


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
            print("Adding Node " + str(id))

            node = ChordNode(id)
            node.join(ChordRing.getNodes()[random.randint(0, ChordRing.getNumNodes() - 1)])
            ChordRing.addNode(node)
            node.stabilize()
            node.fix_fingers()

            for node in ChordRing.getNodes():
                node.stabilize()
                node.fix_fingers()

        elif command[0] == "INSERT_KEY":
            return None
        else:
            return None

    # 23 -> 28 -> 45 -> 23
    for node in ChordRing.getNodes():
        print(str(node.predecessor.id) + " -> " + str(node.id) + " -> " + str(node.successor.id))
        node.printFingerTable()


if __name__ == "__main__":
    readLog()
