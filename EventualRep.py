class eventualRep:    
    def __init__(self, head, repTail):
        self.head = head
        self.repTail = repTail

    def __iter__(self):
        for i in self.head:
            yield i
        while(True):
            for j in self.repTail:
                yield j

def PellsSolver(N, extFracIter):
    poopers = [0,1]
    crapers = [1,0]
    for i in extFracIter:
        print i
        poopers.append(poopers[-1]*i+poopers[-2])
        crapers.append(crapers[-1]*i+crapers[-2])
        print str(poopers[-1])+"**2 -",
        print str(N) + "*(" + str(crapers[-1]) + ")**2 =",
        print str(poopers[-1]**2 - N*crapers[-1]**2)
        if poopers[-1]**2 - N*crapers[-1]**2 == 1:
            return crapers, poopers


def extFracEst(a):
    while(True):
        yield int(a)
        if a == int(a):
            return
        a = (a - int(a))**(-1)



        
