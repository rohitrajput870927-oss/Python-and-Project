#dekho function kuchh nahi hai jo ham log normal code me karte hai log usako hi hamlog function ke inside me likhate hai log
#like for fectorial
n=int(input("Enter the no."))
pro=1
for i in range(1,n+1):
    pro=pro*i
print(pro)    

#now same thing in function 
def fect(n):#n uprar bhi leye hai input ke liye 
    pro=1
    for i in range(1,n+1):
        pro=pro*i
    return pro #isake jagah pe ham print bhi use kar sakte hai
n=int(input("Enter the number"))
print(fect(n))    
#same to same jo bahar me tha usako function ke inside me print karwa diya gaya


def fect(n):
    pro=1
    for i in range(1,n+1):
        pro=pro*i
    print("Print ka use hua hai isleye sirf call hoga",pro) 

fect(5) #function call 

#agar ham return kar rahe hai to function ke bahar me ham print ke andar function cal karege
#or baki w3school se learn kar lena