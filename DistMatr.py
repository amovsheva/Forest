#lets make it  dict of dicts so that 
#          a   b   c
#	 a 0   25  20
#	 b 25  0   30
#        c 20  30  0
# is represented by
# {'a':{'b':25,'c':20}, 'b':{'c':30},'c':{}}
# and so that m['a','b'] gives access to the corresponding entry
# in the matrix

import Tree
import pexp
import inspect
import sample


##############################################################################
############################### CLASS EXCEPTION ##############################
##############################################################################
    
    
class DistMatrStructureError(Exception):
    pass


##############################################################################
############################ DISTANCEMATRIX CLASS ############################
##############################################################################


class DistanceMatrix:
    
    
    """ Square symmtric matrix with zeroes on the diagonal
    indexed by strings.
    Methods:
    [key1,key2] -- read/write access to individual entries.
    keys        -- ordered list of keys
    copy()      -- an identical copy of itself

    ClassMethods:
    FromTree(T) -- construct matrix of distances between leaves of T
    FromPexp(P) -- construct matrix of distances from pexp
    """
            
            
##############################################################################
################################# INITIALIZE #################################
##############################################################################


    # dictionary is in the form {key_1: __, key_2: __, etc.}
    # where __ is some value
    # if want __ to be multiple entries put dictionary for __
    # __ = {key'_1: __, key_2: __, etc.}
    
    def __init__(self, dictionary = dict()):
        if type(dictionary) is not dict:
            raise TypeError("DistanceMatrix data has to be a dictionary.")
        keys = dictionary.keys()
        for key in keys:
            if type(dictionary[key]) is not dict:
                raise DistMatrStructureError('''DistanceMatrix data has to 
                be a dictionary of dictionaries''')
            subkeys = dictionary[key].keys()
        self.__data = dictionary

        
##############################################################################
########################### ATTRIBUTES PROPERTIES ############################
##############################################################################


    @property
    def data(self):
        """
        Acts on:    a DistanceMatrix
        Input:      none
        Output:     accesses data inside DistanceMatrix
        Type:       getter property
        """
        return self.__data
    
        
##############################################################################
################################# PROPERTIES #################################
##############################################################################


    @property
    def size(self):
        """
        Acts on:    a DistanceMatrix
        Input:      none
        Output:     size of the distance matrix that corresponds to the 
                    DistanceMatrix object
        Type:       property
        """
        return len(self.data)**2
    
    @property
    def keys(self):
        """
        Acts on:    a DistanceMatrix
        Input:      none
        Output:     a list of strings of all the keys in the data of 
                    DistanceMatrix in alphabetical order
        Type:       property
        """
        return sorted(list(self.data.keys()))
    
    
