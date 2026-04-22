n=int(input("Enter the size of list"))
list=[]
for i in range(n):
    num=int(input("Enter the number"))
    list.append(num)
print(list)    
list.insert(3,10)
print(list)
list2=[80,57,90]
print(list2)
list.extend(list2)
print(list)
list[2]=60000
list[3]=8000
list[4]=9000
print(list)
list.sort()
print(list)
l=list[0]
for i  in range(0,n+1):
    if list[i]>l:
        l=list[i]
print(l)   
