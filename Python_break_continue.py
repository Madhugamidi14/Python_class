# How to use break statement

int_list = [1,5,7,8,19,13,17,3]

for i in int_list:
    print("Current element of the list", i)
    if(i%2==0):
        print("Even number is found in the list:", i)
        break


int_list = [1,5,7,8,19,13,17,3]

for i in int_list:
    print("Current element of the list", i)
    if(i%2==0):
        print("Even number is found in the list:", i, "ignored it")
        continue

a=[]
for num in range(1,21):
    if num<10:
        continue
    list.append(a,num)
print(a)
