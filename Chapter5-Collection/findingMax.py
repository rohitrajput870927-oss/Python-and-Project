n=int(input())
list=[]
for i in range(n):
    num=int(input())
    list.append(num)
print(list)   
l=list[0]
for i  in range(0,n):
    if list[i]>l:
        l=list[i]
print(l)   

P=list[0]
for i in range(0,n):
    
    if list[i]>P:
        if list[i]!=l:
            P=list[i]
print(P)            