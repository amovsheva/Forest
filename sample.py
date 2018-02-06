import random
import numpy as np
import Tree
import time


##############################################################################
############################### GENOTYPE CLASS ###############################
##############################################################################


class Genotype:
    
    
    """Represents sequence of 0/1 bits.
    Properties:
    length          -- length of the sequence
    
    Methods:
    obj[i]
    obj[i]=         -- read/write access to the individual bits
                       we will also probably need slices! 
                       Let's postpone it
    switch(i)       -- change the i^th bit to the opposite
    ==              -- test equality
    mutate(time,mu) -- mutate the sequence for given time with given rate 
    copy()          -- identical copy of self

    ClassMethods:
    From01String
    FromByteArray
    ...
    
    
    Functions:
    distance(g1,g2) -- Hamming distance between two genotypes
    """
    
##############################################################################
################################# CONSTANTS ##################################
##############################################################################


    # to save on calculations: __p2[i]=2**i
    __p2 = (1,   # 10000000
            2,   # 01000000
            4,   # 00100000
            8,   # 00010000
            16,  # 00001000
            32,  # 00000100
            64,  # 00000010
            128, # 00000001
            256) # 00000000 1
    __p2_1 = (254,  # 01111111
               253,  # 10111111
               251,  # 11011111
               247,  # 11101111
               239,  # 11110111
               223,  # 11111011
               191,  # 11111101
               127,  # 11111110
               255)  # 11111111 0
    __p2_2 = (0,   # 00000000
               1,   # 10000000
               3,   # 11000000
               7,   # 11100000
               15,  # 11110000
               31,  # 11111000
               63,  # 11111100
               127, # 11111110
               255) # 11111111
    
    
##############################################################################
############################### INITIALIZATION ###############################
##############################################################################


    # Anna, storing a single integer or a boolean takes 8 bytes = 64 bits
    # plus some extra space for the list
    # Since we will be dealing with long sequences ~10^9 eventually
    # it make sense to represent genotypes as bytearrays. 
    # They take exactly necessary space + 57 bytes extra per array.
    # something like this
    def __init__(self, l, data = None):
        """
        Input:  - l, length of the genotype in bits
                - data, bytearray representing the genotype (biological obj)
                (sequence of bytes, eight bits each)
        Output: object Genotype with attributes length and data, which is the
                input data but converted from bit form to byte form
        
        """
        if type(l) is not int:
            raise TypeError('First input has to be an integer.')
        if data is not None and type(data) is not bytearray:
            raise TypeError('Second input has to be bytearray if included.')
            
        self.__length = l
        (lb, tail) = self.__bytes_and_tail
        if data == None:
            self.__data = bytearray(lb)
        elif len(data) < lb :
            raise ValueError("The data is too short")
        else :
            self.__data = data[:lb]
            self.__truncate()
            
            
