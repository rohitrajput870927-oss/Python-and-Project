newlist=[ "rohit" for i  in range(1,4)]
print(newlist)

p=[i for i in range(1,11)] #jo value apko rakhana hai who pahale likhege
print(p)

t=[i for i in range(1,11) if i%2==0]
print(t)

u=[t for newlist in newlist if "o" in newlist]

print(u)



