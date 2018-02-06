from Tree import *
from pexp import * 
from DistMatr import *
from sample import *
from scipy.special import hyp2f1, binom, gamma
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##############################################################################
################################### STUFF ####################################
##############################################################################

def Test(MT, mu, n):
    """
    Input:  - MT, a MetricTree object (for now only 3 leaf)
            - mu, a float between 0. and 1., rate of mutation 
            - n, a positive integer, length of genotypes
    Output: array of probabilities of each possible combinatorial trees
            of same leaf number as the input MetricTree, given sample
            grown on the MetricTree with genotypes of length n and mutated
            with rate mu 
            corresponding combinatorial trees:
            - (a,b),c
            - (a,c),b
            - (b,c),a
    """
    # create sample on given tree
    SAMPLE = Sample.FromTree(MT, mu, Genotype(n))
    # print('Sample', SAMPLE)
    # create matrix from sample
    MATRIX = DistanceMatrix.FromSample(SAMPLE)
    keys = MATRIX.keys
    A = MATRIX[keys[0], keys[1]]
    B = MATRIX[keys[0], keys[2]]
    C = MATRIX[keys[1], keys[2]]
    ELEM = [A, B, C]
    # print('ELEM', ELEM)
    # print('MATRIX', MATRIX)
    k = int((A + B - C) / 2)
    m = int((B + C - A) / 2)
    l = int((A + C - B) / 2)
    TOTCHANGES = k + m + l
    # creating array of probabilities for each combinatorial tree
    PROB = np.zeros(3)
    for i in range(3):
        PROB[i] = (hyp2f1(1 + ELEM[i], 2 + TOTCHANGES, 2 + ELEM[i], -2) / 
                   (1 + ELEM[i]))
    PROB = PROB / sum(PROB)
    return PROB

def ArrayBuilding(t2, t1_start, mu, n, TRAILS):
    """
    Input:  - t2, positive float, the height of the three leaf tree
            - t1_start, positive float, less than t2, height of lower node of 
            tree
            - mu, float between 0 and 1, rate of mutation
            - n, positive integer, length of genotype
            - TRAILS, positive integer, number of trails done for each t1 to 
            gather enough statistic on the probabilities
    Output: five quantities: three arrays of probabilities for type 1, type 2
            and type 3 trees, array of heights of t1 for which the 
            probabilities were found, and value of t1 when for the first time
            the real type of the tree was not the most probable type.
    """
    # initializing leaves 
    L1 = Tree.MetricTree([], None, 0., 'a')
    L2 = Tree.MetricTree([], None, 0., 'b')
    L3 = Tree.MetricTree([], None, 0., 'c')

    # type 1
    array = np.linspace(t1_start, t2, 50, endpoint=False)
    num = len(array)
    PROB_TYPE_1 = np.zeros(num)
    PROB_TYPE_2 = np.zeros(num)
    PROB_TYPE_3 = np.zeros(num)
    T = np.zeros(num)
    index = 0

    breakpnt = 0
    for t1 in array:
        N1 = Tree.MetricTree([L1, L2], None, t1)
        N2 = Tree.MetricTree([N1, L3], None, t2)
        PROB = np.zeros(3)
        for i in range(TRAILS):
            PROB += Test(N2, mu, n)
        PROB = PROB / TRAILS
        PROB_TYPE_1[index] = PROB[0]
        PROB_TYPE_2[index] = PROB[1]
        PROB_TYPE_3[index] = PROB[2]
        if breakpnt == 0 and (PROB[0] <= PROB[1] or PROB[0] <= PROB[2]):
            breakpnt = t1/t2
        T[index] = t1/t2
        index += 1
    return PROB_TYPE_1, PROB_TYPE_2, PROB_TYPE_3, T, breakpnt

