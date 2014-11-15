#!/usr/bin/python
# Michael Rodrigues (rodrigues.mi@husky.neu.edu)
# CS4800 Fall 2014 Programming Assignment

import sys

# Array where bossIds[0] = 0, bossIds[1] = 0 (CEO's boss), bossIds[<i>] = i's boss' id
bossIds = [0]
# Array where values[0] = 0, values[1] = CEO's Value, values[<i>] = i's value
values = [0]
# Array of arrays where subordinates[1] is the list of subordinates
subordinates = [[]]
# Set max influence effect for each employee
effects = [0]
# Set of Ids of employees we have influenced
influenced = []
# Values of employees as others are chosen
residualEffect = []
# List of tuples of scanned employees
scannedEmployees = []
# Is this employee a max of a branch?
isMax = []


# Prints the correct script usage and exits
def printUsage():
	print "Error: Invalid number of arguments"
	print "  USAGE: python influence.py <number_of_employees> <number_to_influence>"
	sys.exit(1)


# Adds the employee's information to the appropriate array
# O(1) time
def addEmployee(empId, bossId, value):
	subordinates.append([]) # Add this employee to the subordinates list
	subordinates[bossId].append(empId) # Add this employee ID as subordinate to his/her boss
	values.append(value)
	effects.append(effects[bossId] + value)
	bossIds.append(bossId)

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
	#print "Influencing empId: %d" % (empId)
	while(not(empId == 0)):
		influenced[empId] = True
		empId = bossIds[empId]


# Returns the total influence effect that influencing the given employee would have
# This function follows the bossID pointers to calculate the total effect back to the CEO
# Returns a non-negative number
# O(m) time
def employeeInfluenceEffect(empId):
	acc = 0
	while (not(empId == 0)):
		if (not influenced[empId]):
			acc += values[empId]
		empId = bossIds[empId]
	return acc

# id: current employee id, value: boss' value, maxVal: maximum value seen so far
def scanTree(id, value, max):
	if id == 15:
		print value, max
	if (not isMax[id]):
		residualEffect[id] = value + values[id]

	# List of subordinates
	subList = subordinates[id]

	# If no subordinates (BASE CASE)
	if len(subList) == 0:
		return (id, residualEffect[id], residualEffect[id])

	branchMax = residualEffect[id]
	branchMaxId = id
	for subordinate in subList:
		(subId, subEffect, subBranchMax) = scanTree(subordinate, 0 if influenced[id] else effects[id], branchMax)
		if subBranchMax > branchMax:
			branchMax = subBranchMax
			branchMaxId = subId
	isMax[branchMaxId] = True
	for subordinate in subList: # Update non chosen employees, starting with 0 for value
		(subId, subEffect, subBranchMax) = scanTree(subordinate, 0, branchMax)
	residualEffect[id] = 0 # no point influencing a non leaf
	influenced[id] = True
	return (id, residualEffect[id], branchMax)

def main():
	global influenced, residualEffect, isMax
	argv = sys.stdin.readline().strip().split(" ")
	argc = len(argv)
	if (not(argc == 2)):
		printUsage()

	# Retrieve the params from line 1
	num_employees = int(argv[argc-2])
	num_to_influence = int(argv[argc-1])

	# Intialize the influenced array to all False
	influenced = [False] * (num_employees+1)
	isMax = [False] * (num_employees+1)
	residualEffect = [0] * (num_employees+1)

	# Fetch each employee's information
	for i in range(num_employees):
		line = sys.stdin.readline().rstrip()
		vals = line.split(" ")
		addEmployee(int(vals[0]), int(vals[1]), int(vals[2]))

	# If we cannot influence anyone, then value is 0
	if (num_to_influence == 0):
		print 0
	# If we have less employees than we are allowed to influence, then return sum of all values
	elif (num_employees < num_to_influence):
		influenced = [True] * (num_employees+1)
		influenced[0] = False # Cannot influence a non-existent employee
		print calculateInfluenceTotal()

	scanTree(1, 0, 0)
	for i in range(len(residualEffect)):
		# Add (id, effect) tuples to scannedEmployees list
		scannedEmployees.append((i, residualEffect[i]))
	scannedEmployees.sort(key=lambda tup: tup[1], reverse=True) # Decreasing order
	print scannedEmployees
	result = 0
	for i in range(num_to_influence):
		result += scannedEmployees[i][1] # Add the result
	print result

main()