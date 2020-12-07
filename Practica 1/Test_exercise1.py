#(c) Alonso Valdivia Quispe - alonso.valdivia.quispe@ucsp.edu.pe
import unittest
from Ejercicio1 import test_isBalanced

class Test_Ejercicio1(unittest.TestCase):
    def test_all(self):
        self.assertEqual(test_isBalanced('('), 'NO')
        self.assertEqual(test_isBalanced('((('), 'NO')
        self.assertEqual(test_isBalanced('()()'), 'SI')
        self.assertEqual(test_isBalanced('[   [   (  )   ]  ]'), 'SI')
        self.assertEqual(test_isBalanced(')))'), 'NO')
        self.assertEqual(test_isBalanced('[ )'), 'NO')
        self.assertEqual(test_isBalanced(')]'), 'NO')
        self.assertEqual(test_isBalanced('( )  ['), 'NO')
        self.assertEqual(test_isBalanced('[ (   )'), 'NO')
        self.assertEqual(test_isBalanced('[ (   [)]  ]'), 'NO')
        self.assertEqual(test_isBalanced('[[[[[[[[[[()]]]]]]]]]]'), 'SI')