# Michael Rodrigues (rodrigues.mi@husky.neu.edu)
# CS4800 Fall 2014 Programming Assignment

import sys

# Array where bossIds[0] = 0, bossIds[1] = 0, bossIds[<i>] = i's boss' id
bossIds = []
# Array where values[0] = CEO's value, values[<i>] = i's value
values = []

def printUsage():
    print "Error: Invalid number of arguments"
    print "  USAGE: python influence.py <number_of_employees> <number_to_influence>"
    sys.exit(1)

def addEmployee(empId, bossId, value):
    bossIds.append(int(bossId))
    values.append(int(value))

def sumValues(l):
  return sum(l)

def main():
    argc = len(sys.argv)
    if (not(argc == 3)):
        printUsage()

    # Retrieve the params from line 1
    num_employees = int(sys.argv[argc-2])
    num_to_influence = int(sys.argv[argc-1])

    # Fetch each employee's information
    for i in range(num_employees):
        line = sys.stdin.readline()
        (empId, bossId, value) = line.split(" ")
        addEmployee(empId,bossId, value)

    # If we have more employees than we are allowed to influence, then return sum of all values
    if (num_employees < num_to_influence):
            print sumValues(values)

main()