def fec(n):
    if n==1:
        return 1
    return n*fec(n-1)
n=int(input("Enter the number:"))
print(fec(n))