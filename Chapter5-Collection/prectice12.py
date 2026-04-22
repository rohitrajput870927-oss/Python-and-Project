list=[1,5,7,9,2]
n=len(list)
print(n)
u=list[0]
for i in range(1,n+1):
    if list[i]>u:
        list[i]=u
print(u)        