n=int(input("Enter the Number"))
r=0
while n>0:
    ld=n%10
    r=r*10
    r=r+ld
    n//=10
print(r)
    # n//=10
    # print(ld)