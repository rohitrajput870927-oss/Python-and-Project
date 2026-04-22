#tuple are immutable that why we can not add ,remove or update  the element in tulple thet why we convert tuple into list and then add the element in list and then convert it back to tuple
t=(1,2,3,4,6)
k=list(t)
k.reverse()
print(k)
k.append(5)
print(k)
t=tuple(k)
print(t)

