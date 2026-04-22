f=open("D:\PYTHON\Chapter09-FileHendling\do.txt", "r")#r ka use read karne ke liye hota hai
data=f.read()
print(data)
print(type(data))
f.close()