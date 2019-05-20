from LexicalAnalysis import get_next_token


class FSM:

    def __init__(self, fsm_map):
        self.current_state = 0
        self.current_char = ''
        self.fsm_map = fsm_map

    def run(self, token=None):
        while True:
            token = get_next_token() if token is None else token
            status, nxt = self.process_next(token)
            if not status:
                return nxt[0], nxt[1], token
            elif nxt == 'Finish':
                return True
            else:
                token = None

    def process_next(self, achar):
        self.current_char = achar
        frozen_state = self.current_state
        for transition in self.fsm_map:
            if transition['src'] == frozen_state:
                condition = transition.get('condition', None)
                if condition and transition['condition'] == achar:
                    terminal(achar)
                    if transition['finish']:
                        return True, 'Finish'
                    else:
                        self.update_state(transition['dst'])
                        return True, 'Cont'
                if not condition:
                    return False, (transition['callback'], transition['dst'])
        return False

    def update_state(self, new_state):
        print("{} -> {} : {}".format(self.current_char,
                                     self.current_state,
                                     new_state))
        self.current_state = new_state


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
        return 'name: ' + self.sub_diagram + ' level: ' + self.level + ' parent_next_state: '\
               + self.parent_next_state + ' type: ' + self.type


def terminal(term):
    curr.children += [Node(curr, term, None, 'Term')]


def non_terminal_end():
    global curr
    if curr.parent is not None:
        next = curr.parent_next_state
        curr = curr.parent
        curr.sub_diagram.current_state = next
        return curr.sub_diagram.run()
    else:
        print_nodes(head)
        return 'END'


def non_terminal_init(non_terminal_name, next_state, token):
    global curr
    curr.children += [Node(curr, globals()[non_terminal_name + '_sub_diagram'], next_state, 'NonTerm')]
    curr = curr.children[-1]
    return curr.sub_diagram.run(token)


def print_nodes(node):
    # print(node)
    print('|\t'*node.level + node.name)
    for x in node.children:
        print_nodes(x)


#  {'src':, 'dst':, 'condition':, 'callback': }
PROGRAM = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'DL', 'name': 'Program'},
           {'src': 1, 'dst': 2, 'condition': 'EOF', 'callback': None, 'finish': True})
DL = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'DL1', 'finish': True, 'name': 'DL'}, None)
DL1 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Dec', 'name': 'DL1'},
       {'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'finish': True},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'DL1', 'finish': True})
Dec = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'TS', 'name': 'Dec'},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FTS2', 'finish': True})
FTS2 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'FTS', 'finish': True, 'name': 'FTS2'},
        {'src': 0, 'dst': 2, 'condition': None, 'callback': 'ID'},
        {'src': 2, 'dst': 3, 'condition': '(', 'callback': None},
        {'src': 3, 'dst': 4, 'condition': None, 'callback': 'Params'},
        {'src': 4, 'dst': 5, 'condition': ')', 'callback': None},
        {'src': 5, 'dst': 6, 'condition': None, 'callback': 'CompStmt', 'finish': True})
VarDec = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'TS', 'name': 'VarDec'},
          {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FTS', 'finish': True})
FTS = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'ID', 'name': 'FTS'},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FID1', 'finish': True})
FID1 = ({'src': 0, 'dst': 1, 'condition': ';', 'callback': None, 'finish': True, 'name': 'FID1'},
        {'src': 0, 'dst': 2, 'condition': '[', 'callback': None},
        {'src': 2, 'dst': 3, 'condition': None, 'callback': 'NUM'},
        {'src': 3, 'dst': 4, 'condition': ']', 'callback': None},
        {'src': 4, 'dst': 5, 'condition': ';', 'callback': None, 'finish': True})
TS = ({'src': 0, 'dst': 1, 'condition': 'int', 'callback': None, 'name': 'TS', 'finish': True},
      {'src': 0, 'dst': 2, 'condition': 'void', 'callback': None, 'finish': True})
