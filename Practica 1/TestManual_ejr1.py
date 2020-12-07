#(c) Alonso Valdivia Quispe - alonso.valdivia.quispe@ucsp.edu.pe
from Ejercicio1 import *

cadena=''
while True:
    cadena = str(input())
    if not cadena:
        break
    print(('NO','SI')[isBalanced(cadena)])