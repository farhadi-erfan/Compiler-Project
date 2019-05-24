import traceback
# from LexicalAnalysis import get_next_token
from FSMs import *
from first_follows import *

i = -1
line_num = '0'


def get_next_token():
    global i
    i += 1
    return 'int id ; EOF'.split()[i]


class FSM:

    def __init__(self, fsm_map):
        self.current_state = 0
        self.current_char = ''
        self.fsm_map = fsm_map
        self.in_error_handling = False

    def run(self, token=None):
        while True:
            token = get_next_token() if token is None else token
            if self.in_error_handling and token == 'EOF':
                print('#{} : Syntax Error! Unexpected EndOfFile'.format(line_num))
                return 'END'
            status, nxt = self.process_next(token)
            if not status:
                return nxt[0], nxt[1], token
            elif nxt == 'Finish':
                return True
            else:
                token = None

    def process_next(self, token):
        self.current_char = token
        frozen_state = self.current_state
        for transition in self.fsm_map:
            if transition['src'] == frozen_state:
                condition = transition.get('condition', None)
                if condition and transition['condition'] == token:
                    #terminal
                    self.in_error_handling = False
                    terminal(token)
                    if transition['Finish']:
                        return True, 'Finish'
                    else:
                        self.update_state(transition['dst'])
                        return True, 'Cont'
                if condition == '':
                    #eps
                    if token in follows[self.fsm_map[0]['name']]:
                        self.update_state(transition['dst'])
                        self.in_error_handling = False
                        return True, 'Finish'
                if not condition:
                    #non terminal
                    non_terminal_name = transition['callback']
                    if token in firsts[non_terminal_name] or (
                            non_terminal_name in nullables and token in follows[non_terminal_name]):
                        self.in_error_handling = False
                        return False, (transition['callback'], transition['dst'])
        # error handling
        self.in_error_handling = True
        outs = self.state_transition(frozen_state)
        if len(outs) == 1:
            out = outs[0]
            condition = out.get('condition', None)
            if condition is not None and condition == 'EOF':
                # eof
                print('#{} : Syntax Error! Malformed Input'.format(line_num))
                return 'END'
            if condition is not None and condition != token and condition != '':
                # terminal
                print('#{} : Syntax Error! Missing {}'.format(line_num, token))
                return True, 'Cont'
            if condition is None:
                # non terminal
                non_terminal_name = out['callback']
                print('#{} : Syntax Error! Unexpected {}'.format(line_num, token))
                token = get_next_token()
                while token not in firsts[non_terminal_name] and token not in follows[non_terminal_name]:
                    token = get_next_token()
                if 'eps' in firsts[non_terminal_name]:
                    return self.process_next(token)
                else:
                    if token in follows[non_terminal_name]:
                        print('#{} : Syntax Error! Missing {}'.format(line_num, non_terminal_name))
                        self.update_state(out['dst'])
                        return True, 'Cont'
        return False, None

    def update_state(self, new_state):
        print("{} -> {} : {}".format(self.current_char,
                                     self.current_state,
                                     new_state))
        self.current_state = new_state

    def state_transition(self, state):
        transitions = []
        for tr in self.fsm_map:
            if tr['src'] == state:
                transitions.append(tr)
        return transitions


class Node:
    def __init__(self, parent, sub_diagram, parent_next_state, type):
        self.parent = parent
        self.level = 0 if parent is None else parent.level + 1
        self.sub_diagram = sub_diagram
        self.parent_next_state = parent_next_state
        self.type = type
        self.children = []
        if type == 'Term':
            self.name = sub_diagram
        elif type == 'NonTerm':
            self.name = sub_diagram.fsm_map[0]['name']

    def __repr__(self):
        return 'name: ' + self.name + ' level: ' + self.level + ' parent_next_state: '\
               + self.parent_next_state + ' type: ' + self.type


def terminal(term):
    curr.children += [Node(curr, term, None, 'Term')]


def is_it_the_end():
    l = []
    for x in curr.sub_diagram.fsm_map:
        if x:
            if 'Finish' in x.keys():
                l += [x['dst']]
    return curr.sub_diagram.current_state in l


def non_terminal_end():
    global curr
    if curr.parent is not None:
        next = curr.parent_next_state
        curr = curr.parent
        curr.sub_diagram.current_state = next
        if is_it_the_end():
            return non_terminal_end()
        return curr.sub_diagram.run()
    else:
        print_nodes(head)
        return 'END'


def non_terminal_init(non_terminal_name, next_state, token):
    global curr
    curr.children += [Node(curr, FSM(globals()[non_terminal_name]), next_state, 'NonTerm')]
    curr = curr.children[-1]
    return curr.sub_diagram.run(token)


def print_nodes(node):
    # print(node)
    print('|\t'*node.level + node.name)
    for x in node.children:
        print_nodes(x)


PROGRAM_sub_diagram = FSM(PROGRAM)
# DL_sub_diagram = FSM(DL)
# DL1_sub_diagram = FSM(DL1)
# Dec_sub_diagram = FSM(Dec)
# FTS2_sub_diagram = FSM(FTS2)
# VarDec_sub_diagram = FSM(VarDec)
# FTS_sub_diagram = FSM(FTS)
# FID1_sub_diagram = FSM(FID1)
# TS_sub_diagram = FSM(TS)
# FDec_sub_diagram = FSM(FDec)
# Params_sub_diagram = FSM(Params)
# FVoid_sub_diagram = FSM(FVoid)
# PL_sub_diagram = FSM(PL)
# PL1_sub_diagram = FSM(PL1)
# Param_sub_diagram = FSM(Param)
# FTS1_sub_diagram = FSM(FTS1)
# FID2_sub_diagram = FSM(FID2)
# CompStmt_sub_diagram = FSM(CompStmt)
# SL_sub_diagram = FSM(SL)
# SL1_sub_diagram = FSM(SL1)
# Stmt_sub_diagram = FSM(Stmt)
# ExpStmt_sub_diagram = FSM(ExpStmt)
# SelStmt_sub_diagram = FSM(SelStmt)
# IterStmt_sub_diagram = FSM(IterStmt)
# ID_sub_diagram = FSM(ID)
try:
    head = Node(None, PROGRAM_sub_diagram, None, 'NonTerm')
    curr = head
    result = curr.sub_diagram.run()
    while True:
        while result is True:
            result = non_terminal_end()
            if result == 'END':
                exit()
        non_terminal_name, next_state, token = result[0], result[1], result[2]
        result = non_terminal_init(non_terminal_name, next_state, token)
except Exception as e:
    print_nodes(head)
    print(e)