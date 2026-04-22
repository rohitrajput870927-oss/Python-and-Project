def sta(n):
    if n==1 or n==2:
        return n
    return sta(n-1)+sta(n-2)#n -1 matlab n=5 hai to ab 4 ho jayege matlab ek step chadha hai
n=int(input())
print(sta(n))
