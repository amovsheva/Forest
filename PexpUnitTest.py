import unittest
from Tree import *
from pexp import *

class TestPexpMethods(unittest.TestCase):
    
    def setUp(self):
        
        self.p1 = Pexp('a')
        self.p2 = Pexp('(b,a):5')
        self.p3 = Pexp('(d,(c,(a,b):3):13):20')
        
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
        with self.assertRaises(PexpStructureError):
            Pexp(1)
    
    def test_string(self):
        self.assertEqual(self.p1.string, 'a')
        self.assertEqual(self.p2.string, '(b,a):5')
        self.assertEqual(self.p3.string, '(d,(c,(a,b):3):13):20')
        
    def test_is_leaf(self):
        self.assertTrue(self.p1.is_leaf)
        self.assertFalse(self.p2.is_leaf)
        self.assertFalse(self.p3.is_leaf)
        
    def test_first_name(self):
        self.assertEqual(self.p1.first_name, 'a')
        self.assertEqual(self.p2.first_name, 'b')
        self.assertEqual(self.p3.first_name, 'd')
        
    def test_height(self):
        self.assertEqual(self.p1.height, 0)
        self.assertEqual(self.p2.height, 5)
        self.assertEqual(self.p3.height, 20)
        
        
    def test_children(self):
        self.assertEqual(self.p1.children, [])
        self.assertEqual(self.p2.children, [Pexp('b'), Pexp('a')])
        self.assertEqual(self.p3.children, [Pexp('d'), Pexp('(c,(a,b):3):13')])
        
    def test_split(self):
        self.assertEqual(self.p1.split, ([], 0))
        self.assertEqual(self.p2.split, ([Pexp('b'), Pexp('a')], 5))
        self.assertEqual(self.p3.split, ([Pexp('d'), Pexp('(c,(a,b):3):13')], 20))
        
    def test_reassemble_pexp(self):
        self.assertEqual(self.p1._reassemble_pexp(), self.p1)
        self.assertEqual(self.p2._reassemble_pexp(), Pexp('(a,b):5'))
        self.assertEqual(self.p2._reassemble_pexp(False), Pexp('(a,b)'))
        self.assertEqual(self.p3._reassemble_pexp(), Pexp('(((a,b):3,c):13,d):20'))
        self.assertEqual(self.p3._reassemble_pexp(False), Pexp('(((a,b),c),d)'))
        
    def test_eq(self):
        with self.assertRaises(TypeError):
            self.p1.__eq__('a')
            
        self.assertTrue(self.p1.__eq__(self.p1))
        self.assertTrue(self.p1.__eq__(Pexp('a')))
        self.assertFalse(self.p1.__eq__(Pexp('ab')))
        self.assertTrue(self.p2.__eq__(self.p2))
        self.assertTrue(self.p2.__eq__(Pexp('(b,a):5')))
        self.assertTrue(self.p2.__eq__(Pexp('(a,b):5')))
        self.assertFalse(self.p2.__eq__(Pexp('(a,b):4')))
        self.assertFalse(self.p2.__eq__(Pexp('(a,c):5')))
        self.assertFalse(self.p2.__eq__(Pexp('(c,a):5')))
        
        self.assertTrue(self.p3.__eq__(Pexp('(((a,b):3,c):13,d):20')))
        self.assertTrue(self.p3.__eq__(Pexp('(d,(c,(a,b):3):13):20')))
        self.assertTrue(self.p3.__eq__(Pexp('(d,((a,b):3,c):13):20')))
        self.assertTrue(self.p3.__eq__(self.p3))

        self.assertFalse(self.p3.__eq__(Pexp('(((a,b):3,c):13,d):21')))
        self.assertFalse(self.p3.__eq__(Pexp('(((a,c):3,c):13,d):20')))
        self.assertFalse(self.p3.__eq__(Pexp('(((a,b):3,c):13,e):20')))
        
    def test_JoinChildren(self):
        with self.assertRaises(TypeError):
            Pexp.JoinChildren('a', [Pexp('a'), Pexp('(b,c):3')])
        with self.assertRaises(TypeError):
            Pexp.JoinChildren(5., ['a', Pexp('(b,c):3')])
        with self.assertRaises(TypeError):
            Pexp.JoinChildren(5., [Pexp('a'), Pexp('(b,c):3')], 1)
        with self.assertRaises(TypeError):
            Pexp.JoinChildren(2, [Pexp('a'), Pexp('(b,c):3.0')])
            
        self.assertEqual(Pexp.JoinChildren(5., [Pexp('a'), Pexp('(b,c):3.')]), 
                         Pexp('(a,(b,c):3.):5.'))
        self.assertEqual(Pexp.JoinChildren(5., [Pexp('a'), Pexp('(b,c):3.')], False), 
                         Pexp('(a,(b,c):3.)'))
        self.assertEqual(Pexp.JoinChildren(5., [Pexp('(b,c):3.'), Pexp('a')]), 
                         Pexp('(a,(b,c):3.):5.'))
        self.assertEqual(Pexp.JoinChildren(5., [Pexp('(b,c):3.'), Pexp('a')], False), 
                         Pexp('(a,(b,c):3.)'))
        self.assertEqual(Pexp.JoinChildren(10., [Pexp('(b,c):3.'), Pexp('a'), Pexp('(e,d):8.')]), 
                         Pexp('(a,(b,c):3.,(e,d):8.):10.'))
        self.assertEqual(Pexp.JoinChildren(10., [Pexp('(b,c):3.'), Pexp('a'), Pexp('(e,d):8.')], False), 
                         Pexp('(a,(b,c):3.,(e,d):8.)'))

        
        
    def test_FromTree(self):
        with self.assertRaises(TypeError):
            Pexp.FromTree(self.p1)
        self.assertEqual(Pexp.FromTree(self.ct1), Pexp('a'))
        self.assertEqual(Pexp.FromTree(self.ct4), Pexp('(a,b):1.'))
        self.assertEqual(Pexp.FromTree(self.ct5), Pexp('((a,b):1.,c):2.'))
        
        self.assertEqual(Pexp.FromTree(self.mt1), Pexp('a'))
        self.assertEqual(Pexp.FromTree(self.mt4), Pexp('(a,b):3.'))
        self.assertEqual(Pexp.FromTree(self.mt5), Pexp('((a,b):3.,c):5.'))
        
    def test_FromDistMatr(self):
        with self.assertRaises(TypeError):
            Pexp.FromTree(self.p1)
        self.assertEqual(Pexp.FromDistMatr(DistMatr.DistanceMatrix({'a': {}})), 
                         Pexp('a'))
        self.assertEqual(Pexp.FromDistMatr(DistMatr.DistanceMatrix({'a': {'b': 2.}, 'b': {}})), 
                         Pexp('(a,b):1.'))
        

if __name__ == '__main__':
    unittest.main()