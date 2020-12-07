
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

"""
if __name__ == '__main__':
    terminals = ['$', '+', '*', '(', ')', 'id']
    table = {
        'S': {
            '$': [], '+': [], '*': [], '(': ['E', '$'], ')': [], 'id': ['E', '$']
        },
        'E': {
            '$': [], '+': [], '*': [], '(': ['T', 'Ep'], ')': [], 'id': ['T', 'Ep']
        },
        'Ep': {
            '$': [Parser.epsilon], '+': ['+', 'T', 'Ep'], '*': [], '(': [], ')': [Parser.epsilon], 'id': []
        },
        'T': {
            '$': [], '+': [], '*': [], '(': ['F', 'Tp'], ')': [], 'id': ['F', 'Tp']
        },
        'Tp': {
            '$': [Parser.epsilon], '+': [Parser.epsilon], '*': ['*', 'F', 'Tp'], '(': [], ')': [Parser.epsilon], 'id': []
        },
        'F': {
            '$': [], '+': [], '*': [], '(': ['(', 'E', ')'], ')': [], 'id': ['id']
        },
    }
    parser = Parser(terminals, table)
    print(parser.parse(['(', 'id', '+', 'id', ')', '+', 'id', '$']))
"""