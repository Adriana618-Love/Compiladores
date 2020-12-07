#(c) Alonso Valdivia Quispe - alonso.valdivia.quispe@ucsp.edu.pe
def find_all(a_str, sub):

    def heart(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches
    return list(heart(a_str,sub))

parity = {'p':'W','i':'A','u':'V','m':'0.001','k':'1000','M':'1000000'}

def search(line,index):
    for i in range(index,len(line)):
        if line[i].isalpha():
            return [i,line[i]]
    return [len(line)-1,'x']

def process(line,index):
    temp = search(line,index)
    prefix = line[index+1:temp[0]]
    if temp[1] in 'mkM':
        prefix = str(float(prefix)*float(parity[temp[1]]))
    return [line[index-1].lower(),prefix]

def solve(i):
    line = str(input())
    indexs = find_all(line,'=')
    p_data1 = process(line,indexs[0])
    p_data2 = process(line,indexs[1])
    print('Problem #' + str(i+1))
    pareja = [p_data1[0],p_data2[0]]
    pareja.sort()
    datos = dict([(p_data1[0],p_data1[1]),(p_data2[0],p_data2[1])])
    if pareja == ['i','p']:
        print("U={:.2f}".format(float(datos['p'])/float(datos['i']))+parity['u']+'\n')
    elif pareja == ['p','u']:
        print("I={:.2f}".format(float(datos['p'])/float(datos['u']))+parity['i']+'\n')
    elif pareja == ['i','u']:
        print("P={:.2f}".format(float(datos['u'])*float(datos['i']))+parity['p']+'\n')

def main():
    t = int(input())
    for i in range(0,t):
        solve(i)
        t-=1

main()