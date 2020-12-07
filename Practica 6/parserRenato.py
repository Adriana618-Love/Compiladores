from afilesmgmt import File

DOLAR = '$'


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
                                if 'lambda' in temp:
                                    temp.remove('lambda')
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
                    if i[0] != 'lambda':
                        if i[0] in self.terminals:
                            self.tas[p.get_left()][i[0]] = i
                        else:
                            prim_temp = self.get_first(i[0])
                            for term in prim_temp:
                                if term != 'lambda':
                                    self.tas[p.get_left()][term] = i
                    else:
                        for f in self.nexts[p.get_left()]:
                            self.tas[p.get_left()][f] = i
        return self.tas

    def print_tas(self):
        for fst_key, sub_dict in self.tas.items():
            for snd_key, production in sub_dict.items():
                print(fst_key, snd_key, production)


class TAS:
    def __init__(self):
        self.syn_table = dict({'': {}})

    def build(self):
        self.syn_table['E'] = {}
        self.syn_table['E']['('] = ["T", "Ep"]
        self.syn_table['E']['num'] = ["T", "Ep"]
        self.syn_table['Ep'] = {}
        self.syn_table['Ep']['id'] = ["T", "Ep"]
        self.syn_table['Ep']['+'] = ["+", "T", "Ep"]
        self.syn_table['Ep']['-'] = ["-", "T", "Ep"]
        self.syn_table['Ep'][')'] = ["lambda"]
        self.syn_table['Ep']['$'] = ["lambda"]
        self.syn_table['T'] = {}
        self.syn_table['T']['('] = ["F", "Tp"]
        self.syn_table['T']['num'] = ["F", "Tp"]
        self.syn_table['T']['id'] = ["F", "Tp"]
        self.syn_table['Tp'] = {}
        self.syn_table['Tp']['+'] = ["lambda"]
        self.syn_table['Tp']['-'] = ["lambda"]
        self.syn_table['Tp']['*'] = ["*", "F", "Tp"]
        self.syn_table['Tp']['/'] = ["/", "F", "Tp"]
        self.syn_table['Tp'][')'] = ["lambda"]
        self.syn_table['Tp']['$'] = ["lambda"]
        self.syn_table['F'] = {}
        self.syn_table['F']['('] = ["(", "E", ")"]
        self.syn_table['F']['num'] = ["num"]
        self.syn_table['F']['id'] = ["id"]


class Parser:
    terminal = {}
    table = {}
    epsilon = 'lambda'
    error_message = 'There was a problem, failed'

    def __init__(self, terminals, table):
        for term in terminals:
            self.terminal[term] = True
        self.table = table

    def _parse(self, non_terminal, idx, tokens, answer):
        answer += '{}: ['.format(non_terminal)
        dict = self.table.get(non_terminal, None)
        if dict is None:
            return -1, answer
        prod = dict.get(tokens[idx], None)
        if prod is None:
            return -1, answer
        for term in prod:
            if term == self.epsilon:
                answer += '{}, '.format(term)
                continue
            is_terminal = self.terminal.get(term, False)
            if not is_terminal:
                idx, answer = self._parse(term, idx, tokens, answer)
                if idx == -1:
                    return -1, answer
            else:
                if tokens[idx] == term:
                    idx += 1
                    answer += '{}, '.format(term)
                else:
                    return -1, answer
        answer += '] '
        return idx, answer

    def parse(self, tokens):
        answer = ''
        size, answer = self._parse('S', 0, tokens, answer)
        if size != len(tokens):
            answer = self.error_message
        return answer


def print_dict(dicti):
    [print(key, value) for key, value in dicti.items()]


my_file = File('sos.txt')
my_grammar = Grammar()
my_grammar.set_init('goal')
my_grammar.load(my_file, '@')
print(print_dict(my_grammar.get_firsts()))
print("-------------")
print(print_dict(my_grammar.get_nexts()))
print("-------------")
my_grammar.create_table()
my_grammar.print_tas()
print(my_grammar.terminals)
print(my_grammar.non_terminals)

parser = Parser(my_grammar.terminals, my_grammar.tas)
print(parser.parse(['name', '+', 'name', ')' '$']))
