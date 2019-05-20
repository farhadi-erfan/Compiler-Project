# from LexicalAnalysis import get_next_token

i = -1


def get_next_token():
    global i
    i += 1
    return 'int id ; EOF'.split()[i]


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
                    if transition['Finish']:
                        return True, 'Finish'
                    else:
                        self.update_state(transition['dst'])
                        return True, 'Cont'
                if not condition:
                    return False, (transition['callback'], transition['dst'])
        return False, None

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
        return 'name: ' + self.name + ' level: ' + self.level + ' parent_next_state: '\
               + self.parent_next_state + ' type: ' + self.type


def terminal(term):
    curr.children += [Node(curr, term, None, 'Term')]

def is_it_the_end():
    l = []
    for x in curr.sub_diagram.fsm_map:
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
           {'src': 0, 'dst': 3, 'condition': 'continue', 'callback': None},
           {'src': 3, 'dst': 2, 'condition': ';', 'callback': None, 'finish': True},
           {'src': 0, 'dst': 4, 'condition': 'break', 'callback': 'SL'},
           {'src': 4, 'dst': 2, 'condition': ';', 'callback': None, 'finish': True},
           {'src': 0, 'dst': 2, 'condition': ';', 'callback': None, 'finish': True})

SelStmt = ({'src': 0, 'dst': 1, 'condition': 'if', 'callback': None, 'name': 'SelStmt'},
           {'src': 1, 'dst': 2, 'condition': '(', 'callback': None},
           {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Exp'},
           {'src': 3, 'dst': 4, 'condition': ')', 'callback': None},
           {'src': 4, 'dst': 5, 'condition': None, 'callback': 'Stmt'},
           {'src': 5, 'dst': 6, 'condition': 'else', 'callback': None},
           {'src': 6, 'dst': 7, 'condition': None, 'callback': 'Stmt', 'finish': True})

IterStmt = ({'src': 0, 'dst': 1, 'condition': 'while', 'callback': None, 'name': 'IterStmt'},
            {'src': 1, 'dst': 2, 'condition': '(', 'callback': None},
            {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Expr'},
            {'src': 3, 'dst': 4, 'condition': ')', 'callback': None},
            {'src': 4, 'dst': 5, 'condition': None, 'callback': 'Stmt', 'finish': True})

RetStmt = ({'src': 0, 'dst': 1, 'condition': 'return', 'callback': None, 'name': 'RetStmt'},
           {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Fret', 'finish': True})

Fret = ({'src': 0, 'dst': 2, 'condition': ';', 'callback': None, 'name': 'Fret', 'finish': True},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'Expr'},
        {'src': 1, 'dst': 2, 'condition': ';', 'callback': 'None', 'finish': True})

SwitchStmt = ({'src': 0, 'dst': 1, 'condition': 'switch', 'callback': None, 'name': 'SwitchStmt'},
              {'src': 1, 'dst': 2, 'condition': '(', 'callback': None},
              {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Expr'},
              {'src': 3, 'dst': 4, 'condition': ')', 'callback': None},
              {'src': 4, 'dst': 5, 'condition': '{', 'callback': None},
              {'src': 5, 'dst': 6, 'condition': None, 'callback': 'CaseStmts'},
              {'src': 6, 'dst': 7, 'condition': None, 'callback': 'DefaultStmt'},
              {'src': 7, 'dst': 8, 'condition': '}', 'callback': None, 'finish': True})

CaseStmts = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'CaseStmts_1', 'name': 'CaseStmts',
              'finish': True})

CaseStmts_1 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'CaseStmt', 'name': 'CaseStmts_1'},
               {'src': 1, 'dst': 2, 'condition': None, 'callback': 'CaseStmts_1', 'finish': True},
               {'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'finish': True})

CaseStmt = ({'src': 0, 'dst': 1, 'condition': 'case', 'callback': None, 'name': 'CaseStmt'},
            {'src': 1, 'dst': 2, 'condition': None, 'callback': 'NUM'},
            {'src': 2, 'dst': 3, 'condition': ':', 'callback': None},
            {'src': 3, 'dst': 4, 'condition': 'StatementList', 'callback': None, 'finish': True})

DefaultStmt = ({'src': 0, 'dst': 1, 'condition': 'default', 'callback': None, 'name': 'DefaultStmt'},
               {'src': 1, 'dst': 2, 'condition': ':', 'callback': None},
               {'src': 2, 'dst': 3, 'condition': None, 'callback': 'StatementList', 'finish': True},
               {'src': 0, 'dst': 3, 'condition': '', 'callback': None, 'finish': True})

Expr = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Var', 'name': 'Expr'},
        {'src': 1, 'dst': 2, 'condition': 'eq', 'callback': None},
        {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Expr', 'finish': True},
        {'src': 0, 'dst': 3, 'condition': None, 'callback': 'SimpleExpr', 'finish': True})

Var = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'ID', 'name': 'Var'},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FID', 'finish': True})

FID = ({'src': 0, 'dst': 1, 'condition': '[', 'callback': None, 'name': 'FID'},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Expr'},
       {'src': 2, 'dst': 3, 'condition': ']', 'callback': None, 'finish': True})

SimpleExpr = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'AdditiveExpr',
                     'name': 'SimpleExpr'},
                    {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FAdditiveExpr', 'finish': True})

FAdditiveExpr = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Relop', 'name': 'FAdditiveExpr'},
                       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'AdditiveExpr', 'finish': True},
                       {'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'finish': True})

Relop = ({'src': 0, 'dst': 1, 'condition': '<', 'callback': None, 'name': 'Relop', 'finish': True},
         {'src': 0, 'dst': 1, 'condition': '==', 'callback': None, 'finish': True})

AdditiveExpr = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Term', 'name': 'AdditiveExpr'},
                      {'src': 1, 'dst': 2, 'condition': None, 'callback': 'AdditiveExpr_1', 'finish': True})

