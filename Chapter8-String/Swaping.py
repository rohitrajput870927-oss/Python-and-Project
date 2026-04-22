# def sap(s):
#     result=" "
#     for i in s:
#         if i.islower():
#          result+=i.upper()
#         elif i.isupper():
#             result+=i.lower()
#     return result
# s=input("enter the string")
# print(sap(s))        

def sap(s):
    return s.swapcase()#builting property
s=input("enter the string")
print(sap(s))