r=input("Enter the string")
n=int(input("enter the number"))

a="abcdefghijklmnopqrstuvxyz"
rev=a[ : :-1] #[starting:ending:step]
dec1=dict(zip(a,r))
print(dec1)

prefix=r[0:n-1]
sufix=r[n-1:]

