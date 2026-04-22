with open("D:\PYTHON\Chapter09-FileHendling\do.txt","r") as f:
    data=f.readline()
    print(data)
    data=f.readline()
    print(data)
    data=f.readline()
    print(data)

with open("D:\PYTHON\Chapter09-FileHendling\do.txt","w") as f:
    print(f.write("Hello everyone my name is Rohit kumar singh And i am now doing BCA from Galgotias university"))      

with open("D:\PYTHON\Rohit.txt","r") as f:
    d=f.read()
    print(d)
# with statement automatically closes the file after the block of code is executed

