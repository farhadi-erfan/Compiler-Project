import LL1Parser
from LL1Parser import *
from LexicalAnalysis import *


def report():
    global la
    with open('errors.txt', 'w+') as errors_file:
        for i in la.errors.keys():
            errors_file.write('{}. '.format(i))
            for v in la.errors[i]:
                errors_file.write('{}'.format(v))
            errors_file.write('\n')
        for i in LL1Parser.parse_errors:
            errors_file.write(i)

    with open('scanner.txt', 'w+') as tokens_file:
        for i in la.tokens.keys():
            tokens_file.write('{}. '.format(i))
            for v in la.tokens[i]:
                tokens_file.write('{}'.format(v))
            tokens_file.write('\n')

    with open('parse_tree.txt', 'w+') as parse_tree_file:
        print(LL1Parser.parse_tree)
        LL1Parser.parse_tree = ''
        print_nodes(head)
        parse_tree_file.write(LL1Parser.parse_tree)


def get_next_token():
    token = la.get_next_token_lexical()
    if token[0].endswith('ERROR'):
        if la.line_num in la.errors.keys():
            la.errors[la.line_num] += ' (' + token[1] + ', invalid input)'
        else:
            la.errors[la.line_num] = '(' + token[1] + ', invalid input)'
        return get_next_token()
    else:
        if token[0] == 'WHITESPACE' or token[0] == 'COMMENT':
            return get_next_token()
        if la.line_num in la.tokens.keys():
            la.tokens[la.line_num] += ' (' + token[0] + ', ' + token[1] + ')'
        else:
            la.tokens[la.line_num] = '(' + token[0] + ', ' + token[1] + ')'
    if token[0] == 'KEYWORD' or token[0] == 'SYMBOL' or token[0] == 'EOF':
        return token[1], la.line_num
    elif token[0] == 'ID':
        return 'id', la.line_num, token[1]
    elif token[0] == 'NUM':
        return 'num', la.line_num, token[1]

linum = 1
LL1Parser.linum = linum
LL1Parser.get_next_token = get_next_token

la = LexicalAnalyzer()

PROGRAM_sub_diagram = FSM(PROGRAM)
head = Node(None, PROGRAM_sub_diagram, None, 'NonTerm')
LL1Parser.head = head
curr = head
LL1Parser.curr = curr
result = curr.sub_diagram.run()
LL1Parser.result = result
while True:
    while result is True or result[0] is True:
        if type(result) is tuple:
            result = non_terminal_end(result[1])
        else:
            result = non_terminal_end()
        if result == 'END':
            print_nodes(head)
            report()
            break
    if result == 'END':
        print_nodes(head)
        report()
        break
    non_terminal_name, next_state, token = result[0], result[1], result[2]
    result = non_terminal_init(non_terminal_name, next_state, token)