##############################################################################
################################# PROPERTIES #################################
##############################################################################


    @property
    def length(self):
        """
        Acts on:    a Genotype object
        Input:      none
        Output:     integer that says how long the data in the Genotype is in 
                    bits.
        Type:       property
        """
        return self.__length

    # how long is bytearray and how much the last byte is filled
    @property
    def __bytes_and_tail(self):
        """
        Acts on:    a Genotype object
        Input:      none
        Output:     a 2-tuple where first element is number of bytes needed
                    to contain the data of the genotype, and how many 
                    significant bits the last byte contains
                    (which are not always to be zero).
                    This is all given that the data is of 'length' bits long.
        Type:       property
        
        If length = 8*n -> # bytes = n, (8*n-1)//8 + 1 = n-1+1 = n
        If length = 8*n - 1 -> # bytes = n, (8*n-2)//8 + 1 = n-1+1 = n
        If length = 8*n + 1 -> # bytes = n + 1, (8*n)//8 + 1 = n+1 = n + 1
        First element works out
        
        If length = 8*n -> # tail = 8, (8*n-1)%8 + 1 = 7+1 = n
        If length = 8*n - 1 -> # tail = 7, (8*n-2)%8 + 1 = 6+1 = 7
        If length = 8*n + 1 -> # tail = 1, (8*n)%8 + 1 = n+1 = n + 1
        Second element works out
        """
        return ((self.__length - 1) // 8 + 1, (self.__length - 1) % 8 + 1)
    
    
##############################################################################
############################### STATIC METHOD ################################
##############################################################################


    # given index find the byte and the shift within the byte  
    # corresponding to the idexed bit
    @staticmethod
    def __byte_and_shift(i):
        """
        Acts on:    Genotype class or object
        Input:      i, a non negative integer
        Output:     a 2-tuple of nonnegative integers which encodes the 
                    location of the ith bit within the data attribute (which 
                    is a bytearray), where the first element is the number of  
                    the byte within the array is located and where the second 
                    element is the location of the bit in the aforementioned
                    byte
        Type:       staticmethod
        """
        return (i // 8, i % 8)
    
    
##############################################################################
################################### METHODS ##################################
##############################################################################


    def __truncate(self):
        """
        Acts on:    a Genotype object
        Input:      none
        Output:     modifies the data attribute in the object to be minimal 
                    amount of bytes to contain all the needed bits and sets
                    all the insignificant bits in the last byte to zero
        Type:       staticmethod
        """
        (lb, tail) = self.__bytes_and_tail
        # remove extra bytes. 
        del self.__data[lb:]
        # clean up unused portion of the last byte
        self.__data[lb - 1] &= (self.__p2[tail] - 1)

    def __str__(self):
        """
        Acts on:    Genotype object
        Input:      none
        Output:     a string of zeros and ones that is equivalent to the 
                    bytearray stored in the Genotype
        Short for:  print(self)
        """
        string = ''
        for i in range(self.length):
            string += str(int(self[i]))
        return string

    # temporary
    def __repr__(self):
        """
        Acts on:    Genotype object
        Input:      none
        Output:     a string that will produce equivalent Genotype to self if 
                    plugged back into python
        Short for:  self (enter)
        """
        return "Genotype.From01String('" + str(self) + "')"
          
    def __getitem__(self, i):
        """
        Acts on:    Genotype object
        Input:      i, nonnegative integer, index for bytearray
        Output:     boolean that is the ith element of the bytearray stored 
                    in the Genotype object
        Short form: self[i]
        """
        # check that i is valid
        # byte index, shift within byte
        (nb, sb) = self.__byte_and_shift(i)
        return bool(self.__data[nb] & self.__p2[sb])

    def __setitem__(self, i, value):
        """
        Acts on:    Genotype object
        Input:      - i, nonnegative integer, index for bytearray
                    - value, a string, integer, or boolean
        Output:     Genotype object, same as one being acted on, except with
                    ith element of its bytearray changed to boolean value
                    of input value.
        Short form: self[i] = value
        """
        value = bool(value)
        (nb, sb) = self.__byte_and_shift(i)
        if value:
            self.__data[nb] |= self.__p2[sb]
        else:
            self.__data[nb] &= self.__p2_1[sb]
        return self

    def switch(self, i):
        """
        Acts on:    Genotype object
        Input:      i, nonnegative integer, index for bytearray
        Output:     modifies the Genotype, same as one being acted on, except 
                    with ith element of its bytearray switched (from being 
                    True to being False or from being False to being True)
        """
        # ... optimize
        self[i] = not self[i]

    def mutate(self, T, mu, interval = None):
        """
        Acts on:    Genotype object
        Input:      - time, a positive float
                    - mu, a positive float less than one, rate of mutation
                    - interval, a list of two integers, which is range of loci
                    that will be mutated inside the Genotype
        Output:     a Genotype object which is has taken the bytearray 
                    within the Genotype being acted on and has been mutated
                    by Poisson process with mutation rate mu and the given
                    time
        """
        newgenotype = self.copy()
        if interval is None:
            range_genome = range(newgenotype.length)
        else:
            range_genome = range(interval[0], interval[1])
        for i in range_genome:
            if random.random() < 1 - np.exp(-T * mu):
                newgenotype.switch(i)
        return newgenotype

    def __eq__(self, other):
        """
        Acts on:    Genotype object
        Input:      other, a Genotype
        Output:     a boolean which indicates whether the two Genotypes are
                    equivalent
        Short form: self == other
        """
        if type(other) is not type(self):
            raise TypeError('''Second value in the equality has to be same
                            type as self.''')
        if self.length != other.length:
            return False
        self.__truncate()
        other.__truncate()
        return self.__data == other.__data
       
    def copy(self):
        """
        Acts on:    Genotype object
        Input:      none
        Output:     a Genotype object which is equivalent (but not same) as the 
                    Genotype being acted on
        """
        cls = type(self)
        return cls(self.__length, self.__data)
    
    def __iadd__(self, other):
        """
        Acts on:    Genotype object
        Input:      other, Genotype object
        Output:     modifies self by adding bytearray of other to self 
                    bytearray element by element 
        Short form: +=
        """
        for i in range(len(self.__data)):
            self.__data[i] |= other.__data[i]
        return self
    
    
##############################################################################
################################ CLASS METHODS ###############################
##############################################################################


    @classmethod
    def From01String(cls, string):
        """
        Acts on:    the Genotype class
        Input:      string, a string of 0's and 1's
        Output:     a Genotype that has contains a bytearray equivalent to the 
                    string of zeros and ones which was the input
        Type:       classmethod
        """
        # could be optimized, I think
        if type(string) is not str:
            raise TypeError("Input has to be a string.")
        try:
            g = cls(len(string))
            i = 0
            for c in string:
                g[i] = int(c)
                i += 1
            return g
        except (ValueError, SyntaxError):
            raise ValueError("Input has to be a string of 0's and 1's.")


##############################################################################
################################# CONSTANTS ##################################
##############################################################################


# For experimentation
g1=Genotype.From01String('10110011101')
g2=Genotype.From01String('0101001011100100101010100101011101001010100011110')


##############################################################################
############################### OUTSIDE METHOD ###############################
##############################################################################

def HummingDistance(g1,g2):
    """
    Acts on:    none
    Input:      g1 and g2, Genotype objects with bytearrays of same length
    Output:     an integer which is the number of differences between their
                bytearrays
    """
    # count at how many places g1 and g2 differ
    # how to do it effectively?
    if g1.length != g2.length:
        raise ValueError('Length two genotypes has to be the same.')
    count = 0.
    for i in range(g1.length):
        if g1[i] != g2[i]:
            count += 1.
    return count


##############################################################################
################################ SAMPLE CLASS ################################
##############################################################################


class Sample:
    
    
    # implement as a dictionary of genotypes.
    """Named sequence of Genotypes of the same length
    Properties:
    length   -- length of the sequences
    keys     -- list/set of names
    size     -- size of the sample = number of genotypes

    Methods:
    [name]
    [name]=  -- read/write access to the individual genotypes
    +        -- union of samples
    copy()   -- identical copy

    ClassMethods:
    FromTree(T, mu, init=Genotype(l)) 
             -- generate sample from a metric tree T by mutating
                init sequence with the rate mu
    """
    
##############################################################################
############################### INITIALIZATION ###############################
##############################################################################


    def __init__(self, dictionary):
        self.__dictionary = dictionary
        
        if type(dictionary) is not dict:
            raise TypeError('Input has to be a dictionary.')
        
        for key in dictionary:
            if type(dictionary[key]) is not Genotype:
                raise TypeError('''Each value in the dictionary has to be a 
                                Genotype.''')
            if key == list(dictionary.keys())[0]:
                val = dictionary[list(dictionary.keys())[0]].length
            if dictionary[key].length != val:
                raise ValueError('''All of the Genotypes stored in the 
                dictionary have to have the same length.''')
                
                
##############################################################################
############################ ATTRIBUTE PROPERTIES ############################
##############################################################################

        
    @property
    def dictionary(self):
        """
        Acts on:    Sample object
        Input:      none
        Output:     dictionary which is the object's attribute
        Type:       property
        """
        return self.__dictionary
    
    
##############################################################################
################################# PROPERTIES #################################
##############################################################################

            
    @property
    def keys(self):
        """
        Acts on:    Sample object
        Input:      none
        Output:     list of names in alphabetical order, which are the keys of
                    the dictionary stored within the Sample object
        Type:       property
        """
        return sorted(list(self.dictionary.keys()))
            
    @property
    def length(self):
        """
        Acts on:    Sample object
        Input:      none
        Output:     the length of the bytearrays within Genotypes stored inside 
                    the dictionary of the Sample obj (since all of them have
                    to be the same length)
        Type:       property
        """
        return self[self.keys[0]].length
    
    @property 
    def size(self):
        """
        Acts on:    Sample object
        Input:      none
        Output:     number of Genotypes stored in dictionary of the Sample
        Type:       property
        """
        return len(self.keys)
    

##############################################################################
################################## METHODS ###################################
##############################################################################


    def __iadd__(self, other):
        """
        Acts on:    a Sample object
        Input:      other, Sample
        Output:     Sample that is being acted on, with its dictionary 
                    modified to contain dictionary of other Sample
        Short form: self += other
        """
        if type(other) is not type(self):
            raise TypeError("Value added has to be a Sample.")
        self.__dictionary.update(other.__dictionary)
        return self

    def __getitem__(self, key):
        """
        Acts on:    a Sample object
        Input:      key, string
        Output:     Genotype stored in dictionary in Sample under the input 
                    key
        Short form: self[key]
        """
        return self.dictionary[key]
    
    def __setitem__(self, key, value):
        """
        Acts on:    a Sample object
        Input:      - key, string (key of dictionary inside Sample)
                    - value, Genotype
        Output:     modifies Sample to have dictionary have the key refer to
                    the input value
        Short form: self[key] == value
        """
        self.dictionary[key] = value
        return self

    def __repr__(self):
        """
        Acts on:    a Sample object
        Input:      none
        Output:     a string representation of the Sample object which would 
                    produce an equivalent object if plugged back into python
        Short form: self (enter)
        """
        string = 'Sample({'
        for name in self.keys:
            string += "'" + name + "'" + ': ' + self[name].__repr__() + ','
        # get rid of the last comma
        string = string[:-1] + '})'
        return string
    
    def __str__(self):
        """
        Acts on:    a Sample object
        Input:      none
        Output:     a string representation of the Sample object keys and 
                    the genotypes in terms of 0s and 1s
        Short form: print(self)
        """
        string = '('
        for key in self.keys:
            string += key + ':' + self[key].__str__() + ', '
        string = string[:-2] + ')'
        return string
    
    
##############################################################################
################################ CLASSMETHODS ################################
##############################################################################
    
    
    @classmethod
    def FromTree(cls, T, mu, init, interval = None):
        """
        Acts on:    Sample class
        Input:      - T, a MetricTree
                    - mu, a float, the mutation rate of each element of the 
                    Genotype in one increment of time
                    - init, a Genotype which will correspond to node of the  
                    given T tree
                    - interval, a list of two integers, loci in Genome you 
                    want to mutate
        Output:     a Sample with the Genotypes for each leaf of the input 
                    tree where each Genotype was mutated from the init 
                    Genotype using mutation rate mu and with time being the 
                    height of the root of the tree. Mutate at loci indicated
                    by interval, unless interval is None, in which case
                    the whole Genotype was subject to potential mutations.
        Type:       classmethod
        """
        if type(T) is not Tree.MetricTree:
            raise TypeError('First input has to be a MetricTree.')
        if type(mu) is not float:
            raise TypeError('Second input has to be a float.')
        if type(init) is not Genotype:
            raise TypeError('Third input has to be a Genotype.')
        if T.is_leaf:
            return cls({T.name: init})
        else:
            newsample = cls(dict())
            for child in T.children:
                childinit = init.mutate(int(T.height - child.height), mu, 
                                        interval)
                newsample += cls.FromTree(child, mu, childinit, interval)
            return newsample
        
    @classmethod
    def FromForest(cls, F, mu, n, init):
        """
        Acts on:    Sample class
        Input:      - F, a Forest object
                    - mu, a float between 0 and 1, mutation rate
                    - n, a positive integer, length of genotypes
                    - init, Genotype, which will be placed on root of each 
                    tree in the Forest
        Output:     a Sample which was produced by mutating parts of Genotypes 
                    and using the given Forest then collecting all the parts 
                    at the base to procur the Sample
        Type:       classmethod
        """
        trees = []
        for multitree in F.multitrees:
            trees.append(multitree.trees[0])
        recombs = [int(n*x) for x in F.recombinations]
        ind = 0

        while ind < len(recombs) - 1:
            if recombs[ind] == recombs[ind + 1]:
                trees.pop(ind)
                recombs.pop(ind)
            else:
                ind += 1
        sample_list = []
        new_sample = cls.FromTree(trees[0], mu, Genotype(n), [0, recombs[0]])
        sample_list.append(new_sample)
        for i in range(1, len(trees)):
            new_sample = cls.FromTree(trees[i], mu, Genotype(n), 
                                      [recombs[i-1], recombs[i]])
            sample_list.append(new_sample)
        leaves = trees[0].leaves_names
        sample_result = sample_list[0]
        for s in sample_list:
            for leaf in s.keys:
                sample_result[leaf] += s[leaf]
        return sample_result, trees
        