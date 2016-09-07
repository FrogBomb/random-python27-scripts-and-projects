
import Tkinter
import tkFileDialog

def open_it():
    filename = tkFileDialog.askopenfilename()
    return filename

def save_it():
    filename = tkFileDialog.askopenfilename()
    return filename

def save_as():
    filename = tkFileDialog.asksaveasfilename()
    return filename

def _raiseDataTableKeyError():
    raise KeyError("Key must be of type int or str or a tuple (int, str).")    

class DataTable:
    """ The Data Table Object

        A DataTable has rows indexed by integers and
    columns indexed by strings (labels). New rows or labels
    may be added easilly using the "addNewRow" or "addNewLabel"
    methods. A DataTable cannot have two of the same labels,
    but two rows may be identical.

    Deletion of rows, labels, or specific values may
    be done through:
    
    >>>del myDataTable[<<row or label or row,label>>]

    Retreval of rows, columns, or specific values may similarly
    be done by:

    >>>myDataTable[<<row or label or row,label>>]

    a value may be set by:

    >>>myDataTable[<<row or label or row, label>>] = value

    to print properly, tables must be less than 1,000,000 rows long."""
    
    def __init__(self, size, *labels):
        if size == 0:#It's never 0...
            size = 1
        elif type(size) != int:
            raise ValueError("The size must be an integer value!")
        self._labels = [str(l) for l in labels]
        self._size = size
        self._table = [dict.fromkeys(str(l) for l in labels) for i in range(size)]
        
    def __len__(self):
        return self._size
    
    def _extraTabsNeeded(self, l, strLen):
        return (max(len(l),max(len(str(i)) for i in self[l]))-8*(strLen/8))/8 + 1
    
    def __str__(self):
        ret = "\t|\t"+"".join(l + "\t"*self._extraTabsNeeded(l, len(l)) for l in self._labels) + "\n" ##assume tabs = 8 spaces, for idle
        ret += "-"*8 + "".join(["-"*(len(l)+8*self._extraTabsNeeded(l, len(l))) for l in self._labels]) +"\n" ##initial tab = 8
        i = 0
        for row in self._table:
            ret += str(i)+"\t|\t" + "".join([str(row[l])+"\t"*self._extraTabsNeeded(l, len(str(row[l]))) for l in self._labels])+"\n"
            i += 1
        return ret[:-1]
    
    def labels(self):
        return self._labels
    
    def __getitem__(self, key):#gets a row, column, or an item by [row, column]
        if type(key)==int:
            return self._table[key]
        elif type(key)==str:
            tmp = self._labels.index(key)##breaks (by design) if the key is not a label
            return [curD[key] for curD in self._table]
        elif type(key)== tuple:
            if type(key[0])==int and type(key[1])==str:
                return (self[key[0]])[key[1]]
            elif type(key[1])==int and type(key[0])==str:
                return (self[key[1]])[key[0]]
            else:
                _raiseDataTableKeyError()
        else:
            _raiseDataTableKeyError()

    def __delitem__(self, key): #deletes a row, column, or clears a specific item
        if type(key)==int: 
            del self._table[key]
            size -= 1
        elif type(key)==str:
            tmp = self._labels.index(key)##breaks (by design) if the key is not a label
            for i in range(self._size):
                del (self._table[i])[key]
            self._labels.remove(key)
        elif type(key)== tuple:
            if type(key[0])==int and type(key[1])==str:
                (self[key[0]])[key[1]] = None
            elif type(key[1])==int and type(key[0])==str:
                (self[key[1]])[key[0]] = None
            else:
                _raiseDataTableKeyError()
        else:
            _raiseDataTableKeyError()
        if self._size == 0:
            self.addNewRow()
            self._size =1
            
    def __setitem__(self, key, value): #sets a row or column with an iterable, and can set a specific item.
        if type(key)==int:
            value = iter(value)##check for iterable and a setup for the for loop
            for l in self._labels:
                try:
                    self._table[key][l] = value.next()#smooth, ain't it? terminates as soon as one exausts
                except StopIteration:
                    break
        elif type(key)==str:
            tmp = self._labels.index(key)##breaks (by design) if the key is not a label
            value = iter(value)
            for i in range(self._size):
                try:
                    self._table[i][key] = value.next()#see above
                except StopIteration:
                    break
        elif type(key)== tuple:
            if type(key[0])==int and type(key[1])==str:
                (self[key[0]])[key[1]] = value
            elif type(key[1])==int and type(key[0])==str:
                (self[key[1]])[key[0]] = value
            else:
                raise KeyError("Key must be a tuple (int, str).")
        else:
            raise KeyError("Key must be a tuple (int, str).")
    def addNewRow(self):
        """Adds a new, empty row to the table."""
        self._size += 1
        self._table.append(dict.fromkeys(self._labels))
    def addNewRows(self, n):
        """Adds n new rows"""
        self._size += n
        self._table.extend(dict.fromkeys(self._labels) for i in range(n))
    def addNewLabel(self, label):
        """Adds a new label"""
        if self[0].has_key(label):
            raise Warning("The table already contains this label")
            return
        self._labels.append(str(label))
        for i in range(self._size):
            (self._table[i])[str(label)] = None
    def addNewLabels(self, *label):
        """Adds a list of new labels"""
        for l in label:
            try:
                self.addNewLabel(l)
            except Warning:
                pass
    def save(self, fileName=None, saveAs=False):
        outStr = "\n".join((str(self._size), str(self._labels), str(self._table)))
        if fileName == None and saveAs == True:
            fileName = save_as()
        elif fileName == None:
            fileName = save_it()
        f = open(fileName, 'w')
        f.write(outStr)
        f.close()
        return fileName

    def load(self, fileName=None):
        if fileName == None:
            fileName = open_it()
        f = open(fileName)
        inStr = f.readlines()
        f.close()
        self._size = eval(inStr[0])
        self._labels = eval(inStr[1])
        self._table = eval(inStr[2])
        
    
