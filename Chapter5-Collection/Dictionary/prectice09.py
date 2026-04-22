t={
    "rohit":10,
    "rohan":90,
    "sagar":2000

}
print(t)
print(t["rohit"])
t["faisal"]=7990
print(t)
print(t.keys())
print(t["sagar"])
p={
    "f":583,
    "h":928,
    "y":729
    }
t.update(p)
print(t)

te={
    "d":{
        "a":3,
        "b":5
    },
    "e":{
        "ro":9,
        "to":4
    }

}
print(te["d"]["a"])
t.pop("sagar")
print(t)
t.popitem()
print(t)
p.pop("f")
print(p)
p.popitem()
print(p)

for i in t:
    print(i)


for i in t:
    print(t[i])

for i ,j in t.items():
    print(i,j)
print(len(t))    