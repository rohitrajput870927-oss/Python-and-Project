s={5,9,390,20,10}
print(s)
for i in s:
    print(i)
s.add(100)
print(s)
set2={10,20,30,40,50}
s3=s.intersection(set2)
print(s3)

s.intersection_update(set2)
print(s)
s.symmetric_difference_update(set2)
print(s)
s.union(set2)
print(s)
