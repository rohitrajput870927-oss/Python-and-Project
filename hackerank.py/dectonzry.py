t={
    "m":[7,3,4,3],
    "n":[3,4,5,6],
    "o":[5,6,7,8]
}
print(t["m"])
o=len(t["m"])
print(t)
sum=0
for i in t["m"]:
    sum=sum+i
print(sum//o)    
#print(f"{average:.2f}") ye two decimal k liye hoga
    