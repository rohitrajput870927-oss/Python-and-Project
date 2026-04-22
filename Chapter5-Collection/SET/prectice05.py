set={"ro","g","f","do"}
print(set)
set3={4,7,5}
set.update(set3)
print(set)

set3={'g','f','u'}
set8={'5','02','g','f'}
print(set3.union(set8))

set3.symmetric_difference_update(set8)
print(set3)