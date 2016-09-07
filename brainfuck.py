class BFError(StandardError):
    pass

class brainfuck:
    def __init__(self, size):
        self._data = [0]*size
        self._pointer = 0
    def _incPointer(self):
        self._pointer += 1
    def _decPointer(self)
        if self._pointer == 0:
            return
        else:
            self._pointer -= 1
    def _inc(self):
        self._data[self._pointer]+=1
    def _dec(self):
        self._data[self._pointer]-=1
    def _output(self):
        return self._data[self._pointer]
    def _input(self, value):
        self._data[self._pointer] = value
    def _isZero(self):
        return self._data[self._pointer]==0
    def _isNotZero(self):
        return self._data[self._pointer]!=0
    def _goToLeftBrac(self, code, curInstrPtr):
        ret = curInstrPtr
        bracCount = 1:
        while(bracCount>0):
            ret -= 1
            if ret < 0:
                raise BFError
            elif code[ret] == "]":
                bracCount += 1
            elif code[ret] == "[":
                bracCount -= 1
            
        return ret
            
    def _goToRightBrac(self, code, curInstrPtr):
        ret = curInstrPtr
        bracCount = 1:
        cLen =  len(code)
        while(bracCount>0):
            ret += 1
            if ret >= cLen:
                raise BFError
            elif code[ret] == "]":
                bracCount -= 1
            elif code[ret] == "[":
                bracCount += 1
        return ret
    
    def __call__(self, code):
        instrPtr = 0
        bracDepth = 0
        while(instrPtr<len(code)):
            if code[instrPtr] == ">":
                self._incPointer()
            elif code[instrPtr] == "<":
                self._decPointer()
            elif code[instrPtr] == "+":
                self._inc()
            elif code[instrPtr] == "-":
                self._dec()
            elif code[instrPtr] == ".":
                print self._output()
            elif code[instrPtr] == ",":
                self._input(int(raw_input("Give a number: ")))
            elif code[instrPtr] == "[":
                if(self._isZero()):
                    instrPtr = self.goToRightBrac(code, instrPtr)
            elif code[instrPtr] == "]":
                if(self._isNotZero()):
                    instrPtr = self.goToLeftBrac(code, instrPtr)
            instrPtr += 1
        
