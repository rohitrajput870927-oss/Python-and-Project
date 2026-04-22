num=[(1,2),(4,5),(7,8),(10,6),(5,70)]
sort=sorted(num,key=lambda a:a[1])  #a[1] means the second element in that tuple
print(sort)

num2=(4,9,0,2,8)
sort=sorted(num2)
print(sort)

num3=[(1,2),(8,9),(90,100),(4,8),(7,60)]
sort=sorted(num3,key=lambda a:a[1])
print(sort)