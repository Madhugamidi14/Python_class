# How to create a class in Python

class Employee:
    
    #constructor of a class

    def __init__(self):
        #instance variable or instance attribute
        self.emp_name = None
        self.emp_salary = None

    #method of a class

    def DisplayEmployeeInfo(self):
        print("Employee name : ",self.emp_name, ", Employee_salary : ", self.emp_salary)


emp1 = Employee()
emp2 = Employee()



class Employee:
    
    #constructor of a class

    def __init__(self,name,salary):
        #instance variable or instance attribute
        self.emp_name = name
        self.emp_salary = salary

    #method of a class

    def DisplayEmployeeInfo(self):
        print("Employee name : ",self.emp_name, ", Employee_salary : ", self.emp_salary)


emp1 = Employee("Madhuchandra", 10000)
emp2 = Employee("Gamidi", 20000)

emp2.DisplayEmployeeInfo()


# Difference between class variable and instance variable

class Employee:

    #Class variable
    EmployeeCount = 0
    
    #constructor of a class

    def __init__(self,name,salary):
        #instance variable or instance attribute
        self.emp_name = name
        self.emp_salary = salary
        Employee.EmployeeCount += 1

    #method of a class

    def DisplayEmployeeInfo(self):
        print("Employee name : ",self.emp_name, ", Employee_salary : ", self.emp_salary)


    #method of a class

    def DisplayEmployeeCount(self):
        print("Employee Count : ", Employee.EmployeeCount)


emp1 = Employee("Madhuchandra", 10000)
emp1.DisplayEmployeeInfo()
emp1.DisplayEmployeeCount()

emp2 = Employee("Gamidi", 20000)
emp2.DisplayEmployeeInfo()
emp2.DisplayEmployeeCount()


# What is a static method in python

class car :
    def __init__(self, name, color) :
        self.name = name
        self.car_color = color

    def DisplayCarDetails(self) :
        print("The car name is ", self.name, " and car color is ",self.car_color)


    @staticmethod
    def initialMessage():
        print("Nice car")