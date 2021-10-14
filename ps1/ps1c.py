# Gabriel Munoz
# Wednesday, September 16, 2020

# MIT OCW Intro to Python & CS
# Problem Set 1c - Finding the right amount to save away

import math

# User inputs - only the annual salary - the percent of salary saved, cost of dream home, and semi-annual raise are set
annual_salary = float(input("Enter the starting salary: "))

# Initialize the rest of the variables - we will vary starting salaries and find the percent of salary to save
total_cost = 1000000
portion_down_payment = 0.25
down_payment = total_cost*portion_down_payment
current_savings = 0
r = 0.04
semi_annual_raise = 0.07
portion_saved = 0.0
low = 0
high = 10000
steps = 0
# know bisection search converges in log2(high) steps (round up)
# in this case log2(10000) = ~13.2877 -- so need the 14th step to  check the last integer in 0-10000
max_steps = math.ceil(math.log(high, 2))

# exit the loop once we are withing $100 or once bisection search has converged
while abs(current_savings - down_payment) >= 100 and steps < max_steps:
    # initialize savings and salary
    current_savings = 0
    sal = annual_salary
    # guess for bisection search
    guess = int((low + high) / 2)
    # save money for 36 months
    for month in range(1, 37):
        current_savings += (guess/10000)*(sal/12) + current_savings*r/12
        # get a raise every 6 months
        if month % 6 == 0:
            sal += semi_annual_raise*sal
    # bisection search - check if guess of portion saved was too low or high
    if current_savings > down_payment:
        # if saved too much, savings rate has to go down
        high = guess
    else:
        # if saved too little, savings rate has to go up
        low = guess
    # count number of steps in bisection search
    steps += 1

if abs(current_savings - down_payment) >= 100:
    print("It is not possible to pay the down payment in three years.")
else:
    print("Best savings rate: " + str(guess/10000))
    print("Steps in bisection search: " + str(steps))
