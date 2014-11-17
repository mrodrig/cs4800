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
# Values of employees as others are chosen
residualEffect = [0]
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
	residualEffect.append(residualEffect[bossId] + value)
	bossIds.append(bossId)

# id: current employee id, value: boss' value
def fixTree(id, value):
	residualEffect[id] = value + values[id]

	# List of subordinates
	subList = subordinates[id]

	# If no subordinates (BASE CASE)
	if len(subList) == 0:
		return (id, residualEffect[id], residualEffect[id])

	branchMax = residualEffect[id]
	branchMaxId = id
	for subordinate in subList:
		(subId, subEffect, subBranchMax) = fixTree(subordinate, residualEffect[id])
		if subBranchMax > branchMax:
			branchMax = subBranchMax
			branchMaxId = subId

	residualEffect[id] = 0 # no point influencing a non leaf
	for subordinate in subList: # Update non max influence employees, starting with 0 for value
		if subordinate == branchMaxId: continue # skip this branch
		(subId, subEffect, subBranchMax) = fixTree(subordinate, residualEffect[id])
	return (id, residualEffect[id], branchMax)

# id: current employee id, value: boss' value
def scanTree(id, value):

	# List of subordinates
	subList = subordinates[id]

	# If no subordinates (BASE CASE)
	if len(subList) == 0:
		return (id, residualEffect[id], residualEffect[id])

	branchMax = residualEffect[id]
	branchMaxId = id
	for subordinate in subList:
		(subId, subEffect, subBranchMax) = scanTree(subordinate, residualEffect[id])
		if subBranchMax > branchMax:
			branchMax = subBranchMax
			branchMaxId = subId

	residualEffect[id] = 0 # no point influencing a non leaf
	for subordinate in subList: # Update non max influence employees, starting with 0 for value
		if subordinate == branchMaxId: continue # skip this branch
		(subId, subEffect, subBranchMax) = fixTree(subordinate, residualEffect[id])
	return (id, residualEffect[id], branchMax)

def main():
	argv = sys.stdin.readline().strip().split(" ")
	argc = len(argv)
	if (not(argc == 2)):
		printUsage()

	# Retrieve the params from line 1
	num_employees = int(argv[argc-2])
	num_to_influence = int(argv[argc-1])

	# Fetch each employee's information
	for i in range(num_employees):
		line = sys.stdin.readline().rstrip()
		vals = line.split(" ")
		addEmployee(int(vals[0]), int(vals[1]), int(vals[2]))

	scanTree(1, 0)
	residualEffect.sort(reverse=True) # Decreasing order
	print sum(residualEffect[0:num_to_influence])

main()