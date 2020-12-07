#(c) Alonso Valdivia Quispe - alonso.valdivia.quispe@ucsp.edu.pe
from Ejercicio2 import *

while True:
    cadena = str(input())
    if not cadena:
        break
    print(('NO','SI')[checkGerund(cadena)])