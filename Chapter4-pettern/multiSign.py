n=int(input("Enter the number"))
for i in range(1,n):
    for j in range(1,n):
        if i==j or i+j==n:
            print("*",end=" ")
    print(" ")        
