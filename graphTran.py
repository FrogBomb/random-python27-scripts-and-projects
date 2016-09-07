import threading
import time
from Useful_Algorithms import memo

class DontPass:
    pass

class ToggleFlipNode:
    pass

class graphTranInterface:
    """The interface for graphTran. This contains the "main node,"
    where a graphTran program is started, and accepts several "outputNodes"
    from which output is printed."""
    def __init__(self, mainNode, IOFile, outputNodes = []):
        self._mainNode = mainNode
        self._outputNodes = []
        self._IOFile = IOFile
        self._timesOut = 0
        for outputNode in outputNodes:
            self.addNewOutputNode(outputNode)
    def execute(self):
        self._mainNode.start()
    def addNewOutputNode(self, newOutputNode):
        self._outputNodes.append(newOutputNode)
        newOutputNode.addLinks(self)
    def printOutput(self, *args):
        print time.clock(), "there"
        outPrint = ""
##        for a in args:
##            outPrint += str(a) + " "
        print outPrint
##        outFile = open(self._IOFile, 'w')
##        outFile.write(str(args))
##        outFile.close()
    def getOutputNodes(self):
        return [i for i in self._outputNodes]
    def removeOutputNode(self, node):
        node._links.remove(self)
        self._outputNodes.remove(node)
    
def fixFunction(func):
    def newFunc(outLinks, *args):
        return func(*args)
    return newFunc

def changeOutLinks(outlinks, newOutLinks):
    for i in [j for j in outlinks]:
        outlinks.remove(i)
    for i in newOutLinks:
        outlinks.append(i)
        
class funcNode:
    """A node that takes a function func(outNodes, *args)
    and links the function output as input for linked nodes.
    If the output of the function is "None", then nothing is passed."""
    def __init__(self, func, links = [], fixFunc = True):
        if fixFunc:
            func = fixFunction(func)
        self._code = func
        self._links = [i for i in links]
        self._args = []
        self._cNThread = _funcNodeThread(func, self._links)
        self.cv = threading.Condition()
    def start(self):
        self._cNThread._passCondition(self.cv)
        self._cNThread.start()
        self._cNThread = _funcNodeThread(self._code, self._links)
        self._cNThread._passArgs(*self._args)
        
    def run(self):
        self._cNThread.run()
    def addLinks(self, *links):
        self._links.extend(links) ##Note, this is also in the cNThread.
        self._cNThread.addLinks(*links)
    def _passArgs(self, *args):
        self._args = args
        self._cNThread._passArgs(*args)
    def isLocked(self):
        return self._cNThread.isLocked
    def lock(self):
        self._cNThread.isLocked = True

class mergeNode(funcNode):
    """A special funcNode that takes a series of inputs together,
    and returns them all in one list to the linked funcNodes."""
    def __init__(self, numInputs, links=[]):
        self._numInLinks = [numInputs] ##so it is passed by reference
        self.outList = []
        def func(*a):
            if len(a) == 1:
                self.outList.append(a[0])
            else:
                self.outList.append(a)
            if self._numInLinks[0] <= len(self.outList):
                retVal = tuple(self.outList)
                self.__init__(self._numInLinks[0], self._links)
                return  retVal
            elif self._numInLinks[0] > len(self.outList):
                return DontPass
        funcNode.__init__(self, func, links)
        
    def changeInLinks(newNumInputs):
        self._numInLinks[0] = newNumInputs

class flipNode(funcNode):
    """A special node that flips between two outLinks if it
    is sent a "ToggleFlipNode" token."""
    def __init__(self, primaryNode, secondaryNode):
        self._whichLink = [0] ##so it is passed by reference
        def func(outLinks, *args):
            if args[0] == ToggleFlipNode:
                args[1:]
                self._whichLink[0] = 1 - self._whichLink[0]
            changeOutLinks(outLinks, self._whichLink)
            return args
        
        funcNode.__init__(self, func, [primaryNode, secondaryNode],\
                          fixFunc = False)

