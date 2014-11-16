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

# Resets the influenced value to False for employee with id = id and all subordinates
def reset(id):
	influenced[id] = False
	for sub in subordinates[id]:
		reset(sub)

# id: current employee id, value: boss' value, maxVal: maximum value seen so far
def scanTree(id, value, max):
	print (id, value, max)
	if (value + values[id] > max):
		residualEffect[id] = value + values[id]
	else:
		residualEffect[id] = values[id]

	# List of subordinates
	subList = subordinates[id]

	# If no subordinates (BASE CASE)
	if len(subList) == 0:
		return (id, residualEffect[id], residualEffect[id])

	branchMax = residualEffect[id]
	branchMaxId = id
	print [effects[id], residualEffect[id]]
	for subordinate in subList:
		(subId, subEffect, subBranchMax) = scanTree(subordinate, 0 if influenced[id] else effects[id], branchMax)
		if subBranchMax > branchMax:
			branchMax = subBranchMax
			branchMaxId = subId
	branchMaxIndex = subList.index(branchMaxId) if branchMaxId in subList else 0

	residualEffect[id] = 0 # no point influencing a non leaf
	for subordinate in subList[0:branchMaxIndex]: # Update non max influence employees, starting with 0 for value
		print str(id) + " fixing sub via " + str((subordinate, residualEffect[id], branchMax))
		(subId, subEffect, subBranchMax) = scanTree(subordinate, residualEffect[id], branchMax)
	return (id, residualEffect[id], branchMax)

def main():
	global influenced, residualEffect
	argv = sys.stdin.readline().strip().split(" ")
	argc = len(argv)
	if (not(argc == 2)):
		printUsage()

	# Retrieve the params from line 1
	num_employees = int(argv[argc-2])
	num_to_influence = int(argv[argc-1])

	# Intialize the influenced array to all False
	influenced = [False] * (num_employees+1)
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
	for (id, effect) in scannedEmployees[0:num_to_influence]:
		result += effect # Add the result
	print result

main()