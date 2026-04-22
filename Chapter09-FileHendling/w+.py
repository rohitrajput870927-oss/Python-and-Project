f=open("D:\PYTHON\Rohit.txt","w+")#it is open for reading and writing .And it also truncate tha file means khali kar deta hai file ko 
data=f.read()
print(data)
d=f.write("Hello")
print(d)
f.close()