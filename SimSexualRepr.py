from sample import *
from Tree import *
import random as rnd
import numpy as np

def simulator(n, N, rho, mu, m, T):
    # initilizing sample of N Genotypes of len n
    s = Sample(dict())
    forest = []
    for i in range(N):
        s[str(i)] = Genotype(n)
        for i2 in range(n):
            forest.append((MetricTree([], None, float(T + 1)), (i, i2)))
        
    for t in range(T):
        time = T - t
        
        keys_list = s.keys
        pair_list = []
        tree_list = []
        while len(keys_list) > 0:
            ind1 = rnd.randrange(0, len(keys_list))
            parent_1 = s[keys_list.pop(ind1)]
            ind2 = rnd.randrange(0, len(keys_list))
            parent_2 = s[keys_list.pop(ind2)]
            tree_list.append((forest[ind1], forest[ind2]))
            pair_list.append((parent_1, parent_2))
        s = Sample(dict())
        for i in range(N//2):
            I = rnd.randrange(0, len(pair_list))
            parent_pair = pair_list[I]
            ind = rnd.randint(0,1)
            parent_copied = parent_pair[ind]
            newgenome = Genotype(n)
            s[str(i)] = newgenome
            count = 0
            for l in range(n):
                newgenome[l] = parent_copied[l]
                if rnd.random() < mu:
                    newgenome.switch(l)
                count += 1
                if rnd.random() < rho*np.exp(-rho*count):
                    ind = (ind + 1) % 2
                    parent_copied = parent_pair[ind]
                    count = 0
            s[str(i)] = newgenome
                        
                        
#             num_children = rnd.randint(2,100)
#             for k in range(num_children):
#                 ind = rnd.randint(0,1)
#                 parent_copied = parent_pair[ind]
#                 newgenome = Genotype(n)
#                 children.append(newgenome)
#                 count = 0
#                 for l in range(n):
#                     newgenome[l] = parent_copied[l]
#                     if rnd.random() < mu:
#                         newgenome.switch(l)
                    
#                     count += 1
#                     if rnd.random() < rho*np.exp(-rho*count):
#                         ind = (ind + 1) % 2
#                         parent_copied = parent_pair[ind]
#                         count = 0
        
        ###
        # s_children = Sample(dict())
        # for i in range(N):
        #     keys_list = s.keys
        #     parent_1 = s[keys_list.pop(rnd.randrange(0, len(keys_list)))]
        #     parent_2 = s[keys_list.pop(rnd.randrange(0, len(keys_list)))]
        #     parent_pair = (parent_1, parent_2)
        #     ind = rnd.randint(0,1)
        #     parent_copied = parent_pair[ind]
        #     newgenome = Genotype(n)
        #     s_children[str(i)] = newgenome
        #     count 0
        #     for k in range(n):
        #         newgenome[k] = parent_copied[k]
        #         if rnd.random() < mu:
        #             newgenome.switch(k)
        #         count += 1
        #         if rnd.random() < rho*np.exp(-rho*count):
        #             ind = (ind + 1) % 2
        #             parent_copied = parent_pair[ind]
        #             count = 0
                
        
        ###

        # while len(children) > N:
        #     children.pop(rnd.randrange(0, len(children)))
        # if len(children) < N:
        #     print('Oh no, number of children less than appropriate.')
        # s = Sample(dict())
        # for i in range(N):
        #     s[str(i)] = children[i]
    keys_list = s.keys
    while len(keys_list) > m:
        keys_list.pop(rnd.randrange(0, len(keys_list)))
    final_sample = Sample(dict())
    for i in range(m):
        final_sample[str(i)] = s[keys_list[i]]
    return final_sample