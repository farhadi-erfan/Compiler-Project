from utils.Stack import Stack


class CodeGenerator:
    def __init__(self):
        # self.index = 2
        self.index = 1
        self.ss = Stack()
        self.symbol_table = Stack()
        self.scope_stack = Stack()
        self.scope_stack.push((0, None))
        self.pb = [0] * 10000
        self.data_index = 1000
        self.temp_index = 5000
        self.jmp_position_index = 7000
        self.arg_index = 8000
        self.return_values_index = 9000
        self.current_arg = 0
        self.in_rhs = False
        self.semantic_errors = []

    def get_address_by_token(self, label):
        for symcell in self.symbol_table.stack:
            if symcell['token'] == label:
                if self.in_rhs and symcell['type'] == 'void':
                    raise Exception('using return value of void function: {}.'.format(label))
                return symcell['addr']
        raise Exception("\'{}\' is not defined.".format(label))

    def get_arg_address_by_token_and_num(self, func, num):
        for symcell in self.symbol_table.stack:
            if symcell['token'] == func and symcell.get('is_func', False):
                if num < len(symcell['args']):
                    return symcell['args'][num]
                else:
                    raise Exception('Mismatch in numbers of arguments of \'{}\'.'.format(func))
        raise Exception("\'{}\' is not defined.".format(func))

    def get_temp(self):
        res = self.temp_index
        self.temp_index += 4
        return res

    def execute(self, func, token):
        key = token[2] if (token[0] == 'id' or token[0] == 'num') else token[0]
        try:
            func(self, key)
        except Exception as e:
            self.semantic_errors += ['#{}:\t{}\n'.format(str(token[1]), str(e))]
        self.print_pb()

    def print_pb(self):
        for ind, x in enumerate(self.pb):
            if x != 0:
                print(ind, x, sep='\t')
    print()

    def get_dict_by_address(self, address):
        for x in self.symbol_table.stack:
            addr = x.get('addr', None)
            if not addr:
                continue
            if addr == address or addr == int(address):
                return x

    def get_dict_by_token(self, token):
        for x in self.symbol_table.stack:
            if x['token'] == token:
                return x
        raise Exception("\'{}\' is not defined.".format(token))

    def output_pb(self):
        with open('in_out/' + 'output.txt', 'w+') as f:
            for ind, x in enumerate(self.pb):
                if x != 0:
                    l = '{}\t{}\n'.format((str(ind)), x)
                    f.write(l)
