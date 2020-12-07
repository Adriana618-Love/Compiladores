#(c) Alonso Valdivia Quispe - alonso.valdivia.quispe@ucsp.edu.pe
import unittest

from Ejercicio2 import test_checkGerund

class Test_ejercicio2(unittest.TestCase):
    def test_all(self):
        self.assertEqual(test_checkGerund('amar   amando'), 'SI')
        self.assertEqual(test_checkGerund('llover  lloviendo'), 'SI')
        self.assertEqual(test_checkGerund('reir  riendo'), 'SI')
        self.assertEqual(test_checkGerund('abatir   abatiendo'), 'SI')
        self.assertEqual(test_checkGerund('caer    caindo'), 'NO')
        self.assertEqual(test_checkGerund('correr  correndo'), 'NO')
        self.assertEqual(test_checkGerund('salir   salendo'), 'NO')