def PlotGraphs(t2, t1_start, mu, n, TRAILS = 1000):
    """
    Input:  - t2, positive float, the height of the three leaf tree
            - t1_start, positive float, less than t2, height of lower node of 
            tree
            - mu, float between 0 and 1, rate of mutation
            - n, positive integer, length of genotype
            - TRAILS, positive integer, number of trails done for each t1 to 
            gather enough statistic on the probabilities
    Output: plots four graphs of probabilites of type 1, type 2, type 3 for 
            given t2 and mu, and then t2*10 and mu/10, t2*10**2 and mu/10**2,
            and t2*10**3 and mu/10**3, with breaking point indicated by a 
            vertical line.
    """

    sns.set(style="whitegrid")
    
    plt.figure(1)
    
    PROB_TYPE_1, PROB_TYPE_2, PROB_TYPE_3, T, breakpnt = ArrayBuilding(t2, t1_start, mu, n, TRAILS)
    
    plt.title('$t_2 =$ ' + str(t2) + ', $\mu =$ ' + str(mu) + ', $n =$ ' + str(n) + 'breakpoint = ' + str(breakpnt))
    plt.plot(T, PROB_TYPE_1, 'b', label = 'Type ((a,b),c) Probability')
    plt.plot(T, PROB_TYPE_2, 'c', label = 'Type ((a,c),b) Probability')
    plt.plot(T, PROB_TYPE_3, 'g', label = 'Type (a,(b,c)) Probability')
    plt.axvline(x = breakpnt, color = 'k', linestyle = '--')
    plt.xlabel('Ratio of smaller height to bigger height: t1/t2.')
    plt.ylabel('Probability')
    
#     plt.figure(2)
    
#     PROB_TYPE_1, PROB_TYPE_2, PROB_TYPE_3, T, breakpnt = ArrayBuilding(t2*10, t1_start*10, mu/10, n, TRAILS)
    
#     plt.title('$t_2 =$ ' + str(t2*10) + ', $\mu =$ ' + str(mu/10) + ', $n =$ ' + str(n) + 'breakpoint = ' + str(breakpnt) )
#     plt.plot(T, PROB_TYPE_1, 'b', label = 'Type ((a,b),c) Probability')
#     plt.plot(T, PROB_TYPE_2, 'c', label = 'Type ((a,c),b) Probability')
#     plt.plot(T, PROB_TYPE_3, 'g', label = 'Type (a,(b,c)) Probability')
#     plt.axvline(x = breakpnt, color = 'k', linestyle = '--')
#     plt.xlabel('Ratio of smaller height to bigger height: t1/t2.')
#     plt.ylabel('Probability')
    
#     plt.figure(3)
    
#     PROB_TYPE_1, PROB_TYPE_2, PROB_TYPE_3, T, breakpnt = ArrayBuilding(t2*10**2, t1_start*10**2, mu/10**2, n, TRAILS)
    
#     plt.title('$t_2 =$ ' + str(t2*10**2) + ', $\mu =$ ' + str(mu/10**2) + ', $n =$ ' + str(n) + 'breakpoint = ' + str(breakpnt) )
#     plt.plot(T, PROB_TYPE_1, 'b', label = 'Type ((a,b),c) Probability')
#     plt.plot(T, PROB_TYPE_2, 'c', label = 'Type ((a,c),b) Probability')
#     plt.plot(T, PROB_TYPE_3, 'g', label = 'Type (a,(b,c)) Probability')
#     plt.axvline(x = breakpnt, color = 'k', linestyle = '--')
#     plt.xlabel('Ratio of smaller height to bigger height: t1/t2.')
#     plt.ylabel('Probability')
    
#     plt.figure(4)
    
#     PROB_TYPE_1, PROB_TYPE_2, PROB_TYPE_3, T, breakpnt = ArrayBuilding(t2*10**3, t1_start*10**3, mu/10**3, n, TRAILS)
    
#     plt.title('$t_2 =$ ' + str(t2*10**3) + ', $\mu =$ ' + str(mu/10**3) + ', $n =$ ' + str(n) + 'breakpoint = ' + str(breakpnt) )
#     plt.plot(T, PROB_TYPE_1, 'b', label = 'Type ((a,b),c) Probability')
#     plt.plot(T, PROB_TYPE_2, 'c', label = 'Type ((a,c),b) Probability')
#     plt.plot(T, PROB_TYPE_3, 'g', label = 'Type (a,(b,c)) Probability')
#     plt.axvline(x = breakpnt, color = 'k', linestyle = '--')
#     plt.xlabel('Ratio of smaller height to bigger height: t1/t2.')
#     plt.ylabel('Probability')
    
    plt.show()
