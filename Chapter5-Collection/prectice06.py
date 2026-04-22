l=int(input("Enter the size"))
list=[]
for i in range(l):
    num=int(input())
    list.append(num)
print(list)
idx1=int(input())
idx2=int(input())
temp=list[idx1]
list[idx1]=list[idx2]
list[idx2]=temp
print(list)