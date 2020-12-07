#(c) Alonso Valdivia Quispe - alonso.valdivia.quispe@ucsp.edu.pe
special_word = {'decir':'diciendo','pedir':'pidiendo','sentir':'sintiendo','repetir':'repitiendo','seguir':'siguiendo','sugerir':'sugiriendo','vestir':'vistiendo','venir':'viniendo','freir':'friendo','reir':'riendo','dormir':'durmiendo','morir':'muriendo'}

def standarize(string):
    return string.lower()

def rreplace(string,old_value,new_value,count=1):
    return string[::-1].replace(old_value[::-1],new_value[::-1],count)[::-1]

def replace_str_index(text,replacement='',indexi=0,indexf=0):
    if not indexf:
        indexf=len(text)
    return '%s%s%s'%(text[:indexi],replacement,text[indexf+1:])

def find_all(a_str, sub):

    def heart(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches
    return list(heart(a_str,sub))

def isVowel(char):
    return char.lower() in 'aeiou'