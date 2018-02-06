import Tree
import DistMatr
import inspect

##############################################################################
################################# EXCEPTION ##################################
##############################################################################


class PexpStructureError(Exception):
    pass


##############################################################################
################################# PEXP CLASS #################################
##############################################################################


class Pexp:
    
    
    """Contains parenthesis expression describing a metric balanced tree
    in the form "(ch1,...,ch_k):height", where ch1,...,ch_k are likewise
    expressions for children. For a leaf expression is 'name', where name 
    does not contain '(', ')', ',', or ':'.

    Properties:
        string       -- access or change string attribute of Pexp
        is_leaf      -- logical. True if pexp is represents a leaf
        first_name   -- first name of leaf that appears in Pexp's string
        height       -- height of the node that the pexp represents
        children     -- split pexp into a list of pexp's of children
        split        -- returns 2-tuple of a pexp of list of children in Pexp 
                        form and height
    Methods:
        __str__      -- prints the string inside of the Pexp
        __repr__     -- string expression that if plugged back into python 
                        would result in creation of equivalent Pexp
        == (__eq__)  -- check whether two pexps correspond to isometric trees
        __imatmul__  -- check whether two pexps correspond to isomorphic 
                        combinatorial trees

    ClassMethods:
        JoinChildren -- joins list of Pexp at a given height in a new Pexp
        FromTree     -- creates Pexp out of a Node (tree)
        FromDistMatr -- creates Pexp out of a DistMatr
    """
    
    
##############################################################################
################################## CONSTANTS #################################
##############################################################################


    openparen = '('
    closeparen = ')'
    sepchildren = ','
    sepheight = ':'
    
    
##############################################################################
################################# INITIALIZE #################################
##############################################################################


    def __init__(self, string):
        if type(string) is not str:
            raise PexpStructureError("Input has to be a string.")
        else:
            self.__string = string

            
##############################################################################
########################### ATTRIBUTE PROPERTIES #############################
############################################################################## 


    @property 
    def string(self):
        """
        Acts on:    a Pexp
        Input:      none
        Output:     string attribute of the Pexp
        Type:       property (getter)
        Used in:    is_leaf, first_name, height, children, __str__, __repr__, 
                    _reassemble_pexp, __eq__, __imatmul__, JoinChildren
        """
        return self.__string
       
        
##############################################################################
################################ PROPERTIES ##################################
############################################################################## 
        
    
    @property
    def is_leaf(self):
        """
        Acts on:    a Pexp
        Input:      none
        Output:     a boolean that indicates if the pexp represents a leaf
        Type:       property
        Used in:    children, _reassemble_pexp 
        """
        return self.string[0] != self.openparen
    
    @property
    def first_name(self):
        """
        Acts on:    a Pexp
        Input:      none
        Output:     first name of a leaf that occurs in the Pexp string
        Type:       property
        Used in:    JoinChildren
        """
        name = []
        for char in self.string:
            if char != self.openparen and char != self.sepchildren:
                name.append(char)
            if char == self.sepchildren:
                return name
        return ''.join(name)
    
    @property
    def height(self):
        """
        Acts on:    a Pexp
        Input:      none 
        Output:     an integer, which is the height of the node expressed by 
                    the Pexp
        Type:       property
        Used in:    split, _reassemble_pexp
        """
        height = ''
        for char in self.string[::-1]:
            if char != self.sepheight:
                height = char + height
            else: 
                return float(height)
        return 0.
            
    @property
    def children(self):
        """
        Acts on:    a Pexp
        Input:      none
        Output:     a list of pexps corresponding to all the children
        Type:       property
        Used in:    split, _reassemble_pexp
        """
        if self.is_leaf:
            return []

        children_list = []
        current_child = ''
        level = 0

        for char in self.string[1:] :
            # update level
            if char == self.openparen: 
                level += 1
            elif char == self.closeparen:
                level -= 1
            
            if level == -1:
                # the end
                children_list.append(Pexp(current_child))
                return children_list

            # if level > 0, just keep reading adding to the current child
            elif level > 0:
                current_child += char
            else:
                # we are at level 0
                if char == self.sepchildren:
                    # add curent child to the list, go on reading next child
                    children_list.append(Pexp(current_child))
                    current_child=''
                else :
                    # keep reading
                    current_child += char
        # we shouldn't be here
        raise PexpStructureError('Unbalanced parantheses.')
    
    @property
    def split(self):
        """
        Acts on:    a Pexp
        Input:      none
        Output:     a tuple of a list of pexps corresponding to all the 
                    children and the height
        Type:       property
        Used in:    
        """
        return (self.children, self.height)

    
