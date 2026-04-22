import random
print(random.random())#index print karata hai
print(random.randint(1,8))#rendom no. b/w 1 to 8 in integer
print(random.uniform(1,6))#rendom no. b/w  1 to 6 in float

n=["apple","pet","hug"]
print(random.choice(n))#picks a random item from a list

nums = [1, 2, 3, 4]
random.shuffle(nums)#randomly rearranges a list
print(nums)
