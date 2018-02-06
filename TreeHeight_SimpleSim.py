import numpy as np
import random as rnd
import sys
import scipy.optimize


def hidden_trees(n, N, rho):
    """
    Input:  - n, a positive integer, length of genome
            - N, a positive integer, size of each generation
            - rho, a positive float between 0 and 1, rate of 
            recombination
    Output: - list of positive floats of length n, which is a
            list of heights built from a Markov process inspired
            by height of ancestral trees of loci on genomes.
            - a list of positive integers (less than n), that 
            correspond to recombination sites in the 'genome'
    """
    hidden_tree_list = np.zeros(n, dtype = float)
    recomb_list = []
    t_0 = np.random.exponential(N)
    hidden_tree_list[0] = t_0
    for i in range(1, n):
        t_prev = hidden_tree_list[i - 1]
        recombination_toss = np.random.uniform(0,1)
        if recombination_toss < np.exp(-2 * rho * t_prev):
            t_i = t_prev
        else:
            t_i = np.random.exponential(N) 
            recomb_list.append(i)
        hidden_tree_list[i] = t_i
    return hidden_tree_list, recomb_list

def observables(tree_list, mu):
    """
    Input:  - tree_list, a list of positive floats, heights of 
            trees
            - mu, a float between 0 and 1, rate of mutation
    Output: a list of 0's and 1's derived from the input tree_list
            which signify, based on the height at each index of 
            input list, whether the loci of two different genomes put
            on the ends of a 2-tree with the given height have same
            or different values (0 for same, 1 for different)
    """
    n = len(tree_list)
    obs_list = np.zeros(n, dtype = int)
    for i in range(n):
        t_i = tree_list[i]
        mutation_toss = np.random.uniform(0,1)
        if mutation_toss < np.exp(-2 * t_i * mu):
            d_i = 0
        else:
            d_i = 1
        obs_list[i] = d_i
    return obs_list



    

        