#!/usr/bin/python
# Michael Rodrigues (rodrigues.mi@husky.neu.edu)
# CS4800 Fall 2014 Programming Assignment

# Import the sys library to be able to read lines from stdin
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
	# Add an entry to the subordinates list for this employee in case they are a manager
	subordinates.append([])
	# Add this employee ID as subordinate to his/her boss' list of subordinates
	subordinates[bossId].append(empId)
	# Add this employee's value to the values list
	values.append(value)
	# Set this employee's residualEffect (value + residualEffect for his/her boss)
	residualEffect.append(residualEffect[bossId] + value)
	# Add this employee's boss' id
	bossIds.append(bossId)

# id: current employee id, value: boss' value
def fixTree(id, value):
	# Update this employee's residual value to ignore his/her boss' values
	residualEffect[id] = value + values[id]

	# Retrieve the list of the current employee's subordinates
	subList = subordinates[id]

	# If there are no subordinates (BASE CASE)
	if len(subList) == 0:
		# Return the current id, and this employee's residual value (as max too)
		return (id, residualEffect[id], residualEffect[id])

	# Keep track of the maximum as we calculate each subordinate's value
	# Initial maximum is the current employee
	branchMax = residualEffect[id]
	branchMaxId = id
	# For each subordinate
	for subordinate in subList:
		# Compute the residual maximum value
		(subId, subEffect, subBranchMax) = fixTree(subordinate, residualEffect[id])
		# If this subordinate provides the greatest branch maximum
		if subBranchMax > branchMax:
			branchMax = subBranchMax
			branchMaxId = subId

	# If there is a branch that has a greater maximum value than the current employee
	if (not branchMaxId == id):
		# Then this employee's residual value is 0
		residualEffect[id] = 0
	# Update non max influence employees, starting with 0 to ignore their managers' values
	for subordinate in subList:
		# If the current subordinate is the maximum, do nothing
		if subordinate == branchMaxId: continue
		# Otherwise, update the residual value (residualEffect[id] = 0)
		(subId, subEffect, subBranchMax) = fixTree(subordinate, residualEffect[id])
	return (id, residualEffect[id], branchMax)

# Traverses the tree starting from the employee with the given ID.
# Returns (employee's id, employee's residual value, maximum subordinate value)
def scanTree(id):
	# Retrieve the list of the current employee's subordinates
	subList = subordinates[id]

	# If there are no subordinates (BASE CASE)
	if len(subList) == 0:
		# Return the current id, and this employee's residual value (as max too)
		return (id, residualEffect[id], residualEffect[id])

	# Keep track of the maximum as we calculate each subordinate's value
	# Initial maximum is the current employee
	branchMax = residualEffect[id]
	branchMaxId = id
	# For each subordinate
	for subordinate in subList:
		# Compute the residual maximum value
		(subId, subEffect, subBranchMax) = scanTree(subordinate)
		# If this subordinate provides the greatest branch maximum
		if subBranchMax > branchMax:
			# Update the maximum values
			branchMax = subBranchMax
			branchMaxId = subId

	# If there is a branch that has a greater maximum value than the current employee
	if (not branchMaxId == id):
		# Then this employee's residual value is 0
		residualEffect[id] = 0
	# Update non max influence employees, starting with 0 to ignore their managers' values
	for subordinate in subList:
		# If the current subordinate is the maximum, do nothing
		if subordinate == branchMaxId: continue
		# Otherwise, update the residual value (residualEffect[id] = 0)
		(subId, subEffect, subBranchMax) = fixTree(subordinate, residualEffect[id])
	return (id, residualEffect[id], branchMax)

def main():
	# Read the number of employees and the number of employees to influence
	argv = sys.stdin.readline().strip().split(" ")
	argc = len(argv) # Number of arguments
	if (not(argc == 2)): # If we weren't given 2 arguments
		printUsage() # Print the appropriate usage

	# Retrieve the number of employees and the number to influence from line 1
	num_employees = int(argv[argc-2]) # First argument
	num_to_influence = int(argv[argc-1]) # Second argument

	# Read each employee's information
	for i in range(num_employees):
		# Read a line and remove whitespace (new lines) from the end of the line
		line = sys.stdin.readline().rstrip()
		# Split by spaces to get an array of [id, bossId, value]
		vals = line.split(" ")
		# Add the values to the appropriate arrays
		addEmployee(int(vals[0]), int(vals[1]), int(vals[2]))

	# Traverse the tree (divide-and-conquer) starting from root
	scanTree(1)

	# Sort the residual effect values in decreasing order
	residualEffect.sort(reverse=True)

	# Sum the residual values of the employees that have the highest residual
	# influence values
	print sum(residualEffect[0:num_to_influence])

main() # Start the algorithm