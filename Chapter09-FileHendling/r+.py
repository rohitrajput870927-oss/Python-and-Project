f=open("D:\PYTHON\Chapter09-FileHendling\do.txt","r+")#ye jo hai na wo starting wale pe overread ho jata hai
data=f.write("\nRohan is a gohkhorwa boy")
print(data)
print(f.read())#jitana overread hua hai utana chhod dega usake bad se read hoga 

f.close()