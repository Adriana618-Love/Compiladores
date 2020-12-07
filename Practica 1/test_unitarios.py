#(c) Alonso Valdivia Quispe - alonso.valdivia.quispe@ucsp.edu.pe
import unittest
import Test_exercise1
import Test_exercise2

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(Test_exercise1))
    suite.addTests(loader.loadTestsFromModule(Test_exercise2))
    runner = unittest.TextTestRunner(verbosity=3)
    results = runner.run(suite)