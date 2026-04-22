cp=float(input("Enter the cost Price"))
sp=float(input("Enter the selling Price"))
if cp>sp:
    print("Seller get loss of:",cp-sp )
elif cp<sp:
    print("Seller get Profite of:",sp-cp)
else:
    print("Seller is not in profite and not in loss")
