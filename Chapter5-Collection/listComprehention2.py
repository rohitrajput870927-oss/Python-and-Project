# It’s a shorter and cleaner way to create lists.

# Instead of writing a loop and appending items, you can write everything in one line.
list=["ro","to"]
for i in range(1,4):
    nuwlist=[list for i in range(1,4)]
    print(nuwlist)

n=["rohit" for i in range(1,9) ]
print(n)

t=[i for i in range(1,8) if i%2==0]
print(t)

put=[list for i in range(1,9) ]
print(put)


'''
new_list = [expression for item in iterable if condition]

item → variable name you choose for each element in the iterable.

expression → what you want to put in the new list (it can use item, or something else).'''