# Gabriel Munoz
# Wednesday, September 9, 2020

# MIT OCW Intro to Python & CS
# Problem Set 0

# import numpy for log function (the basic math library also has it)
import numpy

# 1 - ask user to enter a number "x"
x = input("Enter number x: ")

# 2 - ask user to enter a number "y"
y = input("Enter number y: ")

# 3 - print out "x" raised to power of "y"
print("x**y = " + str(float(x)**float(y)))

# 4 - print out the log base 2 of "x"
print("log(x) = " + str(float(numpy.log2(float(x)))))
