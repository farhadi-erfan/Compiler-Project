class SemanticRoutines:

    @staticmethod
    def label(cg, token=None):
        cg.ss.push(cg.index)

    @staticmethod
    def plast(cg, token):
        cg.ss.push(token)

    @staticmethod
    def assign_expr(cg, token=None):
        dest = cg.ss.get_from_top(1)
        cg.pb[cg.index] = '(ASSIGN, {}, {})'.format(cg.ss.top(), cg.ss.get_from_top(1))
        cg.index += 4
        cg.ss.pop(2)
        cg.ss.push('{}'.format(dest))

    @staticmethod
    def assign(cg, addr_from, addr_to):
        cg.pb[cg.index] = '(ASSIGN, {}, {})'.format(addr_from, addr_to)
        cg.index += 4
        cg.index += 4

    @staticmethod
    def vardec(cg, token=None):
        identifier_token = cg.ss.top()

        if identifier_token == ';':
            # paddr
            cg.symbol_table.push({
                'token': cg.ss.get_from_top(1),
                'type': cg.ss.get_from_top(2),
                'addr': cg.data_index
            })
            cg.data_index += 4
            cg.ss.pop(3)

        elif identifier_token == ']':
            cg.symbol_table.push({
                'token': cg.ss.get_from_top(2),
                'type': cg.ss.get_from_top(3),
                'addr': cg.data_index,
                'ref': True
            })
            SemanticRoutines.assign(cg, '#{}'.format(cg.data_index + 4), '{}'.format(cg.data_index))
            arr_size = cg.ss.get_from_top(1)
            cg.data_index += 4 * (int(arr_size) + 1)
            cg.ss.pop(4)

        elif identifier_token == ')':
            pass    # TODO: function dec

    @staticmethod
    def null(cg, token=None):
        cg.ss.push('NaK') # not an important key

    @staticmethod
    def paddr(cg, id):
        cg.ss.push(cg.get_address_by_token(id))

    @staticmethod
    def get_temp(cg):
        cg.temp_index += 4
        return str(cg.temp_index - 4)

    @staticmethod
    def add(cg, s1, s2, d):
        cg.pb[cg.index] = '(ADD, {}, {}, {})'.format(s1, s2, d)
        cg.index += 4

    @staticmethod
    def not_(cg, s, d):
        cg.pb[cg.index] = '(NOT, {}, {})'.format(s, d)
        cg.index += 4

    @staticmethod
    def mult(cg, s1, s2, d):
        cg.pb[cg.index] = '(MULT, {}, {}, {})'.format(s1, s2, d)
        cg.index += 4

    @staticmethod
    def sub(cg, s1, s2, d):
        cg.pb[cg.index] = '(ADD, {}, {}, {})'.format(s1, s2, d)
        cg.index += 4

    @staticmethod
    def calc_addr(cg, token=None):
        if token == ']':
            addr = cg.get_address_by_token(cg.ss.get_from_top(1))
            t = SemanticRoutines.get_temp(cg)
            index = cg.ss.get_from_top(0)
            cg.ss.pop(2)
            t2 = SemanticRoutines.get_temp(cg)
            SemanticRoutines.mult(cg, '#4', index, t2)
            SemanticRoutines.add(cg, addr, t2, t)
            cg.ss.push('@{}'.format(t))

        else:
            addr = cg.get_address_by_token(cg.ss.get_from_top(0))
            cg.ss.pop(1)
            cg.ss.push('{}'.format(addr))

    @staticmethod
    def calc_mult(cg, token=None):
        val = cg.ss.top()
        s1 = cg.ss.get_from_top(1)
        cg.ss.pop(2)
        t2 = SemanticRoutines.get_temp(cg)
        SemanticRoutines.mult(cg, val, s1, t2)
        cg.ss.push(t2)

    @staticmethod
    def calc_addop(cg, token=None):
        val = cg.ss.top()
        dest = cg.ss.get_from_top(2)
        addop = cg.ss.get_from_top(1)
        cg.ss.pop(3)
        t2 = SemanticRoutines.get_temp(cg)
        if addop == '+':
            SemanticRoutines.add(cg, val, dest, t2)
        elif addop == '-':
            SemanticRoutines.sub(cg, val, dest, t2)
        cg.ss.push(t2)

    @staticmethod
    def pnum(cg, token=None):
        cg.ss.push('#{}'.format(token))

    @staticmethod
    def calc_sign(cg, token=None):
        sign = cg.ss.get_from_top(1)
        val = cg.ss.top()
        cg.ss.pop(2)
        if sign == '-':
            t1 = SemanticRoutines.get_temp(cg)
            SemanticRoutines.not_(cg, val, t1)
            val = t1
        cg.ss.push(val)
