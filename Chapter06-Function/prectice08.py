
def sum(n):
    sum=0
    for i in range(n):
        print(i)
    
n=int(input("enter the number"))
print("All the number")
sum(n)

def add(n):
    som=0
    for i in range(1,n+1):
        som=som+i
    return som
print("Sum of element is:",add(10))    