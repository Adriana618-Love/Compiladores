#(c) Alonso Valdivia Quispe - alonso.valdivia.quispe@ucsp.edu.pe

def isBalanced(cadena):
    cadena = cadena.replace(' ','')
    stack = []
    clausulas = [')',']']
    aperturas = ['(','[']
    for character in cadena:
        if character in clausulas and len(stack):
            if character == clausulas[0] and stack.pop() != aperturas[0]:
                return False
            elif character == clausulas[1] and stack.pop() != aperturas[1]:
                return False
        else:
            stack.append(character)
    return not len(stack)

def test_isBalanced(cadena):
    return ('NO','SI')[isBalanced(cadena)]