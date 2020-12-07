from astring import *
from collections import namedtuple

Token = namedtuple('Token', 'palabra indice tipo')


def reconoceNumero(linea,idx,stopChar=[' ']):
    token = ""
    idx_init = idx
    while(idx<len(linea) and not (linea[idx] in stopChar) and isDigit(linea[idx])):
        token+=linea[idx]
        idx+=1
    return Token(token,idx_init,'N'),idx

def reconoceVariable(linea,idx,stopChar=[' ']):
    token = ""
    idx_init = idx
    while(idx<len(linea) and not (linea[idx] in stopChar) and isAlphaNum(linea[idx])):
        token+=linea[idx]
        idx+=1
    return Token(token,idx_init,'V'),idx

def reconoceOperador(linea,idx,stopChar=[' ']):
    token = ""
    idx_init = idx
    while(idx<len(linea) and not isAlphaNum(linea[idx]) and not (linea[idx] in stopChar)):
        token+=linea[idx]
        idx+=1
    return Token(token,idx_init,'O'),idx

def analizadorLexico(linea):
    tokens = []
    idx = 0
    while idx<len(linea):
        if linea[idx].isdigit():
            token,idx = reconoceNumero(linea,idx)
            tokens.append(token)
        elif linea[idx].isalpha():
            token,idx = reconoceVariable(linea,idx)
            tokens.append(token)
        elif linea[idx] == ' ':
            #Omit
            idx+=1
        elif not linea[idx].isdigit() and not linea[idx].isalpha():
            token,idx = reconoceOperador(linea,idx)
            tokens.append(token)
    return tokens
def printTokens(tokens):
    for token in tokens:
        print("Token["+token.palabra+"] : "+"pos = "+str(token.indice)+", tipo = "+str(token.tipo))
    return 0
result = analizadorLexico("variable = temp0 + 20")
print(result)
printTokens(result)
