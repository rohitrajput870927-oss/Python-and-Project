s1=[1,5,5]
s2=[3,4,5,5,10]
s3=[5,5,10,20]
#list ko set me change karna padega kayoki list me intersection nahi hota hia
s4=set(s1)
s5=set(s2)
s6=set(s3)

# set1=s1.intersection_update(s2)#intersection_update iska use ham log tab karte hai jab kisi new set me diplicate value ko upadate na karna ho 
set1=s4.intersection(s5)#duplicate ko kisi new set me store karwana hai to ham ye use karte hai
set2=set1.intersection(s6)
#fir jab ho gaya to set ko list me change kar dege
print(list(set2))