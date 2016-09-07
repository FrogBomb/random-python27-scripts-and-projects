    
class monoid:
    def __init__(self, typesToGenerateFrom):
        self._rMap = monoidRelationMap(baseMonoid)
        self._baseTypes = [i for i in typesToGenerateFrom]
        self._injectedElements = []

    def injectElement(self, newElement):
        self._injectedElements.append(newElement)

    def injectType(self, newType):
        self._baseTypes.append(newType)

    def areElements(self, *elements):
        return True

    def dot(self, a, b):
        return monoidProduct(self, a, b)

class monoidProduct:
    def __init__(self, baseMonoid, *elements):
        self._bM = baseMonoid
        if not isinstance(baseMonoid, monoid):
            raise TypeError("baseMonoid must be a monoid")
        if not baseMonoid.areElements(elements):
            raise TypeError(\
                "One of the element arguements is not an element of the baseMonoid")
        self._data = []
        for el in elements:
            if isinstance(el, monoidProduct):
                self._data += [i for i in element._data]
            else:
                self._data.append(el)
        self.simplify()

    def simplify(self):
        return

    def __len__(self):
        return len(self._data)

    def __mul__(self, other):
        if isinstance(other, monoidProduct):
            if self._bM == other._bM:
                ret = monoidProduct(self._bM, self)
                ret._data += other._data
                return ret
            else:
                raise TypeError
        else:
            if not self._bM.areElements(other):
                raise TypeError
            else:
                ret = monoidProduct(self._bM, self, other)
                return ret


class monoidRelationMap:
    def __init__(self, baseMonoid):
        self._bM = baseMonoid
        self._map = dict()
        self._data = []

    def addMap(self, a, b):
        if not self._bM.areElements(a, b):
            raise ValueError
        try:
            indexA = self._data.index(a)
        except ValueError:
            indexA = len(self._data)
            self._data.append(a)
            self._map[indexA] = set()
        try:
            indexB = self._data.index(b)
        except ValueError:
            indexA = len(self._data)
            self._data.append(b)
            self._map[indexB] = set()

        self._map[indexA].add(indexB)
        self._map[indexB].add(indexA)

    def __call__(self, element):
        try:
            index = self._data.index(element)
        except ValueError:
            return []
        return [self._data[i] for i in self._map[index]]

            
            
