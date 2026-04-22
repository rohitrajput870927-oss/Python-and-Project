n=int(input("Enter the no."))
sum=0
while n>0:
 ld=n%10
 n=n//10
 sum=sum+ld
print(sum)
