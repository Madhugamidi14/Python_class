# Inline functions (anonymous functions)
# Don't need def keyword 

#Syntax : 
#lambda "argument(s)" : expression

#Normal functions

def add(num):
    result = num +10
    return result

x = 20
print(add(10))

"""------------------xxxxxx---------------------"""

# Using lambda functions

lambda_add = lambda x : x + 39
x = 2020

print(lambda_add(x))

"""------------------xxxxxx---------------------"""

# Write a lambda function to add two imput numbers

lambda_add_two_nums = lambda x,y : x + y

x = int(input("Enter value for x: "))
y = int(input("Enter value for y: "))

print(lambda_add_two_nums(x,y))

"""------------------xxxxxx---------------------"""

# write a lambda function to calculate maximum of two numbers

lambda_max_two_nums = lambda x , y : x if x > y else y

x = 10
y = 20

print(lambda_max_two_nums(x,y))

"""------------------xxxxxx---------------------"""

# map() usage

list1 = [1,2,3,4,5]

square_num = lambda x : x*x

square_list = list(map(square_num, list1))

print(square_list)

"""------------------xxxxxx---------------------"""

# Add sequential respective elements in two given lists

list_a = [1,2,3,4,5]
list_b = [5,4,3,2,1]

sum_two_elements  = lambda x,y : x+y

result = list(map(sum_two_elements, list_a,list_b))

print(result)

"""------------------xxxxxx---------------------"""

# Using reduce()  n inputs gives single output

import functools

list_x = [1,2,3,4,5]

add_two_num = lambda x,y : x + y

result = functools.reduce(add_two_num,list_x)

print(result)

"""------------------xxxxxx---------------------"""

# filter() usage filters based on logic


seq = [1,2,5,6,9,7,10]

filter_odd = lambda x : x % 2 != 0

result = list(filter(filter_odd, seq))

print(result)

"""------------------xxxxxx---------------------"""