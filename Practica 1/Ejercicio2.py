#(c) Alonso Valdivia Quispe - alonso.valdivia.quispe@ucsp.edu.pe
from astring import *

def geneararGerundio(cadena):
    standarize(cadena)
    if cadena in special_word:
        return special_word[cadena]
    sufix = cadena[-2:]
    if sufix == 'ar':
        return rreplace(cadena,'ar','ando',1)
    elif sufix in ['er','ir']:
        if isVowel(cadena[-3]):
            return replace_str_index(cadena,'yendo',len(cadena)-2)
        return replace_str_index(cadena,'iendo',len(cadena)-2)
    return cadena

def checkGerund(cadena):
    word,p_gerund = cadena.split()[0],cadena.split()[1]
    return geneararGerundio(word) == standarize(p_gerund)

def test_checkGerund(cadena):
    return ('NO','SI')[checkGerund(cadena)]