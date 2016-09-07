class KillPath:
    pass

class coloredEdgeNode:
    """red = "r"
    blue = "b"
    green = "g"
    black = "bl" """
    def __init__(self, name, links=[]):
        self.name = name
        self.edges = [[l, ["bl"]]for l in links]
        
    def addEdge(self, link, color = "bl"):
        for i in range(len(self.edges)):
            if self.edges[i][0] == link:
                self.edges[i][1] += [color]
                return
            
        self.edges.append([link, [color]])
        
    def rmEdge(self, link):
        index = [i[0] for i in self.edges].index(link)
        self.edges = self.edges[:index]+self.edges[index+1:]
        
    def colorEdge(self, link, color):
        index = [i[0] for i in self.edges].index(link)
        self.edges[index][0] = color

    def colorDistanceNPaths(self, color, n, curDis = 0,\
                            prevPathsWOAddition = []):
        for i in prevPathsWOAddition:
            if i == self:
                return KillPath
        if curDis == n:
            return [self.name]
        retVal = []
        for e in self.edges:
            if any(i == color for i in e[1]):
                dpRet = e[0].colorDistanceNPaths(color, n, curDis+1)
            else:
                dpRet = e[0].colorDistanceNPaths(color, n, curDis,\
                                                 prevPathsWOAddition+[self])
            if dpRet!=KillPath:
                retVal.extend(self.name+"->"+i for i  in dpRet)
        return retVal

def main():
    names = ['malldoor', 'plaza', 'greathall', 'escalator',\
             'escalatorup', 'mallpond', 'fountain', 'gutter',\
             'escalatordown', 'island', 'thickgarden', 'greattree',\
             'deepgarden', 'jungle', 'deepexit', 'opensea',\
             'deepgarden2', 'fieldpath', 'hillpath', 'mountainpath',\
             'ruin1', 'camp', 'ruin2door', 'ruin2', 'shrine', 'seagarage',\
             'waterfall', 'deck', 'tanks', 'lakeview', 'tanks2', 'lake',\
             'akemonsteruncle', 'tanks2out', 'lakemonster', 'topoflake']
    malldoor = coloredEdgeNode('malldoor')
    plaza = coloredEdgeNode('plaza')
    greathall = coloredEdgeNode('greathall')
    escalator = coloredEdgeNode('escalator')
    escalatorup = coloredEdgeNode('escalatorup')
    mallpond = coloredEdgeNode('mallpond')
    fountain = coloredEdgeNode('fountain')
    gutter = coloredEdgeNode('gutter')
    escalatordown = coloredEdgeNode('escalatordown')
    island = coloredEdgeNode('island')
    thickgarden = coloredEdgeNode('thickgarden')
    greattree = coloredEdgeNode('greattree')
    deepgarden = coloredEdgeNode('deepgarden')
    jungle = coloredEdgeNode('jungle')
    deepexit = coloredEdgeNode('deepexit')
    opensea = coloredEdgeNode('opensea')
    deepgarden2 = coloredEdgeNode('deepgarden2')
    fieldpath = coloredEdgeNode('fieldpath')
    hillpath = coloredEdgeNode('hillpath')
    mountainpath = coloredEdgeNode('mountainpath')
    ruin1 = coloredEdgeNode('ruin1')
    camp = coloredEdgeNode('camp')
    ruin2door = coloredEdgeNode('ruin2door')
    ruin2 = coloredEdgeNode('ruin2')
    shrine = coloredEdgeNode('shrine')
    seagarage = coloredEdgeNode('seagarage')
    waterfall = coloredEdgeNode('waterfall')
    deck = coloredEdgeNode('deck')
    tanks = coloredEdgeNode('tanks')
    lakeview = coloredEdgeNode('lakeview')
    tanks2 = coloredEdgeNode('tanks2')
    lake = coloredEdgeNode('lake')
    akemonsteruncle = coloredEdgeNode('akemonsteruncle')
    tanks2out = coloredEdgeNode('tanks2out')
    lakemonster = coloredEdgeNode('lakemonster')
    topoflake = coloredEdgeNode('topoflake')

    malldoor.addEdge(plaza, "g")
    malldoor.addEdge(mallpond, "b")
    plaza.addEdge(greathall, "g")
    plaza.addEdge(fountain, "g")
    plaza.addEdge(fountain, "r")
    greathall.addEdge(escalator, "g")
    escalator.addEdge(escalatorup, "g")
    escalatorup.addEdge(greattree, "g")
    mallpond.addEdge(plaza, "g")
    fountain.addEdge(gutter, "g")
    fountain.addEdge(island, "g")
    gutter.addEdge(greattree, "b")
    escalatordown.addEdge(deepgarden, "b")
    island.addEdge(greattree, "r")
    thickgarden.addEdge(deepgarden, "g")
    greattree.addEdge(hillpath, "g")
    greattree.addEdge(fieldpath, "r")
    deepgarden.addEdge(jungle, "r")
    deepgarden.addEdge(deepgarden2, "b")
    jungle.addEdge(deepexit, "r")
    jungle.addEdge(fieldpath, "g")
    deepexit.addEdge(opensea, "r")
    deepexit.addEdge(opensea, "b")
    opensea.addEdge(seagarage, "b")
    opensea.addEdge(seagarage, "r")
    deepgarden2.addEdge(jungle, "r")
    fieldpath.addEdge(ruin1, "g")
    hillpath.addEdge(mountainpath, "r")
    hillpath.addEdge(camp, "b")
    mountainpath.addEdge(waterfall, "r")
    mountainpath.addEdge(waterfall, "b")
    ruin1.addEdge(ruin2door, "r")
    ruin1.addEdge(ruin2, "b")
    camp.addEdge(mountainpath, "r")
    ruin2door.addEdge(ruin2, "bl")
    ruin2door.addEdge(shrine, "bl")
    ruin2.addEdge(deepexit, "r")
    ruin2.addEdge(mountainpath, "b")
    shrine.addEdge(ruin2, "bl")
    seagarage.addEdge(waterfall, "b")
    seagarage.addEdge(deck, "g")
    waterfall.addEdge(tanks, "r")
    waterfall.addEdge(lakeview, "b")
    deck.addEdge(waterfall, "g")
    deck.addEdge(tanks, "r")
    deck.addEdge(tanks, "b")
    tanks.addEdge(lakeview, "r")
    tanks.addEdge(tanks2, "r")
    lakeview.addEdge(lake, "b")
    lakeview.addEdge(lake, "g")
    tanks2.addEdge(tanks2out, "r")
    lake.addEdge(akemonsteruncle, "b")
    lake.addEdge(lakemonster, "r")
    akemonsteruncle.addEdge(topoflake, "bl")
    akemonsteruncle.addEdge(tanks2out, "b")
    tanks2out.addEdge(malldoor, "b")
    tanks2out.addEdge(malldoor, "g")
    lakemonster.addEdge(malldoor, "g")
    topoflake.addEdge(malldoor, "g")

    greenWins = malldoor.colorDistanceNPaths("g", 6)
    blueWins = seagarage.colorDistanceNPaths("b", 6)
    redWins = thickgarden.colorDistanceNPaths("r", 6)

    return greenWins, blueWins, redWins
        
