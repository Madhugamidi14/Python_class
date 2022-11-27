# Function overriding in Python
from math import pi

class Shape :
    def __init__(self, name) :
        self.name = name

    def area(self) :
        pass

    def fact(self) :
        pass

    def whichShape (self) :
        print(self.name)


class Square(Shape) :

    def __init__(self, name, length ) :
        super().__init__(name)
        self.side_length = length


    def area(self) :
        print(self.side_length**2)


    def fact(self) : #overridden function from shape class
        print("Square has each angle equal to 90 degrees") 


class Circle(Shape) :

    def __init__(self, name, radius ) :
        super().__init__(name)
        self.circle_radius = radius


    def area(self) :
        print(pi * (self.circle_radius**2))



sq = Square("Square", 10)
cr = Circle("Circle", 20)


sq.area() # will access area from the square class
cr.area() # will access area from the circle class

sq.fact() # overridden value will be the output
cr.fact() # can be called because it is inherited from shape class but as per the function it will just "pass"


sq.whichShape()
cr.whichShape()