class gateNode(funcNode):
    """A special node that passes input n times before
    switching direction of output."""
    def __init__(self, numInputs, primaryNode, secondaryNode):
        self._numInputs = [numInputs] ##so it is passed by reference
        self.curPasses = 0
        def func(outLinks, *args):
            self.curPasses += 1
            if self._numInputs[0] > self.curPasses:
                changeOutLinks(outLinks, [0])
                return args
            else:
                changeOutLinks(outLinks, [1])
                return args    
        funcNode.__init__(self, func, [primaryNode, secondaryNode],\
                          fixFunc = False)
    def start(self):
        funcNode.start(self)
        
        
class dumbNode(funcNode):
    """A special node that simply passes input."""
    def __init__(self, links= []):
        def func(*args):
            return args
        funcNode.__init__(self, func, links)

class splitNode(dumbNode):
    """A special node that splits input."""
    def __init__(self, links = []):
        dumbNode.__init__(self, links)
        self._cNThread = _splitNodeThread(self._code, self._links)
    def start(self):
        self.cv.acquire()
        self._cNThread.start()
        self._cNThread = _splitNodeThread(self._code, self._links)
        self._cNThread._passArgs(*self._args)
        self.cv.notify()
        self.cv.release()
            

class syncNode(funcNode):
    """A special funcNode that syncs with other syncNodes that share the
        same key."""
    def __init__(self, syncKey, links= []):
        def func(*args):
            syncKey.acquire()
            syncKey.wait()
            syncKey.release()
            return args
        funcNode.__init__(self, func, links)
        self.syncKey = syncKey
        syncKey._registerSyncNode(self)
    def changeSyncKey(self, syncKey):
        self.syncKey._removeSyncNode(self)
        self.syncKey = syncKey
        syncKey._registerSyncNode(self)
    def getSyncKey(self):
        return self.syncKey
    def __del__(self):
        self.syncKey._removeSyncNode(self)
        funcNode.__del__(self)

class syncKey:
    """A key for syncNode"""
    _i = 0
    def __init__(self):
        self.keyNumber = syncKey._i
        self._condition = threading.Condition()
        syncKey._i += 1
        self.syncNodes = []
        self.numWaiting = 0
    def _registerSyncNode(self, syncNode):
        self.syncNodes.append(syncNode)
    def _removeSyncNode(self, syncNode):
        self.syncNodes.remove(syncNode)
    def getNodesWithKey(self):
        return [i for i in syncNodes]
    def acquire(self, *args):
        self._condition.acquire(*args)
    def wait(self):
        self.numWaiting += 1
        if self.numWaiting >= len(self.syncNodes):
            self.notifyAll()
        else:
            self._condition.wait()
    def release(self):
        self._condition.release()
    def notify(self, n=1):
        self._condition.notify(n)
    def notifyAll(self):
        self._condition.notifyAll()
    notify_All = notifyAll
        

