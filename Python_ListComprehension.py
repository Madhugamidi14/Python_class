# Syntax: 

# newlist = ["expression(x)" "for x in old_list" "if check"] #3 parameters can be passed

#list comprehension

result = [x for x in range(1,11)]

print(result)

"""------------------xxxxxxxxxx--------------------"""

# get all the even  numbers between 1 to 50

result = [x for x in range(1,51) if x % 2 == 0]

print(result)

"""------------------xxxxxxxxxx--------------------"""

# get all the even  numbers from given list

list_a = [1,2,3,4,5,6,7,8,9,10]

result = [x for x in list_a if x % 2 == 0]

print(result)

"""------------------xxxxxxxxxx--------------------"""

#convert given string into upper case in the given list

list_1 = ['Hi', 'Hello', 'bye', 'nice']

result = [x.upper() for x in list_1]

print(result)

"""------------------xxxxxxxxxx--------------------"""

# Put all negative numbers after positive numbers from given list

list_a = [1,-1,2,-5,9,10,-6]

result = [x for x in list_a if x > 0] + [x for x in list_a if x < 0]
print(result) 