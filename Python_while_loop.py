int_list = [1,2,3,4,5,6,7,8,9]
sum = 0
while(int_list):
    sum=sum+int_list
print(sum)


#write a program to print the table of 9

num = 9
counter = 1

while (counter<11):
    ans = num * counter
    print(num, ' * ',counter, ' = ',ans)
    counter = counter+1