#element ko access karwane ke liye 
def s(*args):
    for i in args:
        print(i)

s(1,2,3,4,45,5)    

def p(*args):
    sum=0
    for i in args:
        sum=sum+i
    return sum
print(p(100,10,20,10,30,40,50,60,70,80))

def d(*args):
    pro=1
    for i in args:
        pro=pro*i
    return pro    

print(d(90,100,900,200,210))        
    
