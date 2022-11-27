# List is a heterogeneous kind of data 
# sequential data
# stored in continous memory location
# every thing is treated as an element
# first in last out

a=[1,2,3,4,5,6,7,8]

a.pop()

print(a)

a.append(8) # append only takes one argument

print(a)

a1 = [1,2,3]
a1.extend([4,5,6]) # multiple values to append
print(a1)

int_list = []
for num in range(1,1001):
    int_list.append(num)

print(int_list)

a=[1,2,3,4,6,7]
print(len(a))

list1 = [1,"Madhu",20, "Hi"]
list2 = [1,"Madhu",20, "Hi"]

print(list1==list2)


list4 = [1,2,3,4,5]
list5 = [80,90,100,110]
list6 = list4 + list5  
print(list6)

b = [1,2,3,4,5,6,7,8,9]

for i in b:
    if i%3==0:
        print("Element found for index 3 is: ", i)
        break

list11 = [1, "madhu", 2 , "chandra"]
list11[1] = "MADHU"

print(list11)

list1=[1,2,3]
list2=[1,2,3]

list1.append(list2)
print(list1)

list1.extend(list2)
print(list1)

# List slicing

a=[1,2,3,4,5,6]

print(a[0:3])

#print list in reverse order
list1 = [1,2,3,4,5]
print(list1[-1::-1])  # step paramater is positive by default so we need to provide the step as negative

