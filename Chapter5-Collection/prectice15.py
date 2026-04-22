list=[55,33,66,22,80]
l=list[0]
for i in range(0,5):
    if list[i]>l:
     l=list[i]
print(l) 
list2=[80,57,90,70,33]
idx1=int(input("Enter the index1"))
idx2=int(input("ENter the index2"))
temp=list2[idx1]
list2[idx1]=list2[idx2]
list2[idx2]=temp
print(list2)
print(len(list2))
list2.remove(70)
print(list2)
list2.pop(1)
print(list2)
list2.pop()
print(list2)
list2.clear()
print(list2)
print(list.count(80))
