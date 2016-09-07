from Useful_Algorithms import memo, timer

@memo
def f(L, M, c, k):
    if L == M:
        return 1
    const = c*(M+1)**.5 - k
    fact = None
    if const>1:
        fact = 1
    elif const>-1:
        fact =.5
    else:
        return 0
    return fact*.5*(f(L, M+1, c, k+1)+f(L, M+1, c, k-1))
