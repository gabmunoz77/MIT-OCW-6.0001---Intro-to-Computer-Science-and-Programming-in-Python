# Gabriel Munoz
# Wednesday, September 16, 2020

# MIT OCW Intro to Python & CS
# Problem Set 1a - House Hunting

# User inputs - annual salary, percent of salary saved, and cost of dream home
annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))

# Initialize state variables - portion of cost down payment will be, current savings, annual return rate
portion_down_payment = 0.25
current_savings = 0
r = 0.04

# At the end of each month, savings will increase by a percentage of monthly salary and returns on investments
# Need to find the number of months it'll take to save the down payment - which depends on variables
# Increment savings until they are greater than or equal to the down payment (cost*portion)
# Count the number of months as the number of iterations of a while loop
months = 0
while current_savings < total_cost*portion_down_payment:
    current_savings += portion_saved*(annual_salary/12) + current_savings*r/12
    months += 1

# Print the number of months
print("Number of months: " + str(months))
