import unittest
from DistMatr import *
from Tree import *
from pexp import *

class TestDistMatrMethods(unittest.TestCase):
    
    def setUp(self):
        
        self.m1 = DistanceMatrix({'a': {}})
        self.m2 = DistanceMatrix({'a': {'b': 10.}, 'b': {}})
        self.m3 = DistanceMatrix({'a': {'b': 6., 'c': 26., 'd': 40.}, 
                                  'b': {'c': 26., 'd': 40.}, 
                                  'c': {'d': 40.}, 
                                  'd': {}})
        
        self.p1 = Pexp('a')
        self.p2 = Pexp('(b,a):5.')
        self.p3 = Pexp('(d,(c,(a,b):3.):13.):20.')
        
        self.ct1 = CombinatorialTree([], None, 'a')
        self.ct2 = CombinatorialTree([], None, 'b')
        self.ct3 = CombinatorialTree([], None, 'c')
        self.ct4 = CombinatorialTree([self.ct1, self.ct2], None)
        self.ct5 = CombinatorialTree([self.ct4, self.ct3], None)
        
        self.mt1 = MetricTree([], None, 0., 'a')
        self.mt2 = MetricTree([], None, 0., 'b')
        self.mt3 = MetricTree([], None, 0., 'c')
        self.mt4 = MetricTree([self.mt1, self.mt2], None, 3.)
        self.mt5 = MetricTree([self.mt4, self.mt3], None, 5.)
        
    def test_init(self):
        with self.assertRaises(TypeError):
            DistanceMatrix({1., 2., 3.})
        with self.assertRaises(DistMatrStructureError):
            DistanceMatrix({'a': 1., 'b': 2., 'd': 3.})

    def test_data(self):
        self.assertEqual(self.m1.data, {'a': {}})
        self.assertEqual(self.m2.data, {'a': {'b': 10.}, 'b': {}})
        self.assertEqual(self.m3.data, {'a': {'b': 6., 'c': 26., 'd': 40.}, 
                                        'b': {'c': 26., 'd': 40.}, 
                                        'c': {'d': 40.}, 
                                        'd': {}})
        
        
    def test_size(self):
        self.assertEqual(self.m1.size, 1)
        self.assertEqual(self.m2.size, 4)
        self.assertEqual(self.m3.size, 16)
        
    def test_keys(self):
        self.assertEqual(self.m1.keys, ['a'])
        self.assertEqual(self.m2.keys, ['a', 'b'])
        self.assertEqual(self.m3.keys, ['a', 'b', 'c', 'd'])
        
    def test_check_keys(self):
        with self.assertRaises(TypeError):
            self.m1._check_keys(('a'))
        with self.assertRaises(TypeError):
            self.m1._check_keys(('a', 'c', 'd'))
        with self.assertRaises(TypeError):
            self.m1._check_keys(('a', 1))
        with self.assertRaises(TypeError):
            self.m1._check_keys((1, 'a'))
        with self.assertRaises(ValueError):
            self.m1._check_keys(('a', 'b'), True)
            
    def test_getitem(self):
        self.assertEqual(self.m1['a', 'a'], 0.)
        self.assertEqual(self.m2['a', 'a'], 0.)
        self.assertEqual(self.m2['a', 'b'], 10.)
        self.assertEqual(self.m2['b', 'a'], 10.)
        self.assertEqual(self.m2['b', 'b'], 0.)
        self.assertEqual(self.m3['a', 'a'], 0.)
        self.assertEqual(self.m3['a', 'b'], 6.)
        self.assertEqual(self.m3['a', 'c'], 26.)
        self.assertEqual(self.m3['a', 'd'], 40.)
        self.assertEqual(self.m3['b', 'a'], 6.)
        self.assertEqual(self.m3['b', 'b'], 0.)
        self.assertEqual(self.m3['b', 'd'], 40.)
        self.assertEqual(self.m3['b', 'c'], 26.)
        self.assertEqual(self.m3['c', 'a'], 26.)
        self.assertEqual(self.m3['c', 'b'], 26.)
        self.assertEqual(self.m3['c', 'c'], 0.)
        self.assertEqual(self.m3['c', 'd'], 40.)
        self.assertEqual(self.m3['d', 'a'], 40.)
        self.assertEqual(self.m3['d', 'b'], 40.)
        self.assertEqual(self.m3['d', 'c'], 40.)
        self.assertEqual(self.m3['d', 'd'], 0.)
        
    def test_add_new_key(self):
        m4 = DistanceMatrix({'a': {'d': 10.}, 'd': {}})
        m4._add_new_key('a')
        self.assertEqual(m4, DistanceMatrix({'a': {'d': 10.}, 'd': {}}))
        m4._add_new_key('b')
        self.assertEqual(m4, 
                         DistanceMatrix({'a': {'b': None, 'd': 10.},
                                         'b': {'d': None}, 
                                         'd': {}}))
        m4._add_new_key('e')
        self.assertEqual(m4, 
                         DistanceMatrix({'a': {'b': None, 'd': 10., 'e': None},
                                         'b': {'d': None, 'e': None}, 
                                         'd': {'e': None}, 
                                         'e': {}}))
        
    def test_setitem(self):
        with self.assertRaises(DistMatrStructureError):
            self.m1.__setitem__(('a', 'a'), 5.)
        
        m4 = DistanceMatrix({'a': {'d': 10.}, 'd': {}})
        
        m4.__setitem__(('a', 'd'), 20.)
        self.assertEqual(m4, DistanceMatrix({'a': {'d': 20.}, 'd': {}}))
        m4.__setitem__(('a', 'b'), 10.)
        self.assertEqual(m4, DistanceMatrix({'a': {'b': 10., 'd': 20.},
                                             'b': {'d': None}, 
                                             'd': {}}))
        m4.__setitem__(('e', 'b'), 4.)
        self.assertEqual(m4, DistanceMatrix({'a': {'b': 10., 'd': 20., 'e': None}, 
                                             'b': {'d': None, 'e': 4.}, 
                                             'd': {'e': None}, 
                                             'e': {}}))
    def test_eq(self):
        with self.assertRaises(TypeError):
            self.m1.__eq__(5)
        self.assertEqual(self.m1, DistanceMatrix({'a': {}}))
        self.assertEqual(self.m2, DistanceMatrix({'a': {'b': 10.}, 'b': {}}))
        self.assertEqual(self.m3, DistanceMatrix({'a': {'b': 6., 'c': 26., 'd': 40.}, 
                                                  'b': {'c': 26., 'd': 40.}, 
                                                  'c': {'d': 40.}, 
                                                  'd': {}}))
            
    def test_copy(self):
        m1 = DistanceMatrix({'a': {}})
        m2 = DistanceMatrix({'a': {'b': 10.}, 'b': {}})
        m3 = DistanceMatrix({'a': {'b': 6., 'c': 26., 'd': 40.},
                             'b': {'c': 26., 'd': 40.}, 
                             'c': {'d': 40.}, 
                             'd': {}})
        
        self.assertEqual(self.m1.copy(), m1)
        self.assertEqual(self.m2.copy(), m2)
        self.assertEqual(self.m3.copy(), m3)
        
        
    def test_submatrix(self):
        with self.assertRaises(TypeError):
            self.m3.submatrix(['a', 'b', 1])
        self.assertEqual(self.m1.submatrix([]), DistanceMatrix(dict()))
        self.assertEqual(self.m1.submatrix(['a']), self.m1)
        self.assertEqual(self.m2.submatrix(['a']), self.m1)
        self.assertEqual(self.m2.submatrix(['b']), DistanceMatrix({'b': {}}))
        self.assertEqual(self.m2.submatrix(['a', 'b']), self.m2)
        self.assertEqual(self.m3.submatrix(['a']), self.m1)
        self.assertEqual(self.m3.submatrix(['a', 'b']), DistanceMatrix({'a': {'b': 6.}, 'b': {}}))
        self.assertEqual(self.m3.submatrix(['c', 'b']), 
                         DistanceMatrix({'b': {'c': 26.}, 'c': {}}))
        self.assertEqual(self.m3.submatrix(['c', 'd', 'b']), 
                         DistanceMatrix({'b': {'c': 26., 'd': 40.}, 'c': {'d': 40.}, 'd': {}}))
        self.assertEqual(self.m3.submatrix(['b', 'c', 'd', 'a']), self.m3)   
        
    def test_append(self):
        with self.assertRaises(TypeError):
            self.m3.append(1, {'a': 2.})
        with self.assertRaises(TypeError):
            self.m3.append('a', {2, 3, 4})
        self.assertEqual(self.m1.append('b', {'a': 2.}), DistanceMatrix({'a': {'b': 2.}, 'b': {}}))
        self.assertEqual(self.m2.append('d', {'a': 4., 'b': 4.}), 
                         DistanceMatrix({'a': {'b': 10., 'd': 4.}, 
                                         'b': {'d': 4.}, 
                                         'd': {}}))
        
    def test_FromTree(self):
        with self.assertRaises(TypeError):
            DistanceMatrix.FromTree(self.m1)
        self.assertEqual(DistanceMatrix.FromTree(self.mt1), DistanceMatrix({'a': {}}))
        self.assertEqual(DistanceMatrix.FromTree(self.mt2), DistanceMatrix({'b': {}}))
        self.assertEqual(DistanceMatrix.FromTree(self.mt4), DistanceMatrix({'a': {'b': 6.}, 'b': {}}))
        self.assertEqual(DistanceMatrix.FromTree(self.mt5), DistanceMatrix({'a': {'b': 6., 'c': 10.}, 'b': {'c': 10.}, 'c': {}}))
        self.assertEqual(DistanceMatrix.FromTree(self.ct1), DistanceMatrix({'a': {}}))
        self.assertEqual(DistanceMatrix.FromTree(self.ct2), DistanceMatrix({'b': {}}))
        self.assertEqual(DistanceMatrix.FromTree(self.ct4), DistanceMatrix({'a': {'b': 2.}, 'b': {}}))
        self.assertEqual(DistanceMatrix.FromTree(self.ct5), DistanceMatrix({'a': {'b': 2., 'c': 4.}, 'b': {'c': 4.}, 'c': {}}))  
        
    def test_FromPexp(self):
        with self.assertRaises(TypeError):
            DistanceMatrix.FromTree(self.m1)
        self.assertEqual(DistanceMatrix.FromPexp(self.p1), DistanceMatrix({'a': {}}))
        self.assertEqual(DistanceMatrix.FromPexp(self.p2), DistanceMatrix({'a': {'b': 10.}, 'b': {}}))
        self.assertEqual(DistanceMatrix.FromPexp(self.p3), 
                         DistanceMatrix({'a': {'b': 6., 'c': 26., 'd': 40.}, 
                                         'b': {'c': 26., 'd': 40.}, 
                                         'c': {'d': 40.}, 
                                         'd': {}}))

if __name__ == '__main__':
    unittest.main()