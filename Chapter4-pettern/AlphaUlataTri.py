n=int(input("Enter the Number"))
for i in range(1,n):
    for j in range(1,n-i+1):
        print((chr)(j+64),end=" ")
    print(" ")    