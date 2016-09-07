from BaseMatrix import *
"""
    This package contains several tools to
analyze different aspects of Game Theory.

"""
class strategy:
    pass

class TwoPlayerPayoutMatrix(BaseMatrix):
    """A two Player Payout Matrix"""
    def getExpectedOutcome(self, P1Strat, P2Strat):
        pass
    def getP1Security(self, P1Strat):
        pass
    def getP2Security(self, P2Strat):
        pass
    
class TwoPlayerGame:
    """A Two Player Game"""
    def __init__(self, player1PayMatrix, player2PayMatrix):
        self._p1M = player1PayMatrix
        self._p2M = player2PayMatrix
    def isZeroSum(self):
        pass
    def play(self, P1Strat, P2Strat):
        pass
    def getP1Payout(self):
        return self._p1M
    def getP2Payout(self):
        return self._p2M

class conwayGame:
    def __init__(self, LeftOptions = [], RightOptions = []):
##        flags = []
##        for l1 in range(len(LeftOptions)):
##            for l2 in range(l1+1, len(LeftOptions)):
##                if hash(LeftOptions[l1]).congruent(hash(LeftOptions[l2])):
                    
        self._L = tuple(i for i in LDict.iterkeys())
        self._R = tuple(i for i in RDict.iterkeys())

    def congruent(self, other):
        for l in self.LeftOptions():
            pass
        pass
            
    def LeftOptions(self):
        return self._L

    def RightOptions(self):
        return self._R

    def __hash__(self):
        return hash((conwayGame, self._L, self._R))

    def is_a_number(self):
        for i in self._L:
            for j in self._R:
                if not i<j:
                    return False
        return True

    def is_right_Win(self):
        return self.is_right_second_Win() and self.is_right_first_Win()
    def is_left_Win(self):
        return self.is_left_second_Win() and self.is_left_first_Win()
    def is_first_Win(self):
        return self.is_left_first_Win() and self.is_right_first_Win()
    def is_second_Win(self):
        return self.is_left_second_Win() and self.is_right_second_Win()

    def is_right_second_Win(self):
        for lO in self.LeftOptions():
            if any(type(lO) == i  for i in (float, int, long)):
                if lO>=0:
                    return False
            elif not lO.is_right_first_Win():
                return False
        return True
    
    def is_left_second_Win(self):
        for rO in self.RightOptions():
            if any(type(rO) == i  for i in (float, int, long)):
                if rO<=0:
                    return False
            elif not rO.is_left_first_Win():
                return False
        return True
    
    def is_right_first_Win(self):
        for rO in self.RightOptions():
            if any(type(rO) == i  for i in (float, int, long)):
                if rO<=0:
                    return True
            elif rO.is_right_second_Win():
                return True
        return False
    
    def is_left_first_Win(self):
        for lO in self.LeftOptions():
            if any(type(lO) == i  for i in (float, int, long)):
                if lO>=0:
                    return True
            elif lO.is_left_second_Win():
                return True
        return False

    def __lt__(self, other):
        if other == 0:
            return self.is_right_Win()
        if self-other<0:
            return True
        else:
            return False

    def __le__(self, other):
        if other == 0:
            return self.is_right_second_Win()
        if self-other<=0:
            return True
        else:
            return False
        
    def __gt__(self, other):
        if other == 0:
            return self.is_left_Win()
        if self-other>0:
            return True
        else:
            return False
        
    def __ge__(self, other):
        if other == 0:
            return self.is_left_second_Win()
        if self-other>=0:
            return True
        else:
            return False

    def __eq__(self, other):
        if other == 0:
            return self.is_second_Win()
        if self-other==0:
            return True
        else:
            return False

    def __ne__(self, other):
        if  other == 0:
            return self.is_first_Win()
        if self-other<>0:
            return True
        else:
            return False

    def __add__(self, other):
        if self.LeftOptions() == tuple() and\
               self.RightOptions() == tuple():
                return other
        if any(type(other) == i  for i in (float, int, long)):
            return conwayGame([i+other for i in self.LeftOptions()],\
                               [i+other for i in self.RightOptions()])
        if isinstance(other, conwayGame):
            return conwayGame([self+j for j in other.LeftOptions()]+\
                              [i+other for i in self.LeftOptions()],
                              [self+j for j in other.RightOptions()]+\
                              [i+other for i in self.RightOptions()])
    def __radd__(self, other):
        return self+other

    def __sub__(self, other):
        return self+(-other)
    def __neg__(self):
        return conwayGame([-i for i in self.RightOptions()],\
                              [-i for i in self.LeftOptions()])

    def __str__(self):
        retStr = "{"
        for l in self.LeftOptions():
            retStr += l.__str__() + ", "
        retStr = retStr[:-2]
        retStr += "|"
        for r in self.RightOptions():
            retStr += r.__str__() + ", "
        retStr = retStr[:-2]
        retStr += "}"
        return retStr
        
def solveTwoPlayerZeroSumGame(game):
    denom = float(p1Payout[0, 0]-p1Payout[0, 1]-p1Payout[1, 0]+p1Payout[1, 1])
    if denom !=0:
        alpha = (p1Payout[1, 1]-p1Payout[0, 1])/denom
        beta = (p1Payout[1, 1]-p1Payout[1, 0])/denom
        
    pass
