f=open("D:\PYTHON\Chapter09-FileHendling\do.txt","w")#append karwane ke liye hota hai append means hota hai ki last me kuchh add karna 
data=f.write('''Hello i am rohit kumar singh .And i am readig python from college wallah 
             And some point from Apana college and chatGptHello 
             i am rohit kumar singh And i am now doing BCA from Glgotias university
             Hello i am rohit kumar singh And i am now doing BCA from Glgotias university''')

print(data)
f.close()