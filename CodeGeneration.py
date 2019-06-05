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

    def execute(self, func, token):
        key = token[2] if (token[0] == 'id' or token[0] == 'num') else token[0]
        func(self, key)
        print(self.symbol_table)
