from LexicalAnalysis import get_next_token


class FSM:

    def __init__(self, fsm_map):
        self.current_state = 0
        self.current_char = ''
        self.fsm_map = fsm_map

    def run(self):
        while True:
            token = get_next_token()
            status, nxt = self.process_next(token)
            if not status:
                return nxt
            elif nxt == 'Finish':
                return True

    def process_next(self, achar):
        self.current_char = achar
        frozen_state = self.current_state
        for transition in self.fsm_map:
            if transition['src'] == frozen_state:
                condition = transition.get('condition', None)
                if condition and transition['condition'] == achar:
                    if transition['finish']:
                        return True, 'Finish'
                    else:
                        self.update_state(transition['dst'])
                        return True, 'Cont'
                if not condition:
                    return False, (transition['callback'], frozen_state)
        return False

    def update_state(self, new_state):
        print("{} -> {} : {}".format(self.current_char,
                                     self.current_state,
                                     new_state))
        self.current_state = new_state
