n=int(input("Enter the number"))
for i in range(1,n):
    for j in range(1,i+1):
        print((chr)(j+64),end=" ")
    print(" ")    
