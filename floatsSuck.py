def floatsSuck():
    a =(10000000000000000000000/3.0 + .7)*10
    b = 100000000000000000000000/3.0
    c = b + 7
    print "a =(10000000000000000000000/3.0 + .7)*10 = " +str(a)
    print "b = 100000000000000000000000/3.0 = " + str(b)
    print "c = b + 7 = " + str(c)
    print "a - b = " + str(a - b) + "(should be 7...)"
    print "c - b = " + str(c - b) + "(should be 7...)"
    print "a - c = " + str(a - c) + "(should be 0...)"

if __name__ == "__main__":
    floatsSuck()