AdditiveExpr_1 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Addop', 'name': 'AdditiveExpr'},
                  {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Term'},
                  {'src': 2, 'dst': 3, 'condition': None, 'callback': 'AdditiveExpr_1', 'finish': True},
                  {'src': 0, 'dst': 3, 'condition': '', 'callback': None, 'finish': True})

Addop = ({'src': 0, 'dst': 1, 'condition': '+', 'callback': None, 'name': 'Addop', 'finish': True},
         {'src': 0, 'dst': 1, 'condition': '-', 'callback': None, 'name': 'Addop', 'finish': True})

Term = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'SignedFactor', 'name': 'Term'},
        {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Term_1', 'finish': True})

Term_1 = ({'src': 0, 'dst': 1, 'condition': '*', 'callback': None, 'name': 'Term_1'},
          {'src': 1, 'dst': 2, 'condition': None, 'callback': 'SignedFactor'},
          {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Term_1', 'finish': True},
          {'src': 0, 'dst': 3, 'condition': '', 'callback': None, 'finish': True})

SignedFactor = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Factor', 'finish': True, 'name': 'SignedFactor'},
                {'src': 0, 'dst': 2, 'condition': '+', 'callback': None},
                {'src': 2, 'dst': 1, 'condition': None, 'callback': 'Factor', 'finish': True},
                {'src': 0, 'dst': 3, 'condition': '-', 'callback': None},
                {'src': 3, 'dst': 1, 'condition': None, 'callback': 'Factor', 'finish': True})

Factor = ({'src': 0, 'dst': 1, 'condition': '(', 'callback': None, 'name': 'Factor'},
          {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Expr'},
          {'src': 2, 'dst': 3, 'condition': ')', 'callback': None, 'finish': True},
          {'src': 0, 'dst': 3, 'condition': None, 'callback': 'Var', 'finish': True},
          {'src': 0, 'dst': 3, 'condition': None, 'callback': 'Call', 'finish': True},
          {'src': 0, 'dst': 3, 'condition': None, 'callback': 'Num', 'finish': True})

Call = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'ID', 'name': 'Call'},
        {'src': 1, 'dst': 2, 'condition': '(', 'callback': None},
        {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Args'},
        {'src': 3, 'dst': 4, 'condition': ')', 'callback': None, 'finish': True})

Args = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'ArgList', 'name': 'Args', 'finish': True},
        {'src': 0, 'dst': 1, 'condition': '', 'callback': None, 'finish': True})

ArgList = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Expr', 'name': 'ArgList'},
           {'src': 1, 'dst': 2, 'condition': None, 'callback': 'ArgList_1', 'finish': True})

ArgList_1 = ({'src': 0, 'dst': 1, 'condition': ',', 'callback': None, 'name': 'ArgList_1'},
             {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Expr'},
             {'src': 2, 'dst': 3, 'condition': None, 'callback': 'ArgList_1', 'finish': True},
             {'src': 2, 'dst': 3, 'condition': '', 'callback': None, 'finish': True})


ID = ({'src': 0, 'dst': 1, 'condition': 'id', 'callback': None, 'name': 'ID', 'finish': True})

Num = ({'src': 0, 'dst': 1, 'condition': 'num', 'callback': None, 'name': 'NUM', 'finish': True})


PROGRAM_sub_diagram = FSM(PROGRAM)
DL_sub_diagram = FSM(DL)
DL1_sub_diagram = FSM(DL1)
Dec_sub_diagram = FSM(Dec)
FTS2_sub_diagram = FSM(FTS2)
VarDec_sub_diagram = FSM(VarDec)
FTS_sub_diagram = FSM(FTS)
FID1_sub_diagram = FSM(FID1)
TS_sub_diagram = FSM(TS)
FDec_sub_diagram = FSM(FDec)
Params_sub_diagram = FSM(Params)
FVoid_sub_diagram = FSM(FVoid)
PL_sub_diagram = FSM(PL)
PL1_sub_diagram = FSM(PL1)
Param_sub_diagram = FSM(Param)
FTS1_sub_diagram = FSM(FTS1)
FID2_sub_diagram = FSM(FID2)
CompStmt_sub_diagram = FSM(CompStmt)
SL_sub_diagram = FSM(SL)
SL1_sub_diagram = FSM(SL1)
Stmt_sub_diagram = FSM(Stmt)
ExpStmt_sub_diagram = FSM(ExpStmt)
SelStmt_sub_diagram = FSM(SelStmt)
IterStmt_sub_diagram = FSM(IterStmt)
ID_sub_diagram = FSM(ID)
try:
    head = Node(None, PROGRAM_sub_diagram, None, 'NonTerm')
    curr = head
    result = curr.sub_diagram.run()
    while True:
        while result is True:
            result = non_terminal_end()
            if result == 'END':
                exit()
        result = non_terminal_init(result[0], result[1], result[2])
except:
    print_nodes(head)