def leap(n):
    if n%4==0:
        print("True")
    else:
        print("False")
       
n=int(input())
leap(n)

def is_leap(year):
    if year%4==0:
        return True
    else:
        return False     
   
year = int(input())
print(is_leap(year))#return hai isliye ham log print use kar rahe hai
           