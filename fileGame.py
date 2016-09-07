class GameControl:
    def __init__(self, storyFile):
        self._FM = FileMaker()
        self._SB = StoryBoard(storyFile)
    
class FileMaker:
    def __init__(self):
        self.Parser = Parser()

    def makeFile(self, fileLocation):
        return

    def editFile(self, fileLocation):
        return

class StoryBoard:
    def __init__(self, storyFile):
        self._f = storyFile
        
class Parser:
    def __init__(self):
        return
    
