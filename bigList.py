import collections
class BigListError(StandardError):
    pass

class bigList:
    """A list-like structure for managing allot (possibly infinite) data."""
    def __init__(self, prefix, iterable=None, minChunkSize=2**8, database = None):
        if database == None:
            raise BigListError("Must specify a database")
        self._db = database
        self._chunkSize = minChunkSize
        self._iterables = [iterable]
        self._prefix = prefix
        self._suffix = []
        self._curPreChunk = 0
        self._curSufChunk = -1
    def _loadPreChunk(self, n):
        pass
    def loadSufChunk(self, n):
        pass
    def _reChunk(self):
        pass
    def _chunkSizes(self):
        pass
    def __iter__(self):
        i = 0
        while(True):
            yield self[i]
            i+=1
    def __getitem__(self, index):
        if type(index) == int:
            if index>= 0:
                try:
                    retval = self._prefix[index]
                except IndexError:
                    pass ####CHANGE THIS
            elif index<0:
                try:
                    retval = self._suffix[index]
                except IndexError:
                    pass
        elif type(index) == str:
            pass
        else:
            raise TypeError("index must be an int or string.")
        return retval
    def append(self, item):
        self._suffix.append(item)
    def appendToFront(self, item):
        self._loadChunk(0)
        self._prefix = [item]+self._prefix
    def extend(self, iterable):
        if not isinstance(iterable, \
                          collections.Iterable):
            raise TypeError("iterable must be iterable")
        try:
            length = len(iterable)
        except TypeError:
            self._iterables += [self._suffix, iterable]
            self._suffix = []
        self._suffix = iterable

class omegaList(bigList):
    def __init__(self, prefix, iterable=None, minChunkSize=2**8, database = None):
        if database == None:
            raise BigListError("Must specify a database")
        self._db = database
        self._chunkSize = minChunkSize
        self._iterable = iterable
        self._prefix = prefix
    def _addToEndOfIterable(self, newItems):
        iteratorCopy = self._iterable
        for i in iteratorCopy:
            yield i
        for i in newItems:
            yield i
    def _appendPrefix(self, item):
        self._prefix.append(item)
    def _getFromPrefix(self, index):
        return self._prefix[index]
    def _extendPrefix(self, toIndex):
        for i in range(len(self._prefix), toIndex):
                    self._appendPrefix(self._iterable.next())
    def append(self, item):
        self._iterable = self._addToEndOfIterable([item])
    def appendToFront(self, item):
        self._prefix.insert(0, item)
    def weave(self, otherOmegaList, minChunkSize=2**8, database = None):
        if database == None:
            raise BigListError("Must specify a database")
        def weavedIterator(a, b):
            flag = 0
            while(flag == 0):
                try:
                    yield a
                except StopIteration:
                    flag = 1
                try:
                    yield b
                except StopIteration:
                    flag = 2
            if flag == 1:
                for i in b:
                    yield i
            elif flag == 2:
                for i in a:
                    yield i

        newIter = weavedIterator(self, otherOmegaList):
        return omegaList([], newIter, minChunkSize, database)
                    
    def extend(self, iterable):
        self._iterable = self._addToEndOfIterable(iterable)
    def __getitem__(self, index):
        if index< 0:
            raise IndexError("Index must be positive")
        else:
           try:
               retval = self._getFromPrefix(index)
            except IndexError:
                self._extendPrefix(index)
            retval = self._getFromPrefix(index)
        return retval
