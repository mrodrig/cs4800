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
def scanTree(id, value, maxVal):
	# If another employee has already been seen with higher influence overall
	if (maxVal > (value + values[id])):
		effects[id] = values[id]
	else: # This is the highest employee seen so far
		effects[id] = value + values[id]

	# List of subordinates
	subList = subordinates[id]

	# If no subordinates (BASE CASE)
	if len(subList) == 0:
		return (id, effects[id], effects[id], 0)

	maxId = 0
	maxEffect = effects[id]
	for indx in range(len(subList)):
		subordinate = subList[indx]
		(subId, subEffect, subMax, subMaxId) = scanTree(subordinate, effects[id], maxEffect)
		if (subEffect > maxEffect):
			maxEffect = subEffect
			maxId = subId
			# recur on previous subordinates with new max
			#print id, indx, subList[0:0 if indx == 0 else indx], subId
			for prevSub in subList[0:0 if indx == 0 else indx]:
				(prevSubId, prevSubEffect, prevMax, prevId) = scanTree(prevSub, effects[id], maxEffect)
				#print residualEffect[prevSubId], prevSubEffect
				residualEffect[prevSubId] = prevSubEffect
		residualEffect[subId] = subEffect
	if maxEffect > effects[id]: # if choosing a subordinate is better, this node's residual value becomes 0
		residualEffect[id] = 0
	return (id, residualEffect[id], maxEffect, maxId)

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

	print "scanning"
	scanTree(1, 0, 0)
	print "sorting"
	for i in range(len(residualEffect)):
		scannedEmployees.append((i, residualEffect[i]))
	scannedEmployees.sort(key=lambda tup: tup[1], reverse=True) # Decreasing order
	print scannedEmployees

main()