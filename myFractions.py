def _gcd(n, m):
    n = n%m
    if(n < m):##swaps n and m
        n ^= m
        m ^= n
        n ^= m
    ##value setup##
    while(m!=0):
        k = n%m
        n = m
        m = k
    return n

def mod_exp(n, p, mod):
    """returns (n**p)%mod efficiently"""
    k = bin(p)
    n = n%mod
    if(n == 0):
    	return 0 		#exit
    ptr = 1
    ret = 1
    while(k[-ptr] != 'b'):
    	if(n == 1):
    		return ret 	#exit
    	if(k[-ptr] == '1'):
    		ret = (ret*n)%mod
    	n = (n**2)%mod
    	ptr = ptr + 1
    return ret 			#exit


class fraction:
    """Takes a numerator and a denominator and provides tools for
    estimation of the fraction numerator/denominator"""
    def __init__(self, numerator, denominator):
        self._den = denominator
        self._num = numerator
        
    def numerator(self):
        return self._num
    
    def denominator(self):
        return self._den
        
    def __str__(self):
        return str(self._num)+"/"+str(self._den)
    
    def __mul__(self, other):
        if isinstance(other, int):
            return fraction(self._num*other, self._den)
        return fraction(self._num*other._num, self._den*other._den)
    
    def __rmul__(self, other):
        return fraction.__mul__(self, other)

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, long):
            other = fraction(other, 1)
        return fraction(self._num*other._den+self._den*other._num, self._den*other._den)

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, long):
            other = fraction(other, 1)
        return fraction(self._num*other._den-self._den*other._num, self._den*other._den)

    def __radd__(self, other):
        return fraction.__add__(self, other)
    
    def floor(self):
        return self._num/self._den

    def makeReduced(self):
        """Reduces the fraction"""
        gcd = _gcd(self._num, self._den)
        self._num /= gcd
        self._den /= gcd
        
    
    def estimate(self, digits):
        """Estimates the fraction to the specified number of digits.
            This funcion returns a str."""
        ret = str(self.floor())+"."
        div = self._den #the divider
        cur = (self._num%div)*10 #the current thing to divide
        if(cur == 0):
            return ret[:-1]
        while(digits>0):
            if(cur == 0):
                return ret #will just keep being 0's
            ret += str(cur/div) #cats the next digit
            cur = (cur%div)*10
            digits-=1
        return ret
    
    def estimate_generator(self, fromDig = 0, blockSize = 1):
        if fromDig <= 0:
            ret = str(self.floor())+"."
            div = self._den #the divider
            cur = (self._num%div)*(10**blockSize) #the current thing to divide
            yield ret
##            if(cur == 0):
##                for r in ret:
##                    yield r
##                while(True):
##                        yield "0"
##            for r in ret:
##                yield r
        else:
            div = self._den #the divider
            cur = ((mod_exp(10, fromDig, div)*self._num)%div)*10**blockSize
                    ##current thing to divide
        while(True):
            if(cur == 0):
                while(True):
                    yield "0"*blockSize #will just keep being 0's
            curRetStr = str(cur/div)
            yield "0"*(blockSize-len(curRetStr))+ curRetStr #cats the next digit
            cur = (cur%div)*10**blockSize
            
    def binEst_generator(self, fromBit=0):
        if fromDig <= 0:
            ret = bin(self.floor())[2:]+"."
            div = self._den #the divider
            cur = (self._num%div)*2 #the current thing to divide
            if(cur == 0):
                for r in ret:
                    yield r
                while(True):
                        yield "0"
            for r in ret:
                yield r
        else:
            div = self._den #the divider
            cur = ((mod_exp(2, fromBit, div)*self._num)%div)*2
                    ##current thing to divide
        while(True):
            if(cur == 0):
                while(True):
                    yield "0" #will just keep being 0's
            if cur<div:
                yield "0"
                cur *= 2
            else:
                yield "1"
                cur-=div
            
    def estimateUntilRepeat(self):
        """Estimates the fraction to the point where it will repeat
            This funcion returns a str."""
        ret = str(self.floor())+"."
        div = self._den #the divider
        cur = (self._num%div)*10 #the current thing to divide
        curList = [cur] #list of values cur has been
        repIndex = -1 #default to remain in while loop
        if(cur == 0):
            return ret[:-1]
        while(repIndex == -1):
            if(cur == 0):
                return ret #will just keep being 0's
            ret += str(cur/div) #cats the next digit
            cur = (cur%div)*10
            try:#Trys to see if cur was repeated, and then get index
                repIndex = curList.index(cur)
            except ValueError: ##keep estimating!
                pass
            curList += [cur]
        return ret + "(" + ret[repIndex+len(str(self.floor()))+1:]+ "..." + ")" 
