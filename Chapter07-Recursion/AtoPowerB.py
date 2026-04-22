def pow(a,b):
    if b==1:
        return a
    if b==0:
        return 1
    return a*pow(a,b-1)

a=int(input("Enter the number"))
b=int(input("Enter the number:"))
print(pow(a,b))