##############################################################################
############################### CLASS EXCEPTION ##############################
##############################################################################
    
    
    # class PexpStructureError(Exception):
    #     pass
    
    
##############################################################################
################################## METHODS ###################################
############################################################################## 

    def __str__(self):
        """
        Acts on:    a Pexp
        Input:      none
        Output:     string inside of the Pexp
        Short form: print(self)
        """
        return self.string
        
    def __repr__(self):
        """
        Acts on:    a Pexp
        Input:      none
        Output:     string expression that if plugged back into python would 
                    result in creation of equivalent Pexp
        Short form: self (enter)
        """
        return ('Pexp' + self.openparen + '"' + self.string + '"' 
                + self.closeparen)
    
    def _reassemble_pexp(self, include_height = True):
        """
        Acts on:    a Pexp
        Input:      include_height, a boolean
        Output:     if include_height is True it outputs an equivalent Pexp
                    equivalent of a metric tree with all its leaves 
                    alphabetically sorted; if include_height is False it 
                    outputs a sorted Pexp equivalent of a combinatorial tree
                    (no heights included)
        Used in:    __eq__, __imatmul__
        """
        if self.is_leaf:
            return self
        else:
            children = self.children
            for child in children:
                child.__string = child._reassemble_pexp(include_height).string
            return Pexp.JoinChildren(self.height, children, include_height)
       
    def __eq__(self, other):
        """
        Acts on:    a Pexp
        Input:      other, a Pexp
        Output:     a boolean that indicates whether the two Pexps are 
                    equivalent or not
        Short form: ==
        """
        if type(self) is not type(other):
            raise TypeError("Input has to be Pexp.")
        if self.string == other.string:
            return True
        pexp1 = self._reassemble_pexp()
        pexp2 = other._reassemble_pexp()
        answer = (pexp1.string == pexp2.string)
        return answer
    
        
##############################################################################
############################## CLASS METHODS #################################
##############################################################################
        
    
    @classmethod
    def JoinChildren(cls, height, pexp_list, include_height = True):
        """
        Acts on:    Pexp class
        Input:      - height, a positive integer
                    - pexp_list, a list of Pexp objects
        Output:     if include_height is True it outputs a Pexp which is 
                    the combination of all Pexps in the given list with given 
                    height; if include_height is False it outputs a Pexp
                    without any heights included
        Type:       classmethod
        Used in:    FromTree
        """
        if type(height) is not float:
            raise TypeError("First input has to be a float.")
        for elem in pexp_list:
            if type(elem) is not Pexp:
                raise TypeError("Second input has to be a list of Pexps.")
        if type(include_height) is not bool:
            raise TypeError("Third input has to be a boolean.")
        if include_height:
            for pexp_elem in pexp_list:
                if pexp_elem.height >= height:
                    raise ValueError('''First input has to be greater than 
                    the height of all the Pexp in the list.''')
        pexp_list_sorted = sorted(pexp_list, key = lambda x: x.first_name)
        children = cls.openparen
        for i in range(len(pexp_list_sorted)):
            if i != 0:
                children += cls.sepchildren
            children += pexp_list_sorted[i].string
        children += cls.closeparen
        if include_height:
            children += cls.sepheight + str(height)
        return cls(children)
            
    @classmethod
    def FromTree(cls, tree):
        """
        Act on:     Pexp class
        Input:      a Node object
        Output:     Pexp equivalent of the input Node object
        Type:       classmethod
        """
        if (type(tree) is not Tree.CombinatorialTree 
            and type(tree) is not Tree.MetricTree):
            raise TypeError("Input has to be a Combinatorial or Metric Tree.")
        if tree.is_leaf:
            return cls(tree.name)
        else:
            children = []
            for child in tree.children:
                children.append(cls.FromTree(child))
            return cls.JoinChildren(tree.height, children)
        
            
    @classmethod
    def FromDistMatr(cls, m):
        """
        Acts on:    Pexp class
        Input:      m, DistMatr object
        Output:     a Pexp equivalent of the input DistMatr
        Type:       classmethod
        """
        if type(m) is not DistMatr.DistanceMatrix:
            raise TypeError("Input has to be a DistanceMatrix.")
        T = Tree.MetricTree.FromDistMatr(m)
        PE = cls.FromTree(T)
        T.delete()
        return PE

