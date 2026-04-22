a=int(input("Enter the Frist Number"))
b=int(input("Enter the second Number"))
operator=input("Enter the Operator")
match operator:
    case '+':
        print("Sum of Two Number ",a+b)
        
    case '-':
        print("Difference between two Number",a-b)
    case'*':
        print("Multiply two Number",a*b)
    case '/':
        print("Divide two number" ,a/b)
    case default:
        print("Invalid Operator")
            

