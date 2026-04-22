n=int(input("Enter the no."))
for i in range(n-1,1,-1):
    if n%i==0:
        print(i)
        break
   