# Gabriel Munoz
# Wednesday, September 2, 2020

# MIT OCW Intro to Python & CS
# Getting Started

import math

math.cos(math.pi)

# 34*x^2 + 68*x - 510
# find the root of the above quadratic? (-b +- sqrt(b^2 - 4*a*c))/(2*a)
x1 = (-68 + math.sqrt(68**2 - 4*34*(-510)))/(2*34)
print("The root of 34*x^2 + 68*x - 510 is " + str(x1) + ".\n")

# Check?
check = 34*x1**2 + 68*x1 - 510
print("'x1' = " + str(x1) + " is a root of 34*x^2 + 68*x - 510 since 'check' = " + str(check) + ".\n")

# sine, cosine expression - should be equal to 1 - it's the trig identity cos^2(x) + sin^2(x) = 1
a = math.cos(3.4)**2 + math.sin(3.4)**2
print("The expression 'a' = " + str(a) + " should be equal to 1.\n")

# Of course this couldn't be missing!

print("Hello world")
