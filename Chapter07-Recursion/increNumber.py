def inc(n):
    if n==0:
        return
    inc(n-1)#pahale 1 print karne ke liye hai phir chalate rahega
    print(n)
n=int(input())
inc(n)    