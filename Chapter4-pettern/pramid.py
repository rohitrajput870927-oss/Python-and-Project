n=int(input("Enter the number"))
for i in range(1,n):
    for j in range(1,n-i+1):
        print(" ",end=" ")
    for k in range(1,2*i):#n=7 to i=6 tab last wala row 11 hoga
        print("*",end=" ")
    print(" ")        
