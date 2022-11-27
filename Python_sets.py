# Sets in python

set1 = set()
print(type(set1))

list1 = [1,2,3,4,5]

set2 = set(list1)
print(type(set2))
print(set2)

#set is unordered collection of elements. Indexing wont work
#set doesnot support duplicates. Only distinct values are taken

list1 = [1,1,1,2,2,2,3,4,5,5,5,5,6,7,8,8,8,9]
set3 = list(set(list1))
print(set3)

#how to insert elements into set

set4 = set()
set4.add(1)
set4.add(1)
set4.add(1)
set4.add(2)
set4.add(2)
set4.add(2)
set4.add(3)

print(set4)

# use of update menthod

tmp = [1,2,3,4,5,6,7,7,7,7,8,8,8,8,8,9,9]
set4.update(tmp)
print(set4)

#Calculate the length of the set

print(len(set4))

# Set operations

set_a = {1,2,3,4,5,6}
set_b = {3,6,8,9,10}

# union operation

print(set_a | set_b)

# intersect operation

print(set_a & set_b)

# A-B # Difference in sets

print(set_a - set_b)
print(set_a - set_b)

