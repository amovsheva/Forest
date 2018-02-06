import DistMatr
import pexp

import random as rnd
import numpy as np
import sys
import matplotlib.pyplot as plt
import inspect


##############################################################################
################################# EXCEPTION ##################################
##############################################################################
    
    
class TreeStructureError(Exception):
    pass


##############################################################################
################################# TREE CLASS #################################
##############################################################################


class CombinatorialTree(object):
    

##############################################################################
################################# CONSTANTS ##################################
############################################################################## 


    # pexp_class = pexp.Pexp
            
    # distmatr_class = DistMatr.DistanceMatrix
    
    
##############################################################################
################################# INITIALIZE #################################
############################################################################## 


    def __init__(self, children, parent, name = None):
        if parent != None:
            parent._link(self)

        self.__children=[]
        for child in children:
            if type(child) is not type(self):
                raise TreeStructureError('''Every child type has to be same 
                as self type.''')
            self._link(child)

        self.__name=None
        if children != [] and name is not None:
            raise TreeStructureError('''Node with children cannot have a 
            name.''')
        else:
            self.__name = name
            
        
##############################################################################
########################### ATTRIBUTE PROPERTIES #############################
##############################################################################
 
    
    @property
    def children(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     a list of CombinatorialTrees, which are the children of 
                    the CombinatorialTree, which is being acts on
        Type:       property, getter
        """
        return self.__children

    @property
    def parent(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     CombinatorialTree that is the parent of the 
                    CombinatorialTree
        Type:       property, getter
        """
        return self.__parent
    
    @property
    def name(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     string, which is the name of the CombinatorialTree
        Type:       property, getter
        """
        return self.__name
    
    
##############################################################################
################################ PROPERTIES ##################################
############################################################################## 


    @property
    def height(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     depth of a combinatorial tree (unbalanced non metric tree)
        Type:       property
        """
        if self.children == []:
            return 0.
        else:
            d = 0.
            for child in self.children:
                d = max(d, child.height)
            return d + 1.
        
    @property
    def is_leaf(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     a boolean that indicates whether the tree that is being  
                    acted on is a leaf or not
        Type:       property
        """
        return self.children == []
    
    @property
    def my_root(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     go up the parent chain and return the root of the tree 
                    that self is a part of.
        Type:       property
        """
        root = self
        while root.parent is not None:
            root = root.parent
        return root
    
    @property
    def leaves_names(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     a sorted list of names of leaves of the tree that is being 
                    acted on
        Type:       property
        """
        if self.children == []:
            return [self.name]
        else:
            L = []
            for child in self.children:
                L = L + child.leaves_names
            return sorted(L)
        
    @property
    def leaves(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     a list of trees of leaves the tree, which is being acted 
                    on, has, sorted alphabetically
        Type:       property
        """
        if self.children == []:
            return [self]
        else:
            L = []
            for child in self.children:
                L = L + child.leaves
            return sorted(L, key = lambda x: x.name)
        
    @property
    def Nleaves(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     number of leaves the tree has
        Used in:    __plot
        Type:       property
        """
        if self.children == []:
            return 1
        else:
            L = 0
            for child in self.children:
                L = L + child.Nleaves
            return L 
    
    @property
    def _smallest_leaf_name(self):
        return self.leaves_names[0]
    
    @property
    def first_leaf(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     name of first leaf (alphabetically) of the tree
        Type:       property
        """
        return sorted(self.leaves_names)[0]
    
    
##############################################################################
################################## METHODS ###################################
############################################################################## 


    def _link(self, other): 
        """
        Acts on:    a CombinatorialTree
        Output:     other, a CombinatorialTree
        Input:      makes self parent of other and adds other to list of 
                    children of self
        """
        self._check_height_and_type(other)
        self.__children.append(other)
        other.__parent = self
        
    def _unlink(self, other):
        """
        Acts on:    a CombinatorialTree
        Input:      other, a CombinatorialTree
        Output:     removes other from children of self and makes the parent 
                    of other None.
        """
        self.__children.remove(other)
        other.__parent = None
    
    def cut(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     splits the tree above self returning 2-tuple of the
                    resulting trees that are defined by their root
        """
        if self.parent is None:
            return (self, None)
        else:
            parent = self.parent
            parent._unlink(self)
            return (self, parent.my_root)

    def insert(self, other):
        """
        Acts on:    a CombinatorialTree
        Input:      other, a CombinatorialTree
        Output:     inserts other above self modifying all the appropriate 
                    children and parents and returns tree that represents
                    new tree
        """
        if self.parent is None:
            other._link(self)
        else:
            self.parent._link(other)
            self.parent._unlink(self)
            other._link(self)
        return self.my_root
    
    def copy(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     create a copy of the tree and all its children    
        """
        cls=type(self)
        newtree = cls([], self.parent, self.height, self.name)
        for child in self.children:
            newtree._link(child.copy())
        return newtree
    
    def common_ancestor(self, name_or_tree_list):
        """
        Acts on:    a CombinatorialTree
        Input:      a list of names (strings) or CombinatorialTrees of leaves 
                    of a tree
        Output:     a CombinatorialTree of the common ancestor of the leaves 
                    in the list and the tree that is being acted on
        """
        type_0 = type(name_or_tree_list[0])
        if type_0 is not str and type_0 is not type(self):
            raise TypeError('Input list has to be a string or Tree list.')
        ancestor = self
        if type_0 is str:
            leaves_list = ancestor.leaves_names
            for name_or_tree in name_or_tree_list:
                if type(name_or_tree) is not str:
                    raise TypeError('Input list has to be all strings.')
        if type_0 is type(self):
            leaves_list = ancestor.leaves
            for name_or_tree in name_or_tree_list:
                if type(name_or_tree) is not type(self):
                    raise TypeError('Input list has to be all Trees.')
        for name_or_tree in name_or_tree_list:
            if name_or_tree not in leaves_list:
                if ancestor.parent is None:
                    return None
                else:
                    ancestor = ancestor.parent 
                    return ancestor.common_ancestor(name_or_tree_list)
        return ancestor

    def delete(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Ouput:      deletes self and all its children by unlinking all of the 
                    parents and children in the tree
                    (would require an additional [del pointer] outside the 
                    method to completely destroy the object.)
        """
        if self.parent is not None:
            self.parent._unlink(self)
        for child in self.children:
            child.delete()
            
    def promote(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Ouput:      a MetricTree which is 
        
        turn combinatorial tree into metric tree. Change class
        and write depth into the height slots
        """
        children = []
        for child in self.children:
            children.append(child.promote())
        return MetricTree(children, self.parent, float(self.height), 
                          self.name)
            
    def __str__(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     prints the CombinatorialTree in pexp form
        Short form: print(self)
        """
        return str(pexp.Pexp.FromTree(self))
    
    def __repr__(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     prints the CombinatorialTree in the form that you get plug
                    back into python and create equivalent CombinatorialTree
        Short form: self (enter)
        """
        if self.__class__ == MetricTree :
            return ('MetricTree.FromPexp(' 
                    + pexp.Pexp.FromTree(self).__repr__() + ')')
        else:
            return ('CombinatorialTree.FromPexp(' 
                    + pexp.Pexp.FromTree(self).__repr__() + ')')
    
    def __eq__(self, other):
        """
        Acts on:    a CombinatorialTree
        Input:      other, a CombinatorialTree
        Output:     a boolean indicating the equivalance of self and other
        """
        if type(self) != type(other):
            raise TypeError(" Can only compare trees of the same type")
        
        if self.name != other.name:
            return False
        if self.height != other.height:
            return False
        if self.is_leaf and other.is_leaf:
            return self.name == other.name
        if len(self.children) != len(other.children):
            return False
        if set(self.leaves_names) != set(other.leaves_names):
            return False
        children1 = sorted(self.children, 
                           key = lambda x: x._smallest_leaf_name)
        children2 = sorted(other.children, 
                           key = lambda x: x._smallest_leaf_name)
        N = len(children1)
        for i in range(N):
            if children1[i] != children2[i]:
                return False
        return True
    
    
##############################################################################
########################### FOR GRAPHING THE TREE ############################
############################################################################## 
        

    def __plot(self,leaves_left):
        """
        Acts on:    a CombinatorialTree
        Input:      leaves_left, positive integer that is the number of leaves 
                    that are situated to the left of the specified tree
        Output:     Draws a graph of the tree of the tree, its children, and  
                    its children's children, etc. (does not print yet)
        Used in:    plot
        """
        # plot a dot for self
        # self.__children = sorted(self.__children, key = lambda x: x.first_leaf)
        my_x = leaves_left + (self.Nleaves - 1.)/2
        my_y = self.height
        plt.scatter([my_x], [my_y])
        if self.is_leaf:
            plt.annotate(str(self.name), xy = (my_x, my_y), 
                         xytext = (my_x + 0.1, my_y),)
        # plot children subtrees
        leaves_covered = leaves_left
        for child in self.children :
            ((x, y), leaves_covered) = child.__plot(leaves_covered)
            plt.plot([my_x, x], [my_y, my_y], '-k')
            plt.plot([x, x], [my_y, y],  '-k')
        return ((my_x, my_y), leaves_left + self.Nleaves)        


    def plot(self):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     prints the corresponding tree graph for the tree
        """
        plt.figure()
        self.__plot(0)
        plt.show()
        
        
##############################################################################
################################ STATICMETHODS ###############################
##############################################################################
 
    def _check_height_and_type(self,other):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     None. Check whether types are ok.
        """
        if type(other) is not type(self):
            raise TreeStructureError('''Input has to be a tree.''')
    

    
    
##############################################################################
################################ CLASSMETHODS ################################
##############################################################################


    @classmethod
    def FromPexp(cls, pexp_input):
        """
        Acts on:    CombinatorialTree class
        Input:      a Pexp object
        Output:     CombinatorialTree equivalent of the input Pexp object
        Type:       classmethod
        """
        if type(pexp_input) is not pexp.Pexp:
            raise TypeError("Input has to be a Pexp.")
        if pexp_input.is_leaf:
            name = pexp_input.string
            return cls([], None, 0., name)
        else:
            children_trees = []
            children = pexp_input.children
            for child in children:
                children_trees.append(cls.FromPexp(child))
            if cls == MetricTree:
                height = float(pexp_input.height)
             else:
                height = 0
            return cls(children_trees, None,height)


##############################################################################
##############################################################################
############################## INHERITANCE CLASS #############################
##############################################################################
##############################################################################

    
class MetricTree(CombinatorialTree):

    
##############################################################################
################################## CONSTANTS #################################
##############################################################################


    first_letter = ord('a')
    
    
##############################################################################
################################# INITIALIZE #################################
############################################################################## 


    def __init__(self, children, parent, height, name = None):
        if children == [] and height != 0:
            raise TreeStructureError("Leaf must have height==0")
        self.__height = height

        if parent != None:
            parent._link(self)

        self.__children=[]
        for child in children:
            if type(child) is not type(self):
                raise TreeStructureError('''Every child type has to be same 
                as self type.''')
            self._link(child)

        self.__name=None
        if children != [] and name is not None:
            raise TreeStructureError('''Tree with children cannot have a 
            name.''')
        else:
            self.__name = name
        
##############################################################################
########################### ATTRIBUTE PROPERTIES #############################
##############################################################################


    @property
    def height(self):
        """
        Acts on:    a MetricTree
        Input:      none
        Output:     accesses the height attribute of the MetricTree
        Type:       property
        """
        return self.__height

    
##############################################################################
################################# PROPERTIES #################################
##############################################################################

    
##############################################################################
################################## METHODS ###################################
##############################################################################


    def promote(self):
        """
        Acts on:    a MetricTree
        Input:      none
        Output:     self
        """
        return self

    def demote(self):
        """
        Acts on:    a MetricTree
        Input:      none
        Output:     a CombinatorialTree equivalent where all the heights 
                    are removed
        """
        children = []
        for child in self.children:
            children.append(child.demote())
        return CombinatorialTree(children, self.parent, 0, self.name)
            

##############################################################################
################################ STATICMETHOD ################################
##############################################################################


    def _check_height_and_type(self,other):
        """
        Acts on:    a CombinatorialTree
        Input:      none
        Output:     None. Check whether types are ok.
        """
        if type(other) is not type(self):
            raise TreeStructureError('''Input has to be a tree.''')
        if self.height < other.height:
            raise TreeStructureError('''Height of a child node must be not greater then the height of parent''')
        
##############################################################################
################################ CLASSMETHODS ################################
##############################################################################
              
              
    @classmethod
    def Evolve(cls, N0, N):
        """
        Acts on:    the tree class
        Input:      - N0, natural number of leaf trees 
                    - N, natural number of individuals in each generation  
                    parents are chosen from (N >= N0)
        Output:     a tree, that contains in itself a tree with N0 leaves
        Type:       classmethod
        """
        if type(N0) is not int: 
            raise TypeError('First input has to be integer.')
        if N0 <= 0:
            raise ValueError('First input has to be a positive integer.')
        if type(N) is not int:
            raise TypeError('Second input has to be integer.')
        if N < N0:
            raise ValueError('''Second input has to be greater than or equal 
            to the first input.''')
        trees = []
        for i in range(N0):
            newtree = cls([], None, 0., chr(MetricTree.first_letter + i))
            trees.append(newtree)
        t = 0.
        while len(trees) > 1:     
            t += 1.
            klist = []
            hist = []
            for tree in trees:
                k = rnd.randint(0, N-1)
                if k in klist:
                    index = klist.index(k)
                    hist[index].append(tree)
                else:
                    klist.append(k)
                    hist.append([tree])    
            index = 0
            for nlist in hist:
                freq = len(nlist)
                if freq > 1:
                    newtree = cls(nlist, None, t)
                    trees.append(newtree)
                    for tree in newtree.children:
                        trees.remove(tree)
        [root] = trees
        return root
    
    @classmethod
    def FromDistMatr(cls, distmatr):
        if type(distmatr) is not DistMatr.DistanceMatrix:
            raise TypeError("Input has to be a DistMatr.")
        leaves = distmatr.keys
        if len(leaves) == 0:
            return None
        if len(leaves) == 1:
            T = cls([], None, 0., leaves[0])
            return T
        usedleaves = leaves[:2]
        leaf1 = cls([], None, 0., usedleaves[0])
        leaf2 = cls([], None, 0., usedleaves[1])
        T = cls([leaf1, leaf2], None, 
                distmatr[usedleaves[0],usedleaves[1]]/2)
        for leaf in leaves[2:]:
            hist = []
            for usedleaf in usedleaves:
                dist = distmatr[usedleaf, leaf] * 1. / 2
                state = False
                for h in hist:
                    if dist == h[0]:
                        h[1].append(usedleaf)
                        state = True
                if state == False:
                    hist.append((dist, [usedleaf]))
            hist_sorted = sorted(hist, key = lambda x: x[0])
            L = hist_sorted[0][1]
            R = []
            for h in hist_sorted[1:]:
                R += h[1]
            R = sorted(R)
            for aleaf in T.leaves:
                if L[0] == aleaf.name:
                    baseleaf = aleaf
            ca_L = baseleaf.common_ancestor(L)
            if ca_L.leaves_names != L:
                raise ValueError("Error.")
            for l in L:
                for r in R:
                    if distmatr[l, r] != distmatr[leaf, r]:
                        raise ValueError("Error.")
            newleaf = cls([], None, 0., leaf)
            newtree = cls([newleaf], None, distmatr[L[0], leaf] * 1./ 2)
            ca_L.insert(newtree)
            T = T.my_root
            usedleaves.append(leaf)
        return T
