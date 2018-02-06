import random as rnd
import numpy as np
from Tree import *

##############################################################################
##############################################################################
############################## MULTITREE OBJECT ##############################
############################################################################## 
##############################################################################


class MultiTree:
    
    
##############################################################################
############################### INITIALIZATION ###############################
############################################################################## 


    def __init__(self, trees):
        self.__trees = trees            # list of Trees

        
##############################################################################
############################ ATTRIBUTE PROPERTIES ############################
############################################################################## 
        
        
    @property
    def trees(self):
        return self.__trees
    
    
##############################################################################
############################### STATIC METHODS ###############################
############################################################################## 


    @staticmethod
    def tree_tie(leaf, root):
        """
        Acts on:    a MultiTree class or object
        Input:      - leaf, a MetricTree which is a leaf
                    - root, a MetricTree which is a root
        Output:     modifies tree that the leaf belongs to by linking all 
                    the children of the root to the leaf
        Type:       staticmethod
        """
        while len(root.children) > 0:
            child = root.children[0]
            root._unlink(child)
            leaf._link(child)
            
            
##############################################################################
################################### METHODS ##################################
############################################################################## 
    def __str__(self):
        string = ''
        for tree in self.trees:
            string += 'Tree: ' + tree.__str__() + ' Parent: ' + tree.name + '\n'
            for child in tree.children:
                string += '  Child: ' + child.name + '\n'
                for child2 in child.children:
                    string += '    Child: ' + child2.name + '\n'
        return string
    
    def copy(self):
        """
        Acts on:    a MultiTree object
        Input:      none
        Output:     a MultiTree object equivalent (but not same) as the 
                    original MultiTree
        """
        trees = []
        for tree in self.trees:
            trees.append(tree.copy())
        return MultiTree(trees)
    
    def delete(self):
        """
        Acts on:    a MultiTree object
        Input:      none
        Output:     modifies the object by deleting all the trees within it
        """
        for tree in self.trees:
            tree.delete()
            
    def __repr__(self):
        string = 'MultiTree([' 
        for tree in self.trees:
            string += tree.__repr__() + ','
        string = string[:-1]
        string += '])'
        return string
        
    
    def is_name_tree_in_mult(self, name):
        """
        Acts on:    a MultiTree object 
        Input:      name, a string
        Output:     True if a tree exists inside the MultiTree with the input 
                    name; False if such tree does not exist inside the 
                    MultiTree
        """
        for tree in self.trees:
            if tree.name == name:
                return True
        return False
    
    def name_tree_in_mult(self, name):
        """
        Acts on:    a MultiTree object
        Input:      name, a string
        Output:     a MetricTree if a MetricTree with the input name as its 
                    name exists within the MultiTree. None is no such 
                    MultiTree exist (we are talking about name of root)
        """
        for tree in self.trees:
            if tree.name == name:
                return tree
        return None
    
    def add_to_trees(self, tree):
        """
        Acts on:    MutliTree object
        Input:      tree, a MetricTree
        Output:     modifies the MultiTree by adding the tree to its list of
                    trees
        """
        self.__trees.append(tree)
    
    def __iadd__(self, other):
        """
        Acts on:    MultiTree object, bottom MultiTree (can be 
                    multigenerational)
        Input:      - other, a MultiTree object, with trees of height 1, that 
                    will be added on top
        Output:     MultiTree that is combination of self and other where 
                    other is added on top of self, by placing roots of self on 
                    corresponding leaves of other MultiTree
        Short form: self += other
        """         
        if len(self.trees) == 1:
            return self
        top_mult = other
        bottom_mult = self
        for tree_top in top_mult.trees[:]:
            for child in tree_top.children[:]:
                name = child.name
                root = bottom_mult.name_tree_in_mult(name)
                if root is None:
                    if len(tree_top.children) == 1:
                        top_mult.__trees.remove(tree_top)
                        tree_top.delete()
                    else:
                        child.delete()
                else:
                    self.tree_tie(child, root)
        top_mult.trees[:] = [x for x in top_mult.trees if len(x.children) > 0]
        for tree in top_mult.trees:
            for child in tree.children[:]:
                if len(child.children) == 1:
                    child_of_child = child.children[0]
                    tree._unlink(child)
                    tree._link(child_of_child)
        return top_mult
    
    
    def __eq__(self, other):
        if len(self.trees) != len(other.trees):
            return False
        for tree in self.trees:
            if tree not in other.trees:
                return False
        return True
    
