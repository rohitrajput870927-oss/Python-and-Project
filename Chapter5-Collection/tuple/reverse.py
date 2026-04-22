l=(4,3,2,6,8,9)
print(l)
# list=[]#tuple ko reverse karne ke liye hame list ko initialized karna parta hai kayoki tuple inmutable hota hai
# for i in reversed(l):#ya par reverse function ka use ha hai
#     list.append(i)#list me append karwaya gaya hai
#     print(list)
# l=tuple(list)#phir list ko tuple me badla gaya hai
# print(l)

t=list(l)
print(t)
t.reverse()
print(t)
l=tuple(t)
print(l)
