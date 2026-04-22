def d():
    x=0
    def f():#ye dusara function hai na jo ki d()ke inside me hai
        r=9
        r=r+x
       
        return r   
    return f()#thatwhy ham jab bhi return karege to f()
print(d())
