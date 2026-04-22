def op(**kwargs):
    print("Enter the dec")
    for i,j in kwargs.items():
        print(i,j)
op(r="rohit",u="rohan",t=3)    


def o(**kwargs):
    print("Enter the decs:")
    for i in kwargs:
        print(i)

o(t="rwnjsd",u=2,i="sfmc") 
   
def my_function(**kid):
  print("His last name is " + kid["lname"])

my_function(fname = "Tobias", lname = "Refsnes")

