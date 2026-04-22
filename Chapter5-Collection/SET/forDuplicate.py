set={2,3,4,5,6,7}
set2={10,4,6,40,80}

#for print duplicate value
# set.intersection_update(set2)
# print(set)

# print(set.union(set2))#isame pura print hota hai do do bar hai wo bhi atlyst one time to hoga hi
#isase jo common hai wo print nahi hoga baki sab ho jayege
set.symmetric_difference_update(set2)
print(set)