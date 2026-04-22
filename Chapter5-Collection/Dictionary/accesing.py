phone={
    "rohit":8709,
    "sagar":7422,
    "faisal":90321
}
#accesing karne ke liye hota hai
print(phone)
print(phone["rohit"])
print(phone["sagar"])

print(phone.get("rohit"))#isaka bhi use accesing karne ke liye hi hota hai
print(phone.get("sagar"))
print(phone.get("faisal"))

print(phone["faisal"])