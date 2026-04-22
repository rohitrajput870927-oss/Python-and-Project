def maz(cr,cc,er,ec):
    right=0
    downt=0
    if cr==er and cc==ec:
        return  1
    if cr==er:
        right=right+maz(cr+1,cc,er,ec)
        
    if cc==ec:
        downt=downt+maz(cr,cc+1,er,ec)
       
    if cr<er:
        right+=maz(cr+1,cc,er,ec)
        downt+=maz(cr,cc+1,er,ec)
       
       
    total=right+downt
    return total
n=int(input())
m=int(input())
print(maz(1,1,n,m)) 
