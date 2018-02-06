from Tree import *
from DistMatr import *

def ProbExp(CT, M):
    """
    Input:  - CT, CombinatorialTree object
            - M, DistMatr object (matrix of changes)
    Output: probability expression
    """
    MT = CT.copy().promote()
    
    leaves = CT.leaves_names
    
    leaves = distmatr.keys
    if len(leaves) == 0:
        return None
    if len(leaves) == 1:
        return MT
    usedleaves = leaves[:2]
    T = cls([leaf1, leaf2], None, 
            distmatr[usedleaves[0],usedleaves[1]]*1./2)
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
