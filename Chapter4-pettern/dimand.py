n=int(input("Enter the number"))
for i in range(1,n+1):
    for j in range(1,n-i+1):
        print(" ",end=" ")
    for k in range(1,2*i):#n=7 to i=6 tab last wala row 11 hoga
        print("*",end=" ")
    print(" ")        
for i in range(n,0,-1):#n=7 hai to ek kam se suru karege according to upar wala or - karte chalege ok
    for j in range(1,n-i+1):
        print(" ",end=" ")
    for k in range(1,2*i):#n=7 to i=6 tab last wala row 11 hoga
        print("*",end=" ")
    print(" ")            