
import os
from os import path

DOLAR = '$'
EPSILON = 'lambda'


class File:
    file = None

    def __init__(self, name_file, path_file=''):
        self.name_file = name_file
        self.path_file = os.path.join((str(os.getcwd()),path_file)[len(path_file)], self.name_file)
        print("From file:", self.path_file)
        self.init_file()

    def init_file(self):
        if not path.exists(self.path_file):
            self.file = open(self.path_file, 'x')
            self.file.close()

    def append_line(self, line):
        self.file = open(self.name_file, 'a')
        self.file.write(line)
        self.file.close()

    def get_all_lines(self):
        self.file = open(self.name_file, 'r')
        lines = self.file.readlines()
        self.file.close()
        return lines


class Production:
    def __init__(self):
        self.left = []
        self.right = []

    def print(self):
        for i in self.right:
            print(self.left + " -> " + ' '.join(i))

    def get_left(self):
        return self.left.strip()

    def get_production(self):
        return self.right

    def add_right(self, new):
        for elem in new:
            self.right.append(elem)


class Grammar:
    tas = dict({'': {}})
    firsts = {}
    nexts = {}
    initial_node = 'goal'
    production = []
    terminals = []
    non_terminals = []

    def set_init(self, initial):
        self.initial_node = initial

    def get_index(self, left):
        i = 0
        for nt in self.non_terminals:
            if nt == left:
                return i
            i += 1
        return -1

    def load(self, file, separator_union='|', separator='::='):
        lines = file.get_all_lines()
        simbols = []
        for line in lines:
            pdc = line.split(separator)
            if len(pdc) == 1:
                continue
            my_left = pdc[0]
            my_right = pdc[1]
            expand = my_right.split(separator_union)
            expand = self.treat(expand)

            if not (my_left.strip() in self.non_terminals):
                self.non_terminals.append(my_left.strip())
                new_production = Production()
                new_production.left = my_left
                new_production.right = expand
                self.production.append(new_production)
            else:
                idx = self.get_index(my_left.strip())
                self.production[idx].add_right(expand)

            for rights in expand:
                for sim in rights:
                    if not (sim in simbols):
                        simbols.append(sim)
        self.fill_t(simbols)

    def fill_t(self, simbols):
        for ter in simbols:
            if not(ter in self.non_terminals):
                self.terminals.append(ter)

    def print(self):
        for p in self.production:
            p.print()

    def get_production(self, left):
        return self.production[self.get_index(left)].get_production()

    def treat(self, my_right):
        production = []
        for right in my_right:
            right = right.strip()
            production.append(right.split(' '))
        return production

    def join(self, ps, pc):
        for p in ps:
            pc.append(p)
        return pc

    def concatenate(self, pc, rs):
        for ele in rs:
            pc.append(ele)

    def get_first(self, prim):
        productions = self.get_production(prim)
        firsts_simple = []
        firsts_complex = []
        for prod in productions:
            if prod[0] in self.non_terminals:
                self.concatenate(firsts_complex, self.get_first(prod[0]))
            else:
                firsts_simple.append(prod[0])
        firsts = self.join(firsts_simple, firsts_complex)
        return firsts

    def get_productions(self):
        return self.production

    def get_firsts(self):
        self.firsts = {}
        for nodo in self.non_terminals:
            self.firsts[nodo] = self.get_first(nodo)
        return self.firsts

    def get_non_terminal(self, miniprod, i):
        for idx in range(i, len(miniprod)):
            if miniprod[idx] in self.non_terminals:
                return idx
        return -1

    def add(self, obt, tmp):
        for i in tmp:
            if not (i in obt):
                obt.append(i)

    def get_next(self, nt, sgts):
        productions = self.production
        for prod in productions:
            for right in prod.right:
                for idx in range(0, len(right)):
                    if nt == right[idx]:
                        if idx == len(right)-1:
                            self.add(sgts[right[idx]], sgts[prod.get_left()])
                        else:
                            if right[idx+1] in self.terminals:
                                if not(right[idx+1] in sgts[right[idx]]):
                                    sgts[right[idx]].append(right[idx+1])
                            else:
                                temp = self.get_first(right[idx+1])
                                if EPSILON in temp:
                                    temp.remove(EPSILON)
                                    self.add(temp, sgts[prod.get_left()])
                                self.add(sgts[right[idx]], temp)

    def get_nexts(self):
        self.nexts = {}
        for i in self.non_terminals:
            self.nexts[i] = []
        self.nexts[self.initial_node].append(DOLAR)
        for nt in self.non_terminals:
            self.get_next(nt, self.nexts)
        return self.nexts

    def create_table(self):
        self.tas = dict({'': {}})
        for p in self.production:
            self.tas[p.get_left()] = {}
            if len(p.get_production()) == 1:
                for i in self.firsts[p.get_left()]:
                    self.tas[p.get_left()][i] = p.get_production()[0]
            else:
                for i in p.get_production():
                    if i[0] != EPSILON:
                        if i[0] in self.terminals:
                            self.tas[p.get_left()][i[0]] = i
                        else:
                            prim_temp = self.get_first(i[0])
                            for term in prim_temp:
                                if term != EPSILON:
                                    self.tas[p.get_left()][term] = i
                    else:
                        for f in self.nexts[p.get_left()]:
                            self.tas[p.get_left()][f] = i
        return self.tas

    def print_tas(self):
        for fst_key, sub_dict in self.tas.items():
            for snd_key, production in sub_dict.items():
                print(fst_key, snd_key, production)


