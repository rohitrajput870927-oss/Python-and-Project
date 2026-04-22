phone={
    "rohit":2442,
    "sagar":45953,
    "faisal":9484
}
for i in phone:
    print(i)#ya sirf key ko print karega

for i in phone:
    print(phone[i])    #sirf value ko print karwata hai
    
#isase dono print ho jayega
for i,j in phone.items():
    print(i,j)