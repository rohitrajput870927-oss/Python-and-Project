#replace is use to replace the substrig with new substring
#syt=string.replace("oldsubstring","newstring",count)
#count agar ham de rehe hai to us name ka pahala occarence delete hoga baki sab rahega or agar nahi de rehe hai to pura delete ho jayega
name="sagar is a goood boy"
n1=name.replace("boy","girl")
print(n1)

name2="hello world ,what a beaytiful world "
print(name2.replace("world","earth",1))


name3="hello world, what a beautyful world"
n3=name3.replace("world","earth")#hamesa ke liye change nahi hota hai bas n3 ke liye change hua hai
print(n3)
print(name3)