class _funcNodeThread(threading.Thread):
    """Helper class for funcNode"""
    def __init__(self, func, links = []):
        threading.Thread.__init__(self)
        self._code = func
        self._links = links
        self.outTo = range(len(links))
        self.canRun = False
        self._args = []
        self.argsPassed = False
        self.isLocked = False
        self.cv = None
            
    def run(self):
        self.cv.acquire()
        outData = self._code(self.outTo, *self._args)
        tempOutTo = [i for i in self.outTo]
        self.cv.release()
        if outData == DontPass:
            return
        if outData == None:
            for i in tempOutTo:
                if isinstance(self._links[i], graphTranInterface):
                    self._links[i].printOutput(outData)
                    continue
                self._links[i].cv.acquire()
                while self._links[i].isLocked():
                    self._links[i].cv.wait()
                self._links[i].lock()
                self._links[i]._passArgs()
                self._links[i].start()
                self._links[i].cv.release()
                
        elif type(outData) != tuple:
            for i in tempOutTo:
                if isinstance(self._links[i], graphTranInterface):
                    self._links[i].printOutput(outData)
                    continue
                self._links[i].cv.acquire()
                while self._links[i].isLocked():
                    self._links[i].cv.wait()
                self._links[i].lock()
                self._links[i]._passArgs(outData)
                self._links[i].start()
                self._links[i].cv.release()
                

        else:
            for i in tempOutTo:
                if isinstance(self._links[i], graphTranInterface):
                    self._links[i].printOutput(*outData)
                    continue
                self._links[i].cv.acquire()
                while self._links[i].isLocked():
                    self._links[i].cv.wait()
                self._links[i].lock()
                self._links[i]._passArgs(*outData)
                self._links[i].start()
                self._links[i].cv.release()

    def addLinks(self, *links):
        self.outTo = range(len(links))
        
    def _passArgs(self, *args):
        self._args = args
    def _passCondition(self, cv):
        self.cv = cv

class _splitNodeThread(_funcNodeThread):
    """Helper function for splitNodes."""
    def run(self):
        self.cv.acquire()
        outData = self._code(self.outTo, *self._args)
        tempOutTo = [i for i in self.outTO]
        self.cv.release()
        if outData == None:
            return

        if outData == None:
            for i in tempOutTo:
                if isinstance(self._links[i], graphTranInterface):
                    self._links[i].printOutput(outData)
                    continue
                self._links[i].cv.acquire()
                while self._links[i].isLocked():
                    self._links[i].cv.wait()
                self._links[i].lock()
                self._links[i]._passArgs()
                self._links[i].start()
                self._links[i].cv.release()
                
        elif type(outData) != tuple:
            for i in tempOutTo:
                if isinstance(self._links[i], graphTranInterface):
                    self._links[i].printOutput(outData)
                    continue
                self._links[i].cv.acquire()
                while self._links[i].isLocked():
                    self._links[i].cv.wait()
                self._links[i].lock()
                self._links[i]._passArgs(outData)
                self._links[i].start()
                self._links[i].cv.release()
                    
        else:
            for i in tempOutTo:
                if isinstance(self._links[i], graphTranInterface):
                    self._links[i].printOutput(outData[i])
                    continue
                self._links[i].cv.acquire()
                while self._links[i].isLocked():
                    self._links[i].cv.wait()
                self._links[i].lock()
                self._links[i]._passArgs(outData[i])
                self._links[i].start()
                self._links[i].cv.release()

def fibTest(n):
    def o():
        return 1
    def z():
        return 0
    def m():
        return
    def newSum(*args):
        return sum(args)
    def newMax(*args):
        return max(args)
    
    one = funcNode(o, fixFunc = True)
    zero = funcNode(z, fixFunc = True)
    mainNode = funcNode(m, fixFunc = True)
    merge2 = mergeNode(2)
    sumNode = funcNode(newSum,fixFunc = True)
    outNode = dumbNode()
    gaten = gateNode(n, sumNode, outNode)
    maxNode = funcNode(newMax, fixFunc = True)
    mainNode.addLinks(one, zero)
    one.addLinks(merge2)
    zero.addLinks(merge2)
    merge2.addLinks(maxNode, gaten)
    maxNode.addLinks(merge2)
    sumNode.addLinks(merge2)
    interface = graphTranInterface(mainNode, "C:/Python27/fibOut.txt", outputNodes = [outNode])
    interface.execute()

def fib(n):
    curPair = [0, 1]
    for i in range(n-1):
        temp = sum(curPair)
        curPair[0] = curPair[1]
        curPair[1] = temp
    return curPair
    

if __name__ == "__main__":
    time.clock()
    fibTest(100000)
    fib(100000)
##    print fib(200)
    print time.clock(), "hi"
