class refList:
    _list = range(64)
    _avalible = _list
    def __init__(self):
        return self
    def getRefs(self):
        return [i for i in self._list]
    def getAvalible(self):
        return [i for i in self._avalible]
    def getNewRef(self):
        try:
            return _avalible.pop()
        except IndexError:
            self.makeMoreRefs(64)
        return _avalible.pop()
    def makeMoreRefs(self, n):
        _list+=range(_list[-1]+1, _list[-1]+1+n)
        _avalible+=range(_list[-1]+1, _list[-1]+1+n)
    def releaseRef(self, ref):
        for i in self._list:
            if ref == i:
                self._avalible += ref
                return
        raise IndexError("ref does not exist")
        
class simpleHeap:
    _refList = refList()
    _class = simpleHeap
    def __init__(self, compareFunction, *inValues):
        self._tree = dict()
        self.compare = compareFunction
        self._rootRef = None
        ##each node -> [value, parentRef, [childrenRefs]]
        inValLen = len(inValues)
        if inValLen==1:
            self.insert(inValues(1))
        if inValLen>1:
            return merge(self._class(compareFunction, *inValues[inValLen/2:]),
                  self._class(compareFunction, *inValues[:inValLen/2]))
                              
    def __str__(self):
        print self._tree
    def getRefList:
        return self._refList
    
    def __get__(self, ref):
        return self._tree[ref]
    
    def get_rootVal(self):
        if self._rootRef == None:
            return None
        return self._tree[self._rootRef][0]

    def delete_root(self):
        freeChildren = self._tree[self._rootRef][2]
        del self._tree[self._rootRef]
        self._refList.releaseRef(self._rootRef)
        curRoot = freeChildren[0]
        for i in freeChildren:
            if compare(self._tree[i][0], self._tree[curRoot][0]):
                curRoot = i
        freeChildren.remove(curRoot)
        self._refList.releaseRef(self._rootRef)
        self._tree[curRoot][2] = self._tree[curRoot][2] + freeChildren
        self._rootRef = curRoot
        
    def promote_key(self, ref):
        node = self._tree[ref]
        pRef = node[1]
        self._tree[pRef][2].remove(ref)
        newpRef = self._tree[pRef][1]
        self._tree[newpRef][2].append(ref)
        self._tree[ref][1] = newpRef
        
    def insert(self, value):
        newRef = self._refList.getNewRef()
        if self._rootRef==None:
            self._rootRef = newRef
            newNode = [value, None, []]
            self._tree[newRef] = newNode
        elif self.compare(value, self.get_rootVal()):
            newRoot = [value, None, [self._rootRef]]
            self._tree[self._rootRef][1] = newRef
            self._rootRef = newRef
        else:
            newNode = [value, self._rootRef, []]
            self._tree[newRef] = newNode
            self._tree[self._rootRef][2].append(newRef)
            
    def merge(self, other):
        otherRefs = other._tree.iterkeys()
        if self.compare(self.getRootVal(), other.getRootVal()):
            for i in otherRefs:
                self._tree[i] = other._tree[i]
                self._tree[self._rootRef][2].append(other._rootRef)
        elif self.compare(other.getRootVal(), self.getRootVal()):
            for i in otherRefs:
                self._tree[i] = other._tree[i]
                self._tree[self._rootRef][1] = other._rootRef
                self._tree[other._rootRef][2].append(self._rootRef)
                self._rootRef = other._rootRef
        else:
            raise ValueError("Roots are not comparible!")
        del other
