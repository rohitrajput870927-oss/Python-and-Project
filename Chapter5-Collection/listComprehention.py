fruit=["apple","Mango","Money"]
print(fruit)
newlist=[fruit for fruit in fruit if "a" in fruit]#new list banana jisame existing list ke element ko add krana hota hai tab  to ham list comprihention ka use karte hai
#sntax me for loop fir if ka  use kiye hai log fruit starting wala new list me element add karne ke liye hota hai
print(newlist)

newfruit=fruit.copy()#same to same print karwane ke liye hota hai
print(newfruit)


