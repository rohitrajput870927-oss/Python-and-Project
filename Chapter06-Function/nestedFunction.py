def a():
    x=9

    def b():
        y=10
        result=x+y
        return result  #dusare wale function ka return  
    
    return b()#pahale wala function ka return

print(a())