class Token:
    type = None

    def __init__(self, string=None):
        string = string.strip()
        self.type = string

    def __str__(self):
        return '<{}>'.format(self.type)

    def __repr__(self):
        return str(self)

    @classmethod
    def get_tokens(cls, exp):
        return [cls(term) for term in ' '.join(exp.strip().split()).split()] + [cls('$')]

class Node:
    def __init__(self,value,hijos):
        self.value = value
        self.childrens = {}
        for i in range(0, len(hijos)):
            self.childrens[hijos[i]] = Node(hijos[i],[])
    def __getitem__(self,child):
        return self.childrens[child]
    def setitem(self, hijos):
        for i in range(0, len(hijos)):
            self.childrens[hijos[i]] = Node(hijos[i],[])
    def __repr__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.childrens:
            ret += self.childrens[child].__repr__(level+1)
        return ret

def write(stack,input,izq,der):
    
    print("s",' '.join(stack))
    print("in",' '.join([str(x) for x in input]))
    print("izq",izq)
    print("der",' '.join(der))
    line =  ' '.join(stack) + "\t"*4 + ' '.join([str(x) for x in input]) + "\t"*4 + izq + " -> " + ' '.join(der) +'\n'
    f = open("ouput.txt", "a")
    f.write(line)
    f.close()

class Validator:
    terminal = {}
    table = {}
    epsilon = EPSILON
    error_message = 'There was a problem, failed'
    initial_state = 'E'

    def __init__(self, terminals, table, initial_state):
        for term in terminals:
            self.terminal[term] = True
        self.table = table
        self.initial_state = initial_state

    def _join(self,lista,prod):
        temp = prod.copy()
        temp.reverse()
        lista.extend(temp)

    def _validate(self, non_terminal, idx, tokens, lista,node,nivel):
        dict = self.table.get(non_terminal, None)
        if dict is None:
            return -1
        prod = dict.get(tokens[idx].type, None)
        ##
        lista.pop()
        if prod is None:
            return -1
        self._join(lista,prod)
        ######Sección que escribe las operaciones
        izq = non_terminal
        der = prod
        _input = tokens[idx:]
        stack = lista.copy()
        write(stack,_input,izq,der)
        #########################################
        node.setitem(prod)
        for term in prod:
            if term == '':
                lista.pop()
                continue
            if term == self.epsilon:
                lista.pop()
                continue
            is_terminal = self.terminal.get(term, False)
            if not is_terminal:
                idx = self._validate(term, idx, tokens,lista,node.childrens[term],nivel+1)
                if idx == -1:
                    return -1
            else:
                if tokens[idx].type == term:
                    idx += 1
                else:
                    return -1
                lista.pop()
                write(lista.copy(),_input,"",[term])
        return idx

    def validate(self, tokens):
        arbol = Node(self.initial_state,[])
        lista = [self.initial_state]
        size = self._validate(self.initial_state, 0, tokens, lista,arbol,0)
        print("Arbol")
        print(arbol)
        return size == len(tokens)


if __name__ == '__main__':
    file = File('test.txt')
    grammar = Grammar()
    grammar.set_init('E')
    grammar.load(file, '@',':=')
    grammar.get_firsts()
    grammar.get_nexts()
    grammar.create_table()


    validator = Validator(grammar.terminals, grammar.tas, 'E')

    tests = [
        ('id + id', True),
    ]

    TEST = 0
    ANSWER = 1
    errors = 0

    for idx, test in enumerate(tests):
        tokens = Token.get_tokens(test[TEST])
        print(tokens)
        if validator.validate(tokens) != test[ANSWER]:
            errors += 1
            print('There is an error in test {}, Expression "{}"'.format(idx + 1, test[TEST]))

    print('Tests completed with {} {}'.format(errors, 'error' if errors == 1 else 'errors'))
