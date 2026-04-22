def num(x):
    x=x+2#copy of x
    print("Inside the function",x)
#pass by value hai that why koi change nahi hua
x=8#x ka hi copy object pass hua hai function me x nahi hua hai 
num(x)#call hua hai function ka
print("Outside the function",x)