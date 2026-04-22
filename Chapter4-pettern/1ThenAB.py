n=int(input("Enter the number"))
for i in range(1,n):
    for j in range(1,i+1):#i+1 hota hai hamesa
        if i%2==0:
            print((chr)(j+64),end=" ")
        else:
            print(j,end=" ")  
    print(" ")          