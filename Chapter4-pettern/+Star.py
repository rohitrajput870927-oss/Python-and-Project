n=int(input("Enter the number"))
mid=n//2-1
for i in range(1,n):
    for j in range(1,n):
        if i==mid and j==mid:
            print("*",end=" ")
    print(" ")        
        