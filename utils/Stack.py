class Stack:
    def __init__(self):
        self.stack = []
        self.size = 0

    def pop(self, num=1):
        if num > self.size:
            raise Exception('pop size bigger than stack size!, {}, {}'.format(self.size, num))
        self.stack = self.stack[:self.size-num]
        self.size -= num
        print("pop", self.stack)

    def top(self):
        return self.stack[self.size-1]

    def get_from_top(self, i):
        if i >= self.size:
            raise Exception("More than stack size!")
        return self.stack[self.size - i - 1]

    def push(self, key):
        self.stack += [key]
        self.size += 1
        print("push", self.stack)

    def __repr__(self):
        return str(self.stack)