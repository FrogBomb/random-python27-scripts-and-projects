from numpy import random
import itertools
from copy import copy
A = (2, 14, 17)
B = (7, 10, 16)
C = (5, 13, 15)
D = (3, 9, 21)
E = (1, 12, 20)
F = (6, 8, 19)
G = (4, 11, 18)

sevenDiceDict = {'A': A,'B': B,'C': C,'D': D,'E': E,'F': F,'G': G}

ProbSortedFor3 = {'mmm': 1, 'mml': 3,\
                  'mll': 3, 'hml': 6,\
                  'hmm': 3, 'hll': 3, \
                  'lll': 1, 'hhh': 1, \
                  'hhm': 3, 'hhl': 3}

ProbSorted3Vs3 = dict()
for i in ProbSortedFor3:
	for j in ProbSortedFor3:
		ProbSorted3Vs3[i+" vs "+j]\
                                    = ProbSortedFor3[i]*ProbSortedFor3[j]


def calculateSortedProbTable(DiceDict, ProbSort):
    retTable = dict()
    for AtkD in DiceDict:
        for DefD in DiceDict:
            if AtkD == DefD:
                retTable[AtkD+" vs "+DefD] = None
            else:
                retTable[AtkD+" vs "+DefD] =\
                                calcScoreFor2(DiceDict[AtkD], DiceDict[DefD], ProbSort)
    return retTable

def calcScoreFor2(AtkDie, DefDie, ProbSort):
    ret = 0
    for key in ProbSort:
        atkDef = key.split(" vs ")
        atkStr = atkDef[0]
        defStr = atkDef[1]
        keepDefSide = False
        for i in range(len(atkStr)):
            if not keepDefSide:
                j = i
                dStr = defStr[j]
                defSide = DefDie[hml2SideNum(dStr)]
            aStr = atkStr[i]
            atkSide = AtkDie[hml2SideNum(aStr)]
            if atkSide > defSide:
                ret += ProbSort[key]
                keepDefSide = True
            else:
                keepDefSide = False
    return ret

def hml2SideNum(sideStr):
    if sideStr == 'h':
        return 2
    if sideStr == 'm':
        return 1
    if sideStr == 'l':
        return 0
        
def rollDice(**NumOfEachDie):
    ret = []
    for die in NumOfEachDie:
        dieRolls = random.random_integers(0, 2, NumOfEachDie[die])
        dieRolls = [sevenDiceDict[die][s] for s in dieRolls]
        ret.extend(dieRolls)
    return ret

def sortDiceInto3Piles(diceRolls):
    ret = {'l':[], 'm':[], 'h':[]}
    for r in diceRolls:
        if r<=7:
            ret['l'].append(r)
        elif r<=14:
            ret['m'].append(r)
        else:
            ret['h'].append(r)
    return ret

def chooseDefDieExpectedLoss(sortedPilesOfDice, **defDice):
    capLen = min(len(sortedPilesOfDice), sum(defDice[d] for d in defDice))
    totalDice = []
    for dDie in defDice:
        totalDice.extend([dDie]*defDice[dDie])
    DiceCombos = set(itertools.combinations(totalDice, capLen))
    SideCombos = {}
    for dCombo in DiceCombos:
        newRoll = [[]]
        for die in dCombo:
            possibleSides = sevenDiceDict[die]
            tmpNewRoll = []
            for side in possibleSides:
                for roll in newRoll:
                    tmpNewRoll.append(roll+[side])
            newRoll = tmpNewRoll
        SideCombos[dCombo] = newRoll
        
    defStrat = {}
    for dcombo in SideCombos:
        defStrat[dcombo] = [chooseDefDieBestStratScore(sortedPilesOfDice, combo)\
                            for combo in SideCombos[dcombo]]
    expectedScore = {}
    for dcombo in defStrat:
        expectedScore[dcombo] = sum(defStrat[dcombo])/float(len(defStrat[dcombo]))
    
    bestScore = all
    bestCombo = None
    for dcombo in expectedScore:
        if expectedScore[dcombo]<bestScore:
            bestScore = expectedScore[dcombo]
            bestCombo = dcombo
    
    return bestScore, bestCombo
        
def chooseDefDieBestStratScore(sortedPilesOfDice, defRoll):
    """Returns the score that the best def strategy gives the attacker"""
    if len(defRoll)<len(sortedPilesOfDice):
        defRoll.extend([0]*(len(sortedPilesOfDice)-len(defRoll)))
    pileArray = [key for key in sortedPilesOfDice]
    bestScore = all
    for perm in itertools.permutations(defRoll, len(sortedPilesOfDice)):
        curScore = 0
        for i in range(len(perm)):
            for attackRoll in sortedPilesOfDice[pileArray[i]]:
                if attackRoll>perm[i]:
                    curScore+= 1
        if curScore<bestScore:
            bestScore = curScore
    return bestScore
    
    
def simulateDefChooseDiceRules(attackDie, attackNum, defDie, defNum):
    totalExpectedWin = 0
    for i in range(1000):
        attackRoll = sortDiceInto3Piles(rollDice(**{attackDie:attackNum}))
        totalExpectedWin += chooseDefDieExpectedLoss(attackRoll, **{defDie:defNum})[0]
    return totalExpectedWin/1000.0
    