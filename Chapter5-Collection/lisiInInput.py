n=int(input("Enter the size of list"))#kitna size hoga
list=[]#list ko initialized karege
for i in range(n):#loop ko n tak chalayege
    num=int(input())#element input lege
    list.append(num)#element ko add karage append ka use kar ke
print(list)  

k=int(input("Enter the size"))
fruit=[]
for i in range (k):
    name=str(input())
    fruit.append(name)
print(fruit)  
#for swaping  
idx1=int(input("Enter the index1"))#input lege jo index ko swap karna hai unako
idx2=int(input("Enter the index2"))
temp=fruit[idx1]
fruit[idx1]=fruit[idx2]
fruit[idx2]=temp
print(fruit)

