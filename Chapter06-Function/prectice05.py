def fact(n):
    pro=1
    for i in range(1,n+1):
        pro=pro*i
    return pro
#return def ke samne nahi hota hai

n=int(input("Enter the nuomer"))
print(fact(n))    