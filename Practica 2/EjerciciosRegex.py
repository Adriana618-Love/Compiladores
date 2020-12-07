#(c) Alonso Valdivia Quispe alonso.valdivia.quispe@ucsp.edu.pe#

import re

#Ejercicio 1: Reconocer una dirección ip.

def ipcheck(input_ip): #For 999.999.999.999
    pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    test = pat.match(input_ip)
    return not not test

def CheckIp(test_ip): #For 255.255.255.255
    patron = re.compile('(([0-2][0-5][0-5]){1,3}\.){3}(([0-2][0-5][0-5]){1,3})$')
    print (re.match(patron,test_ip))
    return not not re.match(patron,test_ip)


#Ejercicio 2: Reconocer el nombre de una variable

def CheckName(name):
    patron = re.compile('[^0-9][a-zA-Z]')
    return re.match(patron,name)


#Ejercicio 3: Identificar en solicitudes
def CheckTheme(solicitud):
    #Si empieza con 'me gustaria' y finaliza con un '.'
    def MG(solicitud):
        patron = re.compile('(me gustaría )([a-zA-Z0-9]|á|é|í|ó|ú|\ )+\.')
        return re.match(patron,solicitud)
    #Si empieza con 'solicito' y finaliza con un '.'
    def S(solicitud):
        patron = re.compile('(solicito )[a-zA-Z0-9]+\.')
        return re.match(patron,solicitud)
    #Si empieza con 'pido' y finaliza con un '.'
    def P(solicitud):
        patron = re.compile('(pido )[a-zA-Z0-9]+\.')
        return re.match(patron,solicitud)
    if(MG(solicitud) or S(solicitud) or P(solicitud)):
        print(MG(solicitud),S(solicitud),P(solicitud))
    else:
        print('without theme')

print(ipcheck('1.1.1.1'))
