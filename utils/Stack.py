class Stack:
    def __init__(self):
        self.stack = []
        self.size = 0

    def pop(self, num=1):
        if num >= self.size:
            raise Exception('pop size bigger than stack size!')
        self.stack = self.stack[:self.size-num+1]
        self.size -= num

    def top(self):
        return self.stack[self.size-1]

    def get_from_top(self, i):
        return self.stack[self.size - i - 1]

    def push(self, key):
        self.stack += [key]
        self.size += 1

