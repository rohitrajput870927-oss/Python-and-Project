f=open("D:\PYTHON\Chapter09-FileHendling\do.txt","r")
data=f.readline()#line read karne ke liye hota hai jitana line read karna hoga utana bar  read line likhana padega
print(data)
data=f.readline()
print(data)
print(type(data))
f.close()