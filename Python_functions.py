# Functions in Python

list1 = [1,2,3,4,5,6]
print("Maximum number from the list is : ",max(list1))

def welcome_message():
    print("Welcome to iNeuron Big Data batch - 2")
    return "123"

welcome_message()



def bot_message():
    return "Message from bot !!"

print(bot_message())

def avg_of_two_nums(a,b):
    avg_result = (a+b)/2
    return avg_result

num1 = 10
num2 = 15
output = avg_of_two_nums(num1,num2)
print(output)


def avg_of_two_nums(a,b):
    avg_result = (a+b)//2
    return avg_result

num1 = 10
num2 = 15
output = avg_of_two_nums(num1,num2)
print(output)


# write a function to calculate the factorial of a num

import math  
def fact(n):  
    return(math.factorial(n))  
  
num = int(input("Enter the number:"))  
f = fact(num)  
print("Factorial of", num, "is", f) 


def square_and_cube(n):
    sqr = n*n
    cube = n*n*n
    return sqr, cube

num = 4
sqr_ans , cube_ans = square_and_cube(num)
print(sqr_ans)
print(cube_ans)


# How to create optional arguments in python functions

def multiply(a,b=3):
    result = a*b
    return result

num1 = 5
num2 = 10

print(multiply(num1,num2))
print(multiply(num1))
print(multiply(num2))


# NON-KEY valued arguments

def example_nonkeyed_args(*argv):
    for param in argv:
        print(param)

result = example_nonkeyed_args('Hello','Welcome','to','iNeuron')
print(result)

# Key Value type of aruguments in Python

def example_of_kvargs(**kvargs):

    for k,v in kvargs.items():
        print("Key is ",k, " and Value is ",v)

example_of_kvargs(host="170.80.80.80", port = 9021, pswd='cgbdh')


def example_of_kvargs(**kvargs):

    print("Value of port is ", kvargs['host'])
    print("Value of port is ", kvargs['port'])
    print("Value of port is ", kvargs['pswd'])

    #for k,v in kvargs.items():
        #print("Key is ",k, " and Value is ",v)

example_of_kvargs(host="170.80.80.80", port = 9021, pswd='cgbdh')