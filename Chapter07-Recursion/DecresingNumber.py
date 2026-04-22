def num(n):
    if n==0:
        return 
    
    
    print(n)#first me number print ho jayega phir decr hote chala jayega
    num(n-1)
    
n=int(input())
num(n)