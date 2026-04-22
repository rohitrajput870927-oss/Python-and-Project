def fect(n):
    pro=1
    for i in range(1,n+1):
        pro=pro*i
    return pro
n=int(input("Enter the number"))


print(fect(n))    
