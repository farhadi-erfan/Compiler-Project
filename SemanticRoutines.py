class SemanticRoutines:

    @staticmethod
    def label(cg, token=None):
        cg.ss.push(cg.index)

    @staticmethod
    def plast(cg, token):
        cg.ss.push(token)

    @staticmethod
    def assign_expr(cg, token=None):
        cg.pb[cg.index] = '(ASSIGN, {}, {})'.format(cg.ss.top(), cg.ss.get_from_top(1))
        cg.index += 4
        cg.ss.pop(1)

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
            if cg.ss.get_from_top(2) == 'void':
                raise Exception("‫‪Illegal‬‬ ‫‪type‬‬ ‫‪of‬‬ ‫‪void.‬‬")

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

    @staticmethod
    def lt(cg, s1, s2, d):
        cg.pb[cg.index] = '(LT, {}, {}, {})'.format(s1, s2, d)
        cg.index += 4

    @staticmethod
    def eq(cg, s1, s2, d):
        cg.pb[cg.index] = '(EQ, {}, {}, {})'.format(s1, s2, d)
        cg.index += 4

    @staticmethod
    def calc_relop(cg, token=None):
        relop = cg.ss.get_from_top(1)
        lhs = cg.ss.get_from_top(2)
        rhs = cg.ss.top()
        cg.ss.pop(3)
        t = SemanticRoutines.get_temp(cg)
        if relop == '==':
            SemanticRoutines.eq(cg, lhs, rhs, t)
        elif relop == '<':
            SemanticRoutines.lt(cg, lhs, rhs, t)
        cg.ss.push(t)

    @staticmethod
    def save(cg, token=None):
        cg.ss.push(cg.index)
        cg.index += 4

    @staticmethod
    def save_jpf(cg, token=None):
        tos = 0
        if cg.ss.get_from_top(1) == ('break' or 'continue'):
            tos = 2
        cg.pb[cg.ss.get_from_top(tos)] = '(JPF, {}, {}, )'.format(cg.ss.get_from_top(tos + 1), str(cg.index + 4))
        if tos > 0:
            save_1, save_2 = cg.ss.get_from_top(0), cg.ss.get_from_top(1)
            cg.ss.pop(4)
            cg.ss.push(save_2), cg.ss.push(save_1)
        else: cg.ss.pop(2)
        cg.ss.push(cg.index)
        print(cg.index)
        cg.index += 4

    @staticmethod
    def jp(cg, token=None):
        cg.pb[cg.ss.top()] = '(JP, {}, , )'.format(str(cg.index))
        cg.ss.pop(1)

    @staticmethod
    def pop_1(cg, token=None):
        cg.ss.pop(1)

    @staticmethod
    def break_(cg, token=None):
        if 'while' not in cg.ss.stack and 'switch' not in cg.ss.stack:
            raise Exception('‫‪No‬‬ ‫’‪’while‬‬ ‫‪or‬‬ ‫’‪’switch‬‬ ‫‪found‬‬ ‫‪for‬‬ ‫‪’break’.‬‬')
        cg.ss.push('break')
        SemanticRoutines.save(cg)

    @staticmethod
    def breaks_jpf_jp(cg, token=None):
        while cg.ss.get_from_top(1) == 'break':
            cg.pb[cg.ss.top()] = '(JP, {}, , )'.format(str(cg.index + 4))
            cg.ss.pop(2)
        cg.pb[cg.ss.top()] = '(JPF, {}, {}, )'.format(cg.ss.get_from_top(1), str(cg.index + 4))
        cg.pb[cg.index] = '(JP, {}, , )'.format(str(cg.ss.top()))
        cg.ss.pop(3)

    @staticmethod
    def continue_(cg, token=None):
        if 'while' not in cg.ss.stack not in cg.ss.stack:
            raise Exception('‫‪No‬‬ ‫’‪’while‬‬ ‫‪found‬‬ ‫‪for‬‬‪‪ ’‫‪continue’.‬‬')
        cg.pb[cg.index] = '(JP, {}, , )'.format(str(cg.ss.top()))
        cg.index += 4

    @staticmethod
    def eq_save(cg, token=None):
        t = SemanticRoutines.get_temp(cg)
        if cg.ss.top() == 'NaK':
            cg.pb[cg.index] = '(EQ, #{}, {}, {})'.format(str(token), cg.ss.get_from_top(1), t)

        else:
            cg.pb[cg.index] = '(EQ, #{}, {}, {})'.format(str(token), cg.ss.get_from_top(1), t)
            a = cg.ss.top()
            cg.ss.pop(2)
            cg.ss.push(a)
        cg.ss.push(t)
        cg.ss.push(cg.index + 4)
        cg.index += 8

    @staticmethod
    def jp_save_jpf(cg, token=None):
        if cg.ss.get_from_top(2) == 'NaK':
            cg.pb[cg.ss.top()] = '(JPF, {}, {}, )'.format(cg.ss.get_from_top(1), str(cg.index + 4))
        else:
            cg.pb[cg.ss.get_from_top(2)] = '(JP, {}, , )'.format(str(cg.index))
            cg.pb[cg.ss.top()] = '(JPF, {}, {}, )'.format(cg.ss.get_from_top(1), str(cg.index + 4))
        cg.ss.pop(3)
        SemanticRoutines.save(cg, token)
