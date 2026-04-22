n=int(input("Enter the no."))
if n%2==0:
    print("the no. is divisible by 2")
elif n%3==0 or n%15==0:
    print("the no. is divisible by 3")    
else:
    print("the no. is not divisible by 2 or 3")