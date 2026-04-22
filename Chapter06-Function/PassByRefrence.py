def l(h):
    h.append(4)#origanal object ka refrence hi  copy nahi hai
    print("Inside the Function",h)
h=[1,2,3]#isi ko function me as it is pass kiya ja raha hai
l(h)#call hua hai function
print("Outside the function",h)   