from afilesmgmt import File
import constants
from program import Parser

class Produccion:
    def __init__(self):
        self.izq=[]
        self.der=[]
    def print(self):
        for i in self.der:
            print(self.izq +" -> "+' '.join(i))
    def getIzq(self):
        return self.izq.strip()
    def getProduccion(self):
        return self.der
    def addDer(self,NEWDER):
        for elem in NEWDER:
            self.der.append(elem)

class Gramatica:
    def __init__(self):
        self.nodo_inicial='goal'
        self.produccion = []
        self.terminales = []
        self.nonterminales = []

    def setINIT(self,inicial):
        self.nodo_inicial=inicial

    def getIndex(self,izq):
        i = 0
        for nt in self.nonterminales:
            if(nt==izq):
                return i
            i+=1
        return -1

    def cargar(self,file,separatorUnion='|',separator='::='):
        Lines = file.get_all_lines()
        #print("lineas",Lines)
        simbols = []
        for line in Lines:
            #print(line,"f")
            pdc = line.split(separator)
            if(len(pdc)==1):
                continue
            #print("Se trato")
            my_izq = pdc[0]
            my_der = pdc[1]
            expand = my_der.split(separatorUnion)
            expand = self.Treat(expand)
            #print("expand",expand)
            #print("izq",my_izq)
            if(not (my_izq.strip() in self.nonterminales)):
                ###################################################################
                self.nonterminales.append(my_izq.strip()) #Guardo los estados no terminales
                ###################################################################
                newProduccion = Produccion()
                newProduccion.izq = my_izq#añado izq
                newProduccion.der = expand#añado der
                self.produccion.append(newProduccion)
                #print("no existia")
            else:
                idx = self.getIndex(my_izq.strip())
                #print(idx,self.produccion[idx].getIzq())
                self.produccion[idx].addDer(expand)#añado nuevas der
                #print("ya existia")

            ######################Trucazo para encontrar los terminales#########
            for ders in expand:
                for sim in ders:
                    if(not (sim in simbols)):
                        simbols.append(sim)
            ####################################################################
        #print("simbols:",simbols)
        self.fillT(simbols)
        #print(self.nonterminales)
        #print("cargado")
    def fillT(self,simbols):
        for ter in simbols:
            if(not(ter in self.nonterminales)):
                self.terminales.append(ter)
    def print(self):
        for p in self.produccion:
            p.print()
    def getProduccion(self,izq):
        return self.produccion[self.getIndex(izq)].getProduccion()
    def Treat(self,my_der):
        produccion = []
        for der in my_der:
            der = der.strip() #Elimino espacio en blanco del inicio y del final
            produccion.append(der.split(' '))
        return produccion
    def unir(self,ps,pc):
        for p in ps:
            pc.append(p)
        #print("pc",pc)
        return pc
    def concatenate(self,pc,rs):
        for ele in rs:
            pc.append(ele)
    def getPrimero(self, prim):
        producciones = self.getProduccion(prim)#[[],[],[]]
        #print(producciones)
        primerosSimple=[]
        primerosCompuestos=[]
        for prod in producciones:
            if(prod[0] in self.nonterminales):
                self.concatenate(primerosCompuestos,self.getPrimero(prod[0]))
            else:
                primerosSimple.append(prod[0])
            #print("Estoy en ",prim," Y mis pc son",primerosCompuestos)
        #print("ps",primerosSimple)
        primeros = self.unir(primerosSimple,primerosCompuestos)
        #print(primeros)
        return primeros

    def getProducciones(self):
        return self.produccion

    def getPrimeros(self):
        self.primeros = {}
        for nodo in self.nonterminales:
            self.primeros[nodo] = self.getPrimero(nodo)
        return self.primeros

    def getNonterminal(self,miniprod,i):
        for idx in range(i, len(miniprod)):
            if(miniprod[idx] in self.nonterminales):
                return idx
        return -1
    def add(self,obt,tmp):
        for i in tmp:
            if not (i in obt):
                obt.append(i)
    def getSiguiente(self,nt,sgts):
        producciones = self.produccion
        for prod in producciones:
            for der in prod.der:
                #print("analizando der",der)
                for idx in range(0,len(der)):
                    if(nt == der[idx]):
                        #print("nt==der[idx]")
                        #print("pre",sgts[nt])
                        if idx==len(der)-1:
                            #print("sin derecha")
                            self.add(sgts[der[idx]],sgts[prod.getIzq()])
                        else:
                            #print("con derecha")
                            if der[idx+1] in self.terminales:
                                if not(der[idx+1] in sgts[der[idx]]):
                                    sgts[der[idx]].append(der[idx+1])
                            else:
                                temp = self.getPrimero(der[idx+1])
                                #print("temp",temp)
                                if 'lambda' in temp:
                                    temp.remove('lambda')#Remover lambda
                                    self.add(temp,sgts[prod.getIzq()])
                                self.add(sgts[der[idx]],temp)
        #print(sgts[nt])


    def getSiguientes(self):
        self.siguientes = {}
        #print(self.nonterminales)
        #print(self.terminales)
        for i in self.nonterminales:
            self.siguientes[i]=[]
        self.siguientes[self.nodo_inicial].append(constants.DOLAR)
        for nt in self.nonterminales:
            #print("works on",nt)
            self.getSiguiente(nt,self.siguientes)
        return self.siguientes
    def createTabla(self):
        self.tas = dict({'':{}})
        for p in self.produccion:
            self.tas[p.getIzq()] = {}
            #print(p.getProduccion())
            if(len(p.getProduccion()) == 1):
                for i in self.primeros[p.getIzq()]:
                    self.tas[p.getIzq()][i] = p.getProduccion()[0]
                    #Puede ocurrir que la produccion sea A := lambda, pero concluí que en dicho caso la gramática no sería LL(1)
            else:
                for i in p.getProduccion():
                    if i[0] != 'lambda': #SI NO ES LAMBDA
                        if i[0] in self.terminales:
                            self.tas[p.getIzq()][i[0]] = i
                        else:
                            PrimTemp = self.getPrimero(i[0])
                            for term in PrimTemp:
                                if term != 'lambda':
                                    self.tas[p.getIzq()][term] = i
                    else:
                        for f in self.siguientes[p.getIzq()]:
                            self.tas[p.getIzq()][f] = i
        return self.tas
    def printTAS(self):
        for fst_key,sub_dict in self.tas.items():
            for snd_key, produccion in sub_dict.items():
                print(fst_key,snd_key,produccion)

