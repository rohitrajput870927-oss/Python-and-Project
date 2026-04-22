n=int(input("enter the number of students"))
li=[]
for i in range(n):
    name=input()
    score=float(input())
    li.append([name,score])
print(list)   
grades=sorted(set(score for name,score in li))
second_largest=grades[1]
l_name=[name for name,score in li if score==second_largest]

for li in sorted(l_name):
    print(li)