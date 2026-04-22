# list=[1,2,3,[5,6,7],8,9,0]
# print(list)
# print(list[0])
# print(list[3])
# print(list[3][0])

# print(list[3][1][2])   wrong
#how to make a nested list
list=[1,2,3,4,5,6]
print(list)
list.insert(2,[10,20,30,40])
print(list)
print(list[2])
print(list[2][0])
print(list)
#swaping
idx1=0#jis index ko swap karna hai un dono ko lege
idx2=4
temp=list[idx1]
list[idx1]=list[idx2]
list[idx2]=temp
print(list)