class TAS:
    def __init__(self):
        self.tablasintactica = dict({'':{}})
    def Build(self,Gramatica = None):
        self.tablasintactica['E']={}
        self.tablasintactica['E']['('] = ["T","Ep"]
        self.tablasintactica['E']['num'] = ["T","Ep"]
        self.tablasintactica['Ep']={}
        self.tablasintactica['Ep']['id'] = ["T","Ep"]
        self.tablasintactica['Ep']['+'] = ["+","T","Ep"]
        self.tablasintactica['Ep']['-'] = ["-","T","Ep"]
        self.tablasintactica['Ep'][')'] = ["lambda"]
        self.tablasintactica['Ep']['$'] = ["lambda"]
        self.tablasintactica['T']={}
        self.tablasintactica['T']['('] = ["F","Tp"]
        self.tablasintactica['T']['num'] = ["F","Tp"]
        self.tablasintactica['T']['id'] = ["F","Tp"]
        self.tablasintactica['Tp']={}
        self.tablasintactica['Tp']['+'] = ["lambda"]
        self.tablasintactica['Tp']['-'] = ["lambda"]
        self.tablasintactica['Tp']['*'] = ["*","F","Tp"]
        self.tablasintactica['Tp']['/'] = ["/","F","Tp"]
        self.tablasintactica['Tp'][')'] = ["lambda"]
        self.tablasintactica['Tp']['$'] = ["lambda"]
        self.tablasintactica['F']={}
        self.tablasintactica['F']['('] = ["(","E",")"]
        self.tablasintactica['F']['num'] = ["num"]
        self.tablasintactica['F']['id'] = ["id"]

    def print(self):
        for fst_key,sub_dict in self.tablasintactica.items():
            for snd_key, produccion in sub_dict.items():
                print(fst_key,snd_key,produccion)

def printDict(dicti):
    [print(key, value) for key, value in dicti.items()]

############-CARGANDO UNA GRAMÁTICA DESDE UN .TXT-#################
#my_file = File('test.txt')
#my_file = File('grammarTest.txt')
my_file = File('sos.txt')
my_grammar = Gramatica()
my_grammar.setINIT('goal')
my_grammar.cargar(my_file,'@')
print(my_grammar.nonterminales)
print(my_grammar.terminales)
#my_grammar.print()
print(printDict(my_grammar.getPrimeros()))
print("-------------")
print(printDict(my_grammar.getSiguientes()))
print("-------------")
my_grammar.createTabla()
my_grammar.printTAS()
#print(len(my_grammar.produccion))
#my_grammar.print()
#print(my_grammar.getProduccion('Ep'))
#print(my_grammar.nonterminales)
#print(my_grammar.terminales)
#print(my_grammar.getPrimero('E'))
#print(my_grammar.getPrimeros())
############-CREANDO LA TABLA ESTÁTICAMENTE-#################
tabla = TAS()
tabla.Build()
#tabla.print()
#Se debe usar un diccionario para guardar las producciones

#######################VAMO CON EL PARSER######################################
parser  = Parser(my_grammar.terminales,my_grammar.tas)
print(parser.parse(['(', 'id', '+', 'id', ')', '+', 'id', '$']))