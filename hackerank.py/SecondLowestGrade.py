
n=int(input())
li=[]
for i in range(n):
    name=input()
    grade=float(input())
    li.append([name,grade])
print(li)    
grades=list(set(grade for name,grade in li))#pahale grade ko set me  convert kiya taki duplicate na rahe fir usko list  me convert kar diya
grades.sort()#isako sort kar diya
second_lowest=grades[1]#sort hone ke bad second lowest index 1 pe hoga eg=[10,20,30,40] to 20 index 1 pe hoga
for name,grade in sorted(li):# name  and grade ko sorted kar diya taki alphabetically print ho
    if grade==second_lowest:
        print(name)
