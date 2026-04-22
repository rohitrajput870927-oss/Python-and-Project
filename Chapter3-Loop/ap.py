# a+(n-1)d
n=int(input("Enter the no. of term"))
a=int(input("Enter the First term"))
d=int(input("Enter the difference"))
for i in range(0,n,1):#n+1 isliye kiya gaya hai ki n tak hame element lena hai 
    print(a+i*d)