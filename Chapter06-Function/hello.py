def prin():
 print("Hello Rohit!!")
 
prin()
#defaylt
def g(a=10,b=10):
 r=a*b
 return r

print(g()) 
#fectorial

def fect(n):
   pro=1
   for i in range(1,n+1):
       pro=pro*i
   return pro
n=int(input()) 
print(fect(n)) 
#kewword parameter
def t(x):
  x=67
  return x
x=9
t(x)
print(x)

def l(lis):
  lis.append(134)
  return lis
lis=[1,2,3,4,5]
print(l(lis))





