from node import Node
import random as rnd
import numpy as np
import sys
import matplotlib.pyplot as plt	

# N0 = 5													# number of sample of people you take out of first generation to base your tree on
# N = 5												# total number of people in each generation 


N1 = Node('a', 0, [], None)
N2 = Node('a', 0, [], None)
N3 = Node(None, 15, [N1, N2], None)
N4 = Node('c', 0, [], None)
N5 = Node(None, 27, [N3, N4], None)
N6 = Node('d', 0, [], None)
print(N1.name)
# print(N1.myroot.find([0,0]))
# print(N1)
# newN1 = N1.copy()
# print(newN1.name)
# print(newN1.height)
# print(newN1.children)
# print(newN1.parent.name)
# print(newN1.parent.height)
# print(newN1.parent.parent)
# print(N1 == N1)
# N1.__eq__()


# list of methods:
#		- evolve: creates the tree once the Tree object is initiated
#		- printtreegraph: draws the tree in a rectangular form
# 		- printbracketform: returns tree in backet form
#		- leaveslist: returns list of number of leaves each node has
#		- sequences: returns a list of sequences places at each nodes, where the sequence 
#					in the root is all zeros, while its children have randomly mutated sequences
#		- metric: returns a matrix of distances between leaves of the tree
