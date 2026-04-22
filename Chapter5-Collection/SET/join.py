set={1,2,3,4,5,6}
print(set)
set2={6,"ro","fo","co","ho"}
print(set2)

print(set.union(set2))
#upadate ka bhi use kar ke ham log join kar sakte hai
set.update(set2)
print(set)

#for print duplicate value
set.intersection_update(set2)
print(set)