FDec = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'TS', 'name': 'FDec'},
        {'src': 1, 'dst': 2, 'condition': None, 'callback': 'ID'},
        {'src': 2, 'dst': 3, 'condition': '(', 'callback': None},
        {'src': 3, 'dst': 4, 'condition': None, 'callback': 'Params'},
        {'src': 4, 'dst': 5, 'condition': ')', 'callback': None},
        {'src': 5, 'dst': 5, 'condition': None, 'callback': 'CompStmt', 'finish': True})
Params = ({'src': 0, 'dst': 1, 'condition': 'void', 'callback': None, 'name': 'Params'},
          {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FVoid', 'finish': True},
          {'src': 0, 'dst': 3, 'condition': 'int', 'callback': None},
          {'src': 3, 'dst': 4, 'condition': None, 'callback': 'FTS1'},
          {'src': 4, 'dst': 5, 'condition': None, 'callback': 'PL1', 'finish': True})
FVoid = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'FTS1', 'name': 'FVoid'},
         {'src': 1, 'dst': 2, 'condition': None, 'callback': 'PL1', 'finish': True},
         {'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'finish': True})
PL = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Param', 'name': 'Param'},
      {'src': 1, 'dst': 2, 'condition': None, 'callback': 'PL1', 'finish': True})
PL1 = ({'src': 0, 'dst': 1, 'condition': ',', 'callback': None, 'name': 'PL1'},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Param'},
       {'src': 2, 'dst': 3, 'condition': None, 'callback': 'PL1', 'finish': True},
       {'src': 0, 'dst': 3, 'condition': '', 'callback': None, 'finish': True})
Param = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'TS', 'name': 'Param'},
         {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FTS1', 'finish': True})
FTS1 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'ID', 'name': 'FTS1'},
        {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FID2', 'finish': True})
FID2 = ({'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'name': 'FID2', 'finish': True},
        {'src': 0, 'dst': 1, 'condition': '[', 'callback': None},
        {'src': 1, 'dst': 2, 'condition': ']', 'callback': None, 'finish': True})
CompStmt = ({'src': 0, 'dst': 1, 'condition': '{', 'callback': None, 'name': 'CompStmt'},
            {'src': 1, 'dst': 2, 'condition': None, 'callback': 'DL'},
            {'src': 2, 'dst': 3, 'condition': None, 'callback': 'SL'},
            {'src': 3, 'dst': 4, 'condition': '}', 'callback': None, 'finish': True})
SL = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'SL1', 'name': 'SL', 'finish': True}, None)
SL1 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Stmt', 'name': 'SL1'},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'SL1', 'finish': True},
       {'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'finish': True})
Stmt = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'ExpStmt', 'finish': True, 'name': 'Stmt'},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'CompStmt', 'finish': True},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'SelStmt', 'finish': True},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'IterStmt', 'finish': True},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'RetStmt', 'finish': True},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'SwitchStmt', 'finish': True})
ExpStmt = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Exp', 'name': 'ExpStmt'},
           {'src': 1, 'dst': 2, 'condition': ';', 'callback': None, 'finish': True},
           {'src': 0, 'dst': 3, 'condition': 'continue', 'callback': 'SL'},
           {'src': 3, 'dst': 2, 'condition': ';', 'callback': None, 'finish': True},
           {'src': 0, 'dst': 4, 'condition': 'break', 'callback': 'SL'},
           {'src': 4, 'dst': 2, 'condition': ';', 'callback': None, 'finish': True},
           {'src': 0, 'dst': 2, 'condition': ';', 'callback': None, 'finish': True})


PROGRAM_sub_diagram = FSM(PROGRAM)
DL_sub_diagram = FSM(DL)
head = Node(None, PROGRAM_sub_diagram, None, 'NonTerm')
curr = head
result = curr.sub_diagram.run()
while True:
    while result is True:
        result = non_terminal_end()
        if result == 'END':
            exit()
    result = non_terminal_init(result[0], result[1], result[2])