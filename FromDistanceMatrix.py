    @classmethod
    def FromDistMatr(cls, distmatr):
        if type(distmatr) is not type(DistMatr.DistanceMatrix({'a': {}})):
            raise TypeError("Input has to be a DistMatr.")
        leaves = distmatr.keys
        if len(leaves) == 0:
            return None
        if len(leaves) == 1:
            #create a single node and return it
            T = MetricTree([], None, 0., leaves[0])
            return T
        # make a tree T out of the first two leaves and a node above
        usedleaves = leaves[:2]
        leaf1 = MetricTree([], None, 0., usedleaves[0])
        leaf2 = MetricTree([], None, 0., usedleaves[1])
        T = MetricTree([leaf1, leaf2], None, distmatr[usedleaves[0], usedleaves[1]] * 1. / 2)
        for leaf in leaves[2:]:
            # go through usedleaves and find those with the smallest 
            #     distance to leaf.
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
            # record them to L, the rest is R.
            R = []
            for h in hist_sorted[1:]:
                R += h[1]
            R = sorted(R)
            # find common ancestor of L, ca_L
            for aleaf in T.leaves:
                if L[0] == aleaf.name:
                    baseleaf = aleaf
            ca_L = baseleaf.common_ancestor(L)
            # if ca_L.leaves_names != L then raise Error.
            if ca_L.leaves_names != L:
                raise ValueError("Error.")
            # else check distances from L to R and from leaf to R,
            #   should be d(l,r)=d(leaf,r) for all l in L and r in R
            # If not, raise Error.
            for l in L:
                for r in R:
                    if distmatr[l, r] != distmatr[leaf, r]:
                        raise ValueError("Error.")
            # create a leaf-node corresponding to the leaf
            newleaf = MetricTree([], None, 0., leaf)
            # and one above at the height d(l,leaf)/2
            # insert it above ca_L, thus updating T
            newnode = MetricTree([newleaf, ca_L], None, distmatr[L[0], leaf] * 1./ 2)
            T = T.my_root
            # add leaf to usedleaves.
            usedleaves.append(leaf)
            # continue
            continue
        return T