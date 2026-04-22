t=(3,5,7,9,1,10)
list=[]
for i in reversed(t):
    list.append(i)
t=tuple(list)
print(t)    
p=("rohit","Rohan","Faisal","Sagar")
l=[]
for i in reversed(p):
    l.append(i)
p=tuple(l)    
print(p)

for i in t:
    print(i)
r,R,F,S=p
print(R)    

