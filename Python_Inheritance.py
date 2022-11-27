# Inheritance in python

# Base class aka Parent class

class Person () :
    def __init__(self, name) :
        self.name = name

    def displayDetails(self) :
        print(self.name)

    # By default we can say that particular person is unemployed

    def isEmployed (self) :
        print(self.name, "is un-employed !!")



# Derived class aka Child class

class Employee (Person) :

    def __init__(self, emp_name, id_num, salary, designation) : 
        self.id_number = id_num
        self.emp_salary = salary
        self.emp_designation = designation

        #Calling constructor of Base class
        #Person.__init__(self, emp_name)  one way to achieve

        super().__init__(emp_name)

    def isEmployed (self) :
        print(self.name, "is employed !!")

    def employeeDetails(self) :
        print("Employee Id is ",self.id_number,
         ". Employee salary is ", self.emp_salary, 
         ". Employee designation is ", self.emp_designation)


# emp = Person("Madhu")
# emp.displayName()
# emp.isEmployed()

# emp1 = Employee("Madhu Gamidi")
# emp1.displayName()  # inherited
# emp1.isEmployed()


emp3  = Employee("Madhu", 5432, 100000, "Data Engineer 1")

emp3.displayDetails()
emp3.isEmployed()
emp3.employeeDetails()

