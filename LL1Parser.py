from static.first_follows import *
from static.FSMs import *
from CodeGeneration import CodeGenerator as CG
from SemanticRoutines import SemanticRoutines as SR

get_next_token = None
linum = None
curr = None
head = None
result = None
parse_errors = []
parse_tree = ''
saved_token = None
last_read_token = None
cg = CG()


class FSM:
    def __init__(self, fsm_map):
        self.current_state = 0
        self.current_char = ''
        self.fsm_map = fsm_map
        self.in_error_handling = False

    def run(self, token=None):
        global parse_errors, saved_token, last_read_token
        while True:
            if saved_token is not None:
                token = saved_token
            else:
                if token is None:
                    token = get_next_token()
                    last_read_token = token
                else:
                    token = token
            if token == saved_token:
                saved_token = None
            if self.in_error_handling and token == 'EOF':
                parse_errors += ['#{} : Syntax Error! Unexpected EndOfFile\n'.format(token[1])]
                return 'END'
            status, nxt = self.process_next(token)
            if not status:
                return nxt[0], nxt[1], token
            elif nxt == 'END':
                return 'END'
            elif nxt == 'Finish':
                return True
            elif nxt[0] == 'Finish':
                return True, nxt[1]
            else:
                token = None

    def process_next(self, token):
        global parse_errors, last_read_token
        self.current_char = token[0]
        frozen_state = self.current_state
        for transition in self.fsm_map:
            if transition['src'] == frozen_state:
                condition = transition.get('condition', None)
                if condition and transition['condition'] == token[0]:
                    #terminal
                    self.in_error_handling = False
                    terminal(token, transition.get('post', None))
                    self.update_state(transition['dst'])
                    if 'Finish' in transition.keys() and transition:
                        return True, 'Finish'
                    else:
                        return True, 'Cont'
                if condition == '':
                    #eps
                    if token[0] in follows[self.fsm_map[0]['name']]:
                        self.update_state(transition['dst'])
                        self.in_error_handling = False
                        eps(transition.get('post', None))
                        return True, ('Finish', token)
                if condition is None:
                    #non terminal
                    non_terminal_name = transition['callback']
                    if token[0] in firsts[non_terminal_name] or (
                            non_terminal_name in nullables and token[0] in follows[non_terminal_name]):
                        self.in_error_handling = False
                        return False, (transition['callback'], transition)
        # error handling
        self.in_error_handling = True
        outs = self.state_transition(frozen_state)
        if len(outs) == 1:
            out = outs[0]
            condition = out.get('condition', None)
            if condition is not None and condition == 'EOF':
                # eof
                parse_errors += ['#{} : Syntax Error! Malformed Input\n'.format(token[1])]
                return True, 'END'
            if condition is not None and condition != token[0] and condition != '':
                # terminal
                parse_errors += ['#{} : Syntax Error! Missing {}\n'.format(token[1], condition)]
                if 'Finish' in out.keys():
                    return True, 'Finish'
                else:
                    self.update_state(out['dst'])
                    return self.process_next(token)
            if condition is None:
                # non terminal
                non_terminal_name = out['callback']
                while token[0] not in firsts[non_terminal_name] and token[0] not in follows[non_terminal_name]:
                    parse_errors += ['#{} : Syntax Error! Unexpected {}\n'.format(token[1], token[0])]
                    token = get_next_token()
                    last_read_token = token
                    if token[0] == 'EOF':
                        parse_errors += ['#{} : Syntax Error! Unexpected EndOfFile\n'.format(token[1])]
                        return True, 'END'
                if token[0] in firsts[non_terminal_name]:
                    global saved_token
                    saved_token = token
                    return False, (out['callback'], out['dst'])
                if non_terminal_name in nullables:
                    return self.process_next(token)
                else:
                    if token[0] in follows[non_terminal_name]:
                        parse_errors += ['#{} : Syntax Error! Missing {}\n'.format(token[1], non_terminal_name)]
                        if 'Finish' in transition.keys() and transition:
                            return True, ('Finish', token)
                        else:
                            self.update_state(transition['dst'])
                            return True, 'Cont'
        return False, None

    def update_state(self, new_state):
        # print("{} -> {} : {}".format(self.current_char,
        #                              self.current_state,
        #                              new_state))
        self.current_state = new_state

    def state_transition(self, state):
        transitions = []
        for tr in self.fsm_map:
            if tr['src'] == state:
                transitions.append(tr)
        return transitions


class Node:
    def __init__(self, parent, sub_diagram, parent_next_state, n_type, post):
        self.parent = parent
        self.level = 0 if parent is None else parent.level + 1
        self.sub_diagram = sub_diagram
        self.parent_next_state = parent_next_state
        self.type = n_type
        self.post_routine = post
        self.children = []
        if self.type == 'Term':
            self.name = sub_diagram
        elif self.type == 'NonTerm':
            self.name = sub_diagram.fsm_map[0]['name']

    def __repr__(self):
        return 'name: ' + self.name + ' level: ' + self.level + ' parent_next_state: '\
               + self.parent_next_state + ' type: ' + self.type


def terminal(term, post):
    if term[0] == 'id' or term[0] == 'num':
        curr.children += [Node(curr, term[2], None, 'Term', post)]
    else:
        curr.children += [Node(curr, term[0], None, 'Term', post)]
    if post is not None:
        cg.execute(getattr(SR, post), last_read_token)


def eps(post):
    curr.children += [Node(curr, '', None, 'Term', post)]
    if post is not None:
        cg.execute(getattr(SR, post), last_read_token)


def is_it_the_end():
    l = []
    for x in curr.sub_diagram.fsm_map:
        if x:
            if 'Finish' in x.keys():
                l += [x['dst']]
    return curr.sub_diagram.current_state in l


def non_terminal_end(token=None):
    global curr, head
    if curr.parent is not None:
        post = curr.post_routine
        next = curr.parent_next_state
        if post is not None:
            cg.execute(getattr(SR, post), last_read_token)
        curr = curr.parent
        curr.sub_diagram.update_state(next)
        if is_it_the_end():
            return non_terminal_end(token)
        return curr.sub_diagram.run(token)
    else:
        print_nodes(head)
        return 'END'


def non_terminal_init(non_terminal_name, transition, token):
    global curr
    next_state = transition['dst']
    pre = transition.get('pre', None)
    if pre:
        cg.execute(getattr(SR, pre), last_read_token)
    post_routine = transition.get('post', None)
    curr.children += [Node(curr, FSM(globals()[non_terminal_name]), next_state, 'NonTerm', post_routine)]
    curr = curr.children[-1]
    return curr.sub_diagram.run(token)


def print_nodes(node):
    # print(node)
    global parse_tree
    parse_tree += '|\t'*node.level + node.name + '\n'
    for x in node.children:
        print_nodes(x)