##############################################################################
################################## METHODS ###################################
##############################################################################


    def _check_keys(self, keys, check_existing = False):
        """
        Acts on:    a DistanceMatrix
        Input:      - keys, a string 2-tuple
                    - check_existing, a boolean
        Output:     checks if keys is a string 2-tuple (if not gives and error
                    message), and if check_existing is True, also checks if 
                    the input keys exist within the DistanceMatrix dictionary 
                    as keys
        Used in:    __getitem__, __setitem__
        """
        if len(keys) != 2 or type(keys[0]) != str or type(keys[1]) != str:
            raise TypeError("Expected a 2-tuple of strings.")
        if check_existing:
            K = self.keys
            if keys[0] not in K or keys[1] not in K:  
                raise ValueError("At least one of the keys is not valid.")
        
    def __getitem__(self, keys):
        """
        Acts on:    a DistanceMatrix
        Input:      keys, 2-tuple of strings (key_2, key_2)
        Output:     accesses the value in the dictionary of DistanceMatrix 
                    under key_1, key_2
        Type:       "getter" function
        Short form: self[keys_1, key_2]
        """
        self._check_keys(keys, True)
        if keys[0] == keys[1]:
            return 0.
        else:
            (first, second) = sorted(keys)
            return self.data[first][second]

    def _add_new_key(self, new_key):
        """
        Acts on:    a DistanceMatrix
        Input:      new_key, a string
        Output:     if new_key was not already a key in the DistanceMatrix 
                    dictionary add the key to the dictionary and all the
                    subdictionaries for keys that come before it 
                    (alphabetically)
        Used in:    __setitem__
        """
        old_keys = self.keys
        if new_key in old_keys:
            return    
        else: 
            self.data[new_key] = dict()
            for key in old_keys:
                if key < new_key:
                    self.data[key][new_key] = None
                else:
                    self.data[new_key][key] = None
            return

    def __setitem__(self, keys, value):
        """
        Acts on:    a DistanceMatrix
        Input:      - keys, a 2-tuple of strings
                    - value, a nonnegative float
        Output:     first, if necessary adds the specified keys to the 
                    DistanceMatrix dictionary, and then sets the input keys in  
                    the dictionary of DistanceMatrix to the value
        Type:       "setter"
        Short form: self[key_1, key_2] = value
        """
        self._check_keys(keys, False)
        if type(value) is not float:
            raise TypeError('''Value has to be a float.''')
        if keys[0] == keys[1]: 
            if value != 0.:
                raise DistMatrStructureError('''Cannot assign non-zero value 
                to a diagonal element''')
            else:
                self._add_new_key(keys[0])
                return
        else:
            self._add_new_key(keys[0])
            self._add_new_key(keys[1])
            (first, second) = sorted(keys)
            self.data[first][second] = value
            return

    def __str__(self):
        """
        Acts on:    a DistanceMatrix
        Input:      none
        Output:     prints DistanceMatrix in the form of a matrix
        Short form: print(self)
        """
        S = ' '*5
        K = self.keys
        for key in K:
            S += key + ' '*4
        S += '\n'
        for key1 in K:
            S += key1 + ' '*4
            for key2 in K:
                if self[key1, key2] is None:
                    S += str('-') + ' '*4
                else:
                    S += str(self[key1, key2]) + ' '*4
            S += '\n'
        return S
    
    def __repr__(self):
        """
        Acts on:    a DistanceMatrix
        Input:      none
        Output:     prints a string expression that if plugged back into 
                    python would create an equivalent DistanceMatrix to the 
                    DistanceMatrix that is being acted on
        Short form  self (enter)
        """
        return 'DistanceMatrix(' + self.data.__repr__() + ')'
            
    def __eq__(self, other):
        """
        Acts on:    a DistanceMatrix
        Input:      other, a DistanceMatrix
        Output:     a boolean that indicates equivalency of the input 
                    DistanceMatrix and the DistanceMatrix, which is being 
                    acted on.
        Short form: self == other
        """
        if type(self) is not type(other):
            raise TypeError("Input has to be a DistanceMatrix.")
        return self.data == other.data
    
    def copy(self):
        """
        Acts on:    a DistanceMatrix
        Input:      none
        Output:     a DistanceMatrix which is an identical copy of the 
                    DistanceMatrix that is being acted on.
        """
        return eval(self.__repr__())

    def submatrix(self, list_names):
        for name in list_names:
            if type(name) is not str:
                raise TypeError("Input has to be a list of strings.")
        newDistanceMatrix = DistanceMatrix(dict())
        for key1 in list_names:
            for key2 in list_names:
                newDistanceMatrix[key1, key2] = self[key1, key2]
        return newDistanceMatrix
    
    def append(self, label, dictionary):
        if type(label) is not str:
            raise TypeError("First input has to be a string.")
        if type(dictionary) is not dict:
            raise TypeError("Second input has to be a dictionary.")
        for key in dictionary:
            self[label, key] = dictionary[key]
        return self
                
        
##############################################################################
################################ CLASSMETHODS ################################
##############################################################################


    @classmethod
    def FromTree(cls, tree):
        """
        Acts on:   DistanceMatrix class
        Input:     tree, a Tree object (a MetricTree or a CombinatorialTree)
        Output:    a DistanceMatrix equivalent of the input Tree
        Type:      classmethod
        """
        if (type(tree) is not Tree.CombinatorialTree 
            and type(tree) is not Tree.MetricTree):
            raise TypeError("Input has to be a Combinatorial or Metric Tree.")
        newDistanceMatrix = cls(dict())
        leaves = tree.leaves
        for leaf1 in leaves:
            name1 = leaf1.name
            for leaf2 in leaves:
                name2 = leaf2.name
                value = leaf1.common_ancestor([leaf2]).height * 2.
                newDistanceMatrix[name1, name2] = value
        return newDistanceMatrix
    
    @classmethod
    def FromPexp(cls, pexp_input):
        """
        Acts on:   DistanceMatrix class
        Input:     pexp, a Pexp object
        Output:    a DistanceMatrix equivalent of the input Pexp
        Type:      classmethod
        """
        if type(pexp_input) is not pexp.Pexp:
            raise TypeError("Input has to be a Pexp.")
        tree = Tree.MetricTree.FromPexp(pexp_input)
        x = cls.FromTree(tree)
        tree.delete()
        return x
    
    @classmethod
    def FromSample(cls, sample_input):
        """
        Acts on:   DistanceMatrix class
        Input:     sample_input, a Sample object
        Output:    a DistanceMatrix equivalent of the input Sample
        Type:      classmethod
        """
        if type(sample_input) is not sample.Sample:
            raise TypeError("Input has to be a Sample.")
        M = cls(dict())
        keys = sample_input.keys
        N = len(keys)
        for i in range(N):
            for j in range(i, N):
                M[keys[i], keys[j]] = sample.HummingDistance(sample_input[keys[i]], 
                                                             sample_input[keys[j]])
        return M