##############################################################################
##############################################################################
################################ FOREST OBJECT ###############################
############################################################################## 
##############################################################################


class Forest:
    
    
##############################################################################
############################### INITIALIZATION ###############################
##############################################################################


    def __init__(self, multitrees, recombinations):
        self.__multitrees = multitrees
        self.__recombinations = recombinations
        
        
##############################################################################
############################ ATTRIBUTE PROPERTIES ############################
############################################################################## 
        
    
    @property
    def multitrees(self):
        return self.__multitrees
    
    @property 
    def recombinations(self):
        return self.__recombinations
    
    
##############################################################################
############################## OTHER PROPERTIES ##############################
############################################################################## 
    
    
    @property 
    def number_trees(self):
        N = 0
        for multitree in self.multitrees:
            N += len(multitree.trees)
        return N
    
    
##############################################################################
############################### STATIC METHODS ###############################
############################################################################## 
    
    @staticmethod
    def iteration(m, N0, rho):
        """
        Input:  - m, positive integer, number of children
                - N0, positive integer, number of parents to choose from for 
                children
                - rho, positive float, between 0 and 1
        Output: a list of 4-tuples, which represents finding the parents and 
                recombination locations of genomes of each child in children 
                list. First and second elements of tuple are indeces of first 
                and second parents chosen out of N0/2 pairs, third element is 
                which parent (0th or 1st) is used first to create child's
                genome, fourth element is a list of floats between 0 and 1 
                which represent all the recombination locations.
        """
        data_list = []
        parent_list = []
        for i in range(m):
            recombination = []
            t = 0
            while t < 1:
                if rnd.random() < rho * np.exp(-rho * t):
                    recombination.append(t)
                t += 0.01
            recombination.append(1.)
            first_parent = rnd.randrange(0, 1)
            ind = rnd.randrange(0, N0//2)
            if 2 * ind not in parent_list:
                parent_list.append(2 * ind)
                parent_list.append(2 * ind + 1)
            parent_one = 2 * ind
            parent_two = 2 * ind + 1
            if rnd.randrange(0,1) == 0:
                tpl = (parent_one, parent_two, recombination)
            else:
                tpl = (parent_two, parent_one, recombination)
            data_list.append(tpl)
        return data_list, parent_list
    
    @staticmethod
    def set_of_recombination_sites(data_list):
        """
        Input:  data_list, a list of 4 tuples, result of iteration 
        Output: a list of floats between 0 and 1 in increasing order, which is
                a union of all the recombination sites in the genomes of this 
                generation 
        """
        total_set = set()
        for datum in data_list:
            total_set.update(datum[2])
        return sorted(list(total_set))
    
    @staticmethod
    def parent_in_interval(interval_start, interval_end, datum):
        """
        Input:  - interval_start, a float between 0 and 1, where interval in 
                genome starts
                - interval_end, a float between 0 and 1, larger than 
                inteval_start, where the interval in genome ends
                - datum, a 4-tuple just like an element of list output by 
                iteration, which holds in itself information of where all 
                parts of this particular genome came from (which parent)
        Output: parent from which the interval signified by interval_start and
                interval_end in the genome came from
        """
        if interval_end <= datum[2][0]:
            return datum[0]
        for i in range(1, len(datum[2])):
            if (interval_start >= datum[2][i - 1] 
                and interval_end <= datum[2][i]):
                return datum[i%2]
        return None
    
    
##############################################################################
################################## METHODS ###################################
##############################################################################

    def delete(self):
        for mult in self.multitrees:
            mult.delete()
        
    def __str__(self):
        string = ''
        for i in range(len(self.multitrees)):
            string += 'Interval: ' + str(self.recombinations[i]) + '\n'
            for tree in self.multitrees[i].trees:
                string += '  Tree: ' + tree.__str__() 
                string += ' Parent: ' + tree.name + '\n'
        return string

    def forest_subdivide(self, new_recomb_list):
        """
        Acts on:    a Forest object
        Input:      new_recomb_list, a list of floats from 0 to 1 in 
                    increasing order, which contains the set of recombinations 
                    of the Forest
        Output:     modifies the Forest to have multitrees for the new list of 
                    recombination sites (copies multitrees if an preexisting 
                    interval is being subdivided) and updates the list of 
                    recombination sites as well
        """
        ind = 0
        new_multitrees = []
        for new_recomb in new_recomb_list:
            new_multitrees.append(self.multitrees[ind].copy())
            if new_recomb == self.recombinations[ind]:
                ind += 1
        self.delete()
        self.__multitrees = new_multitrees
        self.__recombinations = new_recomb_list
    
    def __repr__(self):
        string = 'Forest(['
        for multitree in self.multitrees:
            string += multitree.__repr__() + ','
        string = string[:-1] + '],'
        string += str(self.recombinations)
        string +=')'
        return string
    
    
##############################################################################
############################### CLASS METHODS ################################
##############################################################################


    @classmethod
    def forest_one_iteration(cls, children, N0, rho, t):
        """
        Input:  - children, list of integers 
                - N0, positive integer, number of parents to choose from
                - rho, float between 0 and 1, rate of recombination
                - t, non-negative float, height of leaves
        Output: a Forest of height one (all multitrees in it have tress of 
                height one) grown for the input children where parents were 
                chosen by pairs out of a pool of N0 parents (N0/2 pairs)
                and recombination sites were found using poisson process with 
                rate constant rho, and list of parents' indices (names) that 
                were found for the input children
                (t is not very important. It is the number of iteration which 
                is used to find the height of the trees in the Forest to later
                on add on to the base of the Forest)
        """
        m = len(children)
        data_list, parent_list = cls.iteration(m, N0, rho)
        recombination_sites = cls.set_of_recombination_sites(data_list)
        forest = cls([], recombination_sites)
        # this is loop for multitree
        interval_start = 0.
        for recombination in recombination_sites:
            interval_end = recombination
            new_mult = MultiTree([])
            # this is loop for trees within multitree
            for i in range(m):
                newtree = MetricTree([], None, float(t), str(children[i]))
                parent_name = cls.parent_in_interval(interval_start, 
                                                     interval_end, 
                                                     data_list[i])
                parent_tree = new_mult.name_tree_in_mult(str(parent_name))
                if parent_tree is None:
                    parent_tree = MetricTree([], None, t + 1., 
                                             str(parent_name))
                    new_mult.add_to_trees(parent_tree)
                parent_tree._link(newtree)
            forest.__multitrees.append(new_mult)
            interval_start = interval_end
        return forest, parent_list

    
    @classmethod
    def forest_n_iterations(cls, m, N0, rho):
        """
        Acts on:    Forest class
        Input:      - m, positive integer, number of individuals in first 
                    generation
                    - N0, positive integer, number of parents to choose from
                    - rho, float between 0 and 1, constant in poisson process 
                    for recombination
        Output:     a Forest of Trees on genome intervals defined by 
                    recombination sites grown until common ancestor is found
                    for all individuals in the first generation on that 
                    interval in the genome.
        Type:       classmethod
        """
        t = 0
        base_f, parent_u_1 = cls.forest_one_iteration(list(range(m)), N0, rho, 
                                                      float(t))
        t += 1
        while base_f.number_trees > len(base_f.multitrees):
            top_f, parent_u_2 = cls.forest_one_iteration(parent_u_1, N0, rho, 
                                                         float(t))
            total_set_recombinations = set(base_f.recombinations)
            total_set_recombinations.update(top_f.recombinations)
            recombination_union = sorted(list(total_set_recombinations)) 
            base_f.forest_subdivide(recombination_union)
            top_f.forest_subdivide(recombination_union)
            for k in range(len(recombination_union)):
                base_f.__multitrees[k] += top_f.__multitrees[k]
            ind = 0
            while ind < len(base_f.multitrees) - 1:
                if base_f.multitrees[ind] == base_f.multitrees[ind + 1]:
                    base_f.__recombinations.pop(ind)
                    base_f.__multitrees.pop(ind)
                else:
                    ind +=1
            parent_u_1 = parent_u_2
            t += 1
        return base_f