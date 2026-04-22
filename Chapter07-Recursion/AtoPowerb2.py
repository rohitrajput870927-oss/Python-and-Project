#2^4=2^2*2^2 for even
#2^5=2^2*2^2*2 for odd
def pow(a,b):
    if b==0:
      return 1
    z=pow(a,b//2)
    if b%2==0:
        return z*z
    if b%2!=0:
        return z*z*a
a=int(input("Enter the number:"))
b=int(input("Enter the number:"))
print(pow(a,b))    

        