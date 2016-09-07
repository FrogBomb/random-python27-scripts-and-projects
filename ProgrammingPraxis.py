###CountingOnes
def COf(n):
    ret = 0
    for i in range(0,n+1):
        while(i!=0):
           tmp = i%10
           i/=10
           if tmp==1:
               ret+=1
    return ret

def findCOfisN():
    ret = 0
    j = 0
    while(True):
        i = j
        while(i!=0):
           tmp = i%10
           i/=10
           if tmp==1:
               ret+=1
        if ret == j:
            yield j
        j+=1
