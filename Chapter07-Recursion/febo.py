def feb(n):
    if n==0 or n==1:
        return   n
    
    return feb(n-1)+feb(n-2)
n=int(input("Enter the number:"))
print(feb(n))