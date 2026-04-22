n=int(input("ENter the number"))
e=1
for i in range(1,n):
    for j in range(1,i+1):
        print(e,end=" ")
        e=e+1
    print(" ")    