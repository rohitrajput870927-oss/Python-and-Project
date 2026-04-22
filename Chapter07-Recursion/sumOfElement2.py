def add(n,s):
    if n==0:
       return s
    
    return n+add(n-1,s)
n=int(input())
print(add(n,0))