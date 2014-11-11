#!/usr/bin/python
# Michael Rodrigues (rodrigues.mi@husky.neu.edu)
# CS4800 Fall 2014 Programming Assignment

import sys

# Array where bossIds[0] = 0, bossIds[1] = 0 (CEO's boss), bossIds[<i>] = i's boss' id
bossIds = [0]
# Array where values[0] = 0, values[1] = CEO's Value, values[<i>] = i's value
values = [0]
# Set max influence effect for each employee
effect = []
# Set of Ids of employees we have influenced
influenced = []
# Array of values for the optimal solution. Opt[num_employees+1] is optimal
opt_values = []


# Prints the correct script usage and exits
def printUsage():
	print "Error: Invalid number of arguments"
	print "  USAGE: python influence.py <number_of_employees> <number_to_influence>"
	sys.exit(1)


# Adds the employee's information to the appropriate array
# O(1) time
def addEmployee(empId, bossId, value):
	bossIds.append(int(bossId))
	values.append(int(value))


# Computes and returns the total influence value computed by the algorithm
# O(n) time
def calculateInfluenceTotal():
	acc = 0
	for empId in range(len(influenced)):
		if influenced[empId]: # If this employee was influenced
			acc += values[empId]
	return acc


# Given an employee id, this function adds the ids of all employees that would be influenced
# to the 'influenced' set.  This prevents duplicates from occurring, ensuring correctness
# O(m) time
def influence(empId):
	while(not(empId == 0)):
		influenced[empId] = True
		empId = bossIds[empId]


# Returns the total influence effect that influencing the given employee would have
# This function follows the bossID pointers to calculate the total effect back to the CEO
# Returns a non-negative number
# O(m) time
def employeeInfluenceEffect(empId):
	acc = 0
	while(not(empId == 0)):
		acc += values[empId]
		empId = bossIds[empId]
	return acc


def findOpt(i, j): # the optimal solution for employees 1...i with up to j influences
	global opt_values

	# Base Cases
	if j == 0: return 0
	if i <= 0: opt_values[i][j] = 0
	if i == 1: opt_values[i][j] = values[i]

	excluding = opt_values[i-1][j]
	including = values[i] + opt_values[bossIds[i]][j]
	opt_values[i][j] = max(excluding, including)

def main():
	global influenced, opt_values
	argv = sys.stdin.readline().strip().split(" ")
	argc = len(argv)
	if (not(argc == 2)):
		printUsage()

	# Retrieve the params from line 1
	num_employees = int(argv[argc-2])
	num_to_influence = int(argv[argc-1])

	# Intialize the influenced array to all False
	effect = [0] * (num_employees+1)
	influenced = [False] * (num_employees+1)
	# The following line is causing the program to run extremely slow on large inputs:
	#opt_values = [[0 for x in range(num_to_influence + 1)] for x in range(num_employees + 1)]

	# Fetch each employee's information
	for i in range(num_employees):
		line = sys.stdin.readline().rstrip()
		vals = line.split(" ")
		addEmployee(vals[0], vals[1], vals[2])

	# If we cannot influence anyone, then value is 0
	if (num_to_influence == 0):
		print 0
	# If we have less employees than we are allowed to influence, then return sum of all values
	elif (num_employees < num_to_influence):
		influenced = [True] * (num_employees+1)
		influenced[0] = False # Cannot influence a non-existent employee
		print calculateInfluenceTotal()

	# Find optimal solutions
	for i in range(0, num_employees+1):
		opt_values.append([0] * (num_to_influence + 1))
		for j in range(1, num_to_influence+1):
			findOpt(i, j)

	print opt_values[num_employees][num_to_influence]


main()