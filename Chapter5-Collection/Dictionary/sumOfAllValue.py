p={
    "a":1,
    "b":2,
    "c":3
}
print(p)
#function ka use kar ke ham log sum karte hai
print(sum(p.values()))

#loop chalayege value print karwane ke liye phir usaka sum kar dege

sum=0
for i in p:
    sum=sum+p[i]
print(sum)    


