from utils.Stack import Stack


class CodeGenerator:
    def __init__(self):
        self.index = 0
        self.ss = Stack()
        self.symbol_table = Stack()
        self.scope_stack = Stack()
        self.pb = [0] * 800
        self.data_index = 100
        self.temp_index = 500

    def get_address_by_token(self, label):
        for symcell in self.symbol_table.stack:
            if symcell['token'] == label:
                return symcell['addr']
        raise Exception("label not found!")

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
                print(ind, x)