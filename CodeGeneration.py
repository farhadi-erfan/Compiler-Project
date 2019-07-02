from utils.Stack import Stack


class CodeGenerator:
    def __init__(self):
        self.index = 4
        self.ss = Stack()
        self.symbol_table = Stack()
        self.scope_stack = Stack()
        self.pb = [0] * 1000
        self.data_index = 100
        self.temp_index = 500
        self.jmp_position_index = 700
        self.arg_index = 800
        self.return_values_index = 900
        self.current_arg = 0

    def get_address_by_token(self, label):
        for symcell in self.symbol_table.stack:
            if symcell['token'] == label:
                return symcell['addr']
        raise Exception("’{}’ is not defined.".format(label))

    def get_arg_address_by_token_and_num(self, func, num):
        for symcell in self.symbol_table.stack:
            if symcell['token'] == func and symcell.get('is_func', False):
                if num < len(symcell['args']):
                    return symcell['args'][num]
                else:
                    raise Exception('Mismatch in numbers of arguments of ’{}’.'.format(func))
        raise Exception("’{}’ is not defined.".format(func))

    def get_temp(self):
        res = self.temp_index
        self.temp_index += 4
        return res

    def execute(self, func, token):
        key = token[2] if (token[0] == 'id' or token[0] == 'num') else token[0]
        func(self, key)
        self.print_pb()

    def print_pb(self):
        for ind, x in enumerate(self.pb):
            if x != 0:
                print(ind, x, sep='\t')
    print()
