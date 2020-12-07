from afilesmgmt import File

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
        self.der=self.der[0]
        return self.der

class Gramatica:
    def __init__(self):
        self.produccion = []
        self.terminales = []
        self.nonterminales = []

    def cargar(self,file,separator=':='):
        Lines = file.get_all_lines()
        for line in Lines:
            pdc = line.split(separator)
            my_izq = pdc[0]
            ###################################################################
            self.nonterminales.append(my_izq) #Guardo los estados no terminales
            ###################################################################
            my_der = pdc[1]
            expand = my_der.split('|')
            newProduccion = Produccion()
            newProduccion.izq = my_izq
            newProduccion.der = self.Treat(expand)
            self.produccion.append(newProduccion)
        pass
    def print(self):
        for p in self.produccion:
            p.print()
    def getProduccion(self,izq):
        producciones = []
        for p in self.produccion:
            if(p.getIzq()==izq):
                producciones.append(p.getProduccion())
        return producciones
    def Treat(self,my_der):
        produccion = []
        for der in my_der:
            der = der.strip() #Elimino espacio en blanco del inicio y del final
            produccion.append(der.split(' '))
        return produccion

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

############-CARGANDO UNA GRAMÁTICA DESDE UN .TXT-#################
my_file = File('test.txt')
my_grammar = Gramatica()
my_grammar.cargar(my_file)
#my_grammar.print()
print(my_grammar.getProduccion('Ep'))
############-CREANDO LA TABLA ESTÁTICAMENTE-#################
tabla = TAS()
tabla.Build()
#tabla.print()
#Se debe usar un diccionario para guardar las producciones