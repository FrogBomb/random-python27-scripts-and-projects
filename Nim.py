class Nim:
    def __init__(self, *heaps):
        self._heaps = [h for h in heaps]
        self._takeOut0Heaps()

    def _takeOut0Heaps(self):
        while(True):
            try:
                self._heaps.remove(0)
            except ValueError:
                return
            
    def __str__(self):
        ret = ""
        for i in range(len(self._heaps)):
            ret += str(i)+" " + "|"*self._heaps[i] + "\n"
        return ret

    def getHeaps(self):
        return self._heaps

    def takeFrom(self, Heap, HowMuch):
        if HowMuch<=0:
            raise ValueError
        self._heaps[Heap]-=HowMuch
        if self._heaps[Heap] < 0:
            self._heaps[Heap] = 0
        self._takeOut0Heaps()

    def checkIfFinished(self):
        return len(self._heaps) == 0

from random import *

class NimBot:
    def __init__(self, nim, mode = "last Wins"):
        self._nim = nim

    def playMove(self):
        heaps = self._nim.getHeaps()
        nimSum = 0
        take = 0
        fromHeap = 0
        for h in heaps:
            nimSum ^= h
        if nimSum == 0:
            fromHeap, take = self.getRandomFromTake()
        else:
            for i in range(len(heaps)):
                if heaps[i]^nimSum < heaps[i]:
                    take = heaps[i] - (heaps[i]^nimSum)
                    fromHeap = i
                    break
        print "The Bot took " + str(take) + " from " + str(fromHeap)
        self._nim.takeFrom(fromHeap, take)

    def getRandomFromTake(self):
        heaps = self._nim.getHeaps()
        fromHeap = randrange(0, len(heaps))
        take = randrange(1, heaps[fromHeap]+1)
        return fromHeap, take
        
if __name__ == "__main__":
    numOfHeaps = randrange(2, 7)
    heaps = [randrange(1, 20) for i in range(numOfHeaps)]
    theGame = Nim(*heaps)
    theBot = NimBot(theGame)
    print "Welcome to Nim!"
    print theGame
    goFirst = raw_input("Want to go first? (y/n): ")
    if(goFirst == 'n'):
        print ""
        theBot.playMove()
        print ""
    while(theGame.checkIfFinished() == False):
        print "Your Turn!"
        print theGame
        temp = True
        while(temp):
            try:
                temp = False
                heap = int(raw_input("Which Heap?: "))
                test = heaps[heap]
            except ValueError, IndexError:
                print "Type an integer in range"
                temp = True
        temp = True
        while(temp):
            try:
                temp = False
                take = int(raw_input("How much Will you take?: "))
                theGame.takeFrom(heap, take)
            except ValueError:
                print "Type an integer in range"
                temp = True
        if theGame.checkIfFinished():
            k = raw_input("You win!")
            break
        print theGame
        theBot.playMove()
        print ""
        if theGame.checkIfFinished():
            k = raw_input("You Lost!")
            break
