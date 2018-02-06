from Tree import *
import random as rnd

class BackSimNode(CombinatorialTree):
    def __init__(self, parents, break_points, height, children = None, index = None):
        self.__parents = parents 
        self.__break_points = break_points
        self.__height = height
        self.__children = children
        self.__index = index
    
    @property
    def parents(self):
        return self.__parents
    
    @property
    def break_points(self):
        return self.__break_points
    
    @property
    def height(self):
        return self.__height
    
    @property
    def children(self):
        return self.__children
    
    @property 
    def index(self):
        return self.__index
    
    @property
    def all_children_first(self):
        for child in self.children:
            if child[1] == 's':
                return False
        return True
    
    @property
    def all_children_second(self):
        for child in self.children:
            if child[1] == 'f':
                return False
        return True
    
    def children_breakpoints(self):
        break_points_list = []
        for child in self.children:
            break_points_list.append(child[2])
        return break_points_list

    
    
    def copy(self):
        children = []
        for child in self.children:
            children.append(child.copy())
        return BackSimNode(self.parents, self.break_points, self.height, children)
    
    @classmethod
    def Evolve(cls, N, T):
        parent_list = []
        for i in range(N):
            newparent = BackSimNode([], [], 1., index = i)
            parent_list.append(newparent)
            
        first_gen = []
        parent_pair_ind = list(range(N//2))
        for i in range(N):
            ind = parent_pair_ind.pop(rnd.randrange(0, len(parent_pair_ind)))
            delta_ind = rnd.randint(0,1)
            if delta_ind == 0:
                first_parent = parent_list[ind]
                second_parent = parent_list[ind]
            if delta_ind == 1:
                first_parent = parent_list[ind+1]
                second_parent = parent_list[ind]
            break_point = rnd.random()
            newnode = BackSimNode([first_parent, second_parent], [break_point], 0.)
            first_gen.append(newnode)
            first_parent.__children.append((newnode, 'f', break_point))
            second_parent.__children.append((newnode, 's', break_point))
            
        for t in range(T-1):
            first_gen = parent_list
            parent_list = []
            for i in range(N):
                newparent = BackSimNode([], [], t+1, index = i)
                parent_list.append(newparent)
                if first_gen(i).children == []:
                    first_gen.pop(i)
            parent_pair_ind = list(range(N//2))
            for node in first_gen:
                ind = parent_pair_ind.pop(rnd.randrange(0, len(parent_pair_ind)))
                delta_ind = rnd.randint(0,1)
                if delta_ind == 0:
                    first_parent = parent_list[ind]
                    second_parent = parent_list[ind]
                if delta_ind == 1:
                    first_parent = parent_list[ind+1]
                    second_parent = parent_list[ind]
                node.__parents = [first_parent, second_parent]
                
                break_point = rnd.random()
                
                if node.all_children_first and break_point >= max(node.children_breakpoints()):
                    break_point = max(node.children_breakpoints())
                    node.__parents.pop(1)
                    node.parents[0].__children.append((node, 'f', break_point))
                elif node.all_children_second and break_point <= min(node.children_breakpoints()):
                    break_point = min(node.children_breakpoints())
                    node.__parents.pop(0)
                    node.parents[0].__children.append((node, 's', break_point))
                else:
                    node.__break_point = break_point
                    first_parent.__children.append((node, 'f', break_point))
                    second_parent.__children.append((node, 's', break_point))

                node.__index = t
        return parent_list