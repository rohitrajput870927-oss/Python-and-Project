#isame pata nahi hota hai ki hame kitana value lena hai
def sum(*args):#args is a tuple isleye hame sum karne ke liye  for loop ka use karna par raha hai
    su=0
    for i in args:
        su+=i
    return su
print("Sum is",sum(1,2,3,4,5,6,7,8,797))    
#*args ka jagah pe ham kuch bhi likh sakte hai * ke sath
def p(*s):
    print("Enter the infinete value",s)
p(1,2,3,3,4,2,54,546,7,2,7,262,6,26,262,2,562,65,26,)    

