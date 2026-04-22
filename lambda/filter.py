#filter kisi bhio statement me se jo true hota hai use print karwata hai 
num=[1,2,3,4,5,6,7,8,9,10]
h= list(filter(lambda a: a %2==0,num))
print(h)

#odd
h=list(filter(lambda a:a % 2!=0,num))
print(h)

#greater no.
num2=[5,8,2,22,77,113,92,4,0,7,6]
h=list(filter(lambda a:a > 10,num2))
print(h)

#name
names = ["Aman", "Ravi", "Ankit", "Shyam", "Aisha"]
c=list(filter(lambda x:x.startswith("A"),names))#startswith is use to show the first element
print(c)




