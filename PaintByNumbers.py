#############NEED TO DO:##################
##                                      ##
##Need to finish PBNViewController      ##
##-setup                                ##
##-drawMap                              ##
##-updateCell                           ##
##-coordinatesToCell                    ##
##                                      ##
##Need to make I/O model (easy-ish)     ##
##                                      ##
##Need to make main                     ##
##                                      ##
##Need to make a better default PBNMap  ##
##                                      ##
##Need to make editor (future)          ##
##########################################


from swampy.Gui import *
import Tkinter
import tkFileDialog

class coordsToCellError(Exception):
    pass

class PBN:
    """A Paint By Numbers object.
        If no parameters are specified, will make a 10x10 default board."""

    def __init__(self, myMap = None, title = None, *colors):
        if myMap == None:
            self._map = getDefaultPBNMap()
        elif isinstance(myMap, PBNMap):
            self._map = myMap
        else:
            raise TypeError("myMap must be a PBN map or None")
        self._viewMap = PBNMap(self._map.dims())
        self._colors = ["white", "black"] + [c for c in colors] + ["x"]
        self._gui = Gui() ##From Swampy
        self._view = PBNViewController(self._map.dims(), self._gui, title, *colors)
        self._view.setup([self.getRowList(i) for i in range(self._map.dims()[0])],
                         [self.getColList(j) for j in range(self._map.dims()[0])],
                         self._viewMap, self._controller)

    def checkIfSolved(self):
        mapData = self._map.stripData()
        viewData = self._viewMap.stripData()
        colors = self._colors
        for i in range(len(viewData)):
            if viewData[i]%(len(colors)-1) != mapData[i]:
                #This makes all x's in viewData white,
                #and then compares the values in each cell
                return False
        return True

            
    def getRowList(self, row):
        """Returns a list outlining consecutive values in a row"""
        mapRow = self._map.getRow(row)
        return self._getRorCList(mapRow)
            
    def getColList(self, col):
        """Returns a list outlining consecutive values in a col"""
        mapCol = self._map.getCol(col)
        return self._getRorCList(mapCol)
                
    def _getRorCList(self, RorC):###This is a PRIVATE helper function!
        """Returns a list outlining consecutive values in another list"""
        curVal = RorC
        retList = []
        curNum = 0
        for i in RorC:
            if curVal == i:
                curNum += 1
            else:
                retList.append((curVal, curNum))
                curVal = i
                curNum = 1
        return retList

    def __str__(self):
        return self._map.__str__()
    
class PBNMap:
    """A map for a paint by numbers board.
    By default: white = 0, black = 1
    For solving purposes, x = -1%len(colors), where
    x is a small x in the center of the
    cell instead of a color."""

    def __init__(self, dims, data = None):
        rows = dims[0]
        cols = dims[1]
        self._numRows = rows
        self._numCols = cols
        if data == None:
            self._data = [0]*rows*cols
        elif len(data)>rows*cols:
            raise BufferError("data must be able to fit in the matrix")
        else:
            self._data = data + [0]*(rows*cols-len(data))
            
    def __getitem__(self, key):
        if type(key) == int:
            return self._data[key]
        if type(key) == tuple:
            if len(key) == 2:
                if (key[0]<self._numRows)&(key[1]<self._numCols)&(key[0]>=0)&(key[1]>=0):
                    return self._data[self._numCols*key[0] + key[1]]
                else:
                    raise IndexError("list index out of range")
        raise TypeError("must be an int or two ints separated by a comma")
    
    def __setitem__(self, key, value):
##        if type(value) !=  self._mtype:
##            raise TypeError("must be the same type as the matrix")
        if type(key) == int:
            self._data[key] = value
            return
        if type(key) == tuple:
            if len(key) == 2:
                if (key[0]<self._numRows)&(key[1]<self._numCols)&(key[0]>=0)&(key[1]>=0):
                    self._data[self._numCols*key[0] + key[1]] = value
                    return
                else:
                    raise IndexError("list index out of range")
        raise TypeError("must be an int or two ints separated by a comma")
    
    def __str__(self):
        ret = ""
        return ret.join(str(self.getRow(i))+"\n" for i in range(self._numRows))[:-1]
    
    def dims(self):
        return self._numRows, self._numCols
    
    def getRow(self, rowNum):
        return [self[rowNum, i] for i in range(self._numCols)]
    
    def getCol(self, colNum):
        return [self[i, colNum] for i in range(self._numRows)]

    def stripData(self):
        return self._data

class PBNViewController:
    """A Paint By Numbers view controller"""
    def __init__(self, dims, gui, title, *colors):
        self._dims = dims
        self._title = title
        if title == None:
            self._title = "Paint By Numbers"
        self._colors = colors
        self._gui = gui
        self._canvas = None
        self._boundingPixels = None
        
    def setup(self, rowListNumbers, colListNumbers, pbnMap):
        self._gui.title(self._title)
        self._canvas = self._gui.ca(width = self._dims[1]*50+60,
                                    height = self._dims[0]*50+60,
                                    bg = "white")
        self.drawMap(rowListNumbers, colListNumbers, pbnMap)
        self._canvas.bind("<ButtonPress-1>", onMouseClick)
        self._canvas.bind("<ButtonPress-3>", onMouseClick)
        self._gui.mainloop()

    def drawMap(self, rowListNumbers, colListNumbers, pbnMap):
        """Prepares the gui to draw a Map"""
        pass

    def updateCell(self, mapLocation):
        """Updates the Cell at the mapLocation = [row, col]"""
        pass

    def coordinatesToCell(self, coordinates):
        """Returns the mapLocation of a Cell from gui coordinates."""
        pass

    def onMouseClick(self, event):
        """Does what is needed when a user clicks on the canvas."""
        try:
            mP = [2-event.num, self.coordinatesToCell((event[0], event[1]))]
        except
        self._viewMap[mP[1]] += mP[0]
        self._viewMap[mP[1]] %= len(self._colors)
        self._view.updateCell(mP[1])
        
    

def getDefaultPBNMap():
    return PBNMap((10, 10))

def getBlankPBNMap(rows, cols):
    return PBNMap((rows, cols))

def open_it():
    filename = tkFileDialog.askopenfilename()
    return filename

def save_it():
    filename = tkFileDialog.askopenfilename()
    return filename

def save_as():
    filename = tkFileDialog.asksaveasfilename()
    return filename
