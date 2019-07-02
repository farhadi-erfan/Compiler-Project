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

            if cg.ss.get_from_top(3) == 'void':
                raise Exception("‫‪Illegal‬‬ ‫‪type‬‬ ‫‪of‬‬ ‫‪void.‬‬")

            arr_size = cg.ss.get_from_top(1)
            cg.symbol_table.push({
                'token': cg.ss.get_from_top(2),
                'type': cg.ss.get_from_top(3),
                'addr': cg.data_index,
                'ref': True,
                'size': arr_size
            })
            SemanticRoutines.assign(cg, '#{}'.format(cg.data_index + 4), '{}'.format(cg.data_index))
            arr_size = cg.ss.get_from_top(1)
            cg.data_index += 4 * (int(arr_size) + 1)
            cg.ss.pop(4)

    @staticmethod
    def fundec(cg, token=None):
        cg.symbol_table.push({
            'token': cg.ss.top(),
            'type': cg.ss.get_from_top(1),
            'addr': cg.index,
            'is_func': True,
            'args': [],
            'jmp_position': cg.jmp_position_index,
            'result_addr': cg.return_values_index
        })
        cg.symbol_table.push({
            'token': 'NaK',
            'type': 'divider'
        })
        cg.return_values_index += 4
        cg.jmp_position_index += 4
        fun_name = cg.ss.top()
        cg.ss.pop(2)
        cg.ss.push(fun_name)

    @staticmethod
    def null(cg, token=None):
        cg.ss.push('NaK')  # not an important key

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
        if '#' not in s1:
            a = cg.get_dict_by_address(s1)
            if a:
                ref = a.get('ref', False)
                is_func = a.get('is_func', False)
                if ref or is_func:
                    raise Exception('‫‪Type‬‬ ‫‪mismatch‬‬ ‫‪in‬‬ ‫‪operands.‬‬')
        if '#' not in val:
            a = cg.get_dict_by_address(s1)
            if a:
                ref = a.get('ref', False)
                is_func = cg.symbol_table[a].get('is_func', False)
                if ref or is_func:
                    raise Exception('‫‪Type‬‬ ‫‪mismatch‬‬ ‫‪in‬‬ ‫‪operands.‬‬')

        cg.ss.pop(2)
        t2 = SemanticRoutines.get_temp(cg)
        SemanticRoutines.mult(cg, val, s1, t2)
        cg.ss.push(t2)

    @staticmethod
    def calc_addop(cg, token=None):
        val = cg.ss.top()
        dest = cg.ss.get_from_top(2)
        if '#' not in dest:
            a = cg.get_dict_by_address(dest)
            if a:
                ref = a.get('ref', False)
                is_func = a.get('is_func', False)
                if ref or is_func:
                    raise Exception('‫‪Type‬‬ ‫‪mismatch‬‬ ‫‪in‬‬ ‫‪operands.‬‬')
        if '#' not in val:
            a = cg.get_dict_by_address(val)
            if a:
                ref = a.get('ref', False)
                is_func = a.get('is_func', False)
                if ref or is_func:
                    raise Exception('‫‪Type‬‬ ‫‪mismatch‬‬ ‫‪in‬‬ ‫‪operands.‬‬')
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
        if '#' not in rhs:
            a = cg.get_dict_by_address(rhs)
            if a:
                ref = a.get('ref', False)
                is_func = a.get('is_func', False)
                if ref or is_func:
                    raise Exception('‫‪Type‬‬ ‫‪mismatch‬‬ ‫‪in‬‬ ‫‪operands.‬‬')
        if '#' not in lhs:
            a = cg.get_dict_by_address(lhs)
            if a:
                ref = a.get('ref', False)
                is_func = a.get('is_func', False)
                if ref or is_func:
                    raise Exception('‫‪Type‬‬ ‫‪mismatch‬‬ ‫‪in‬‬ ‫‪operands.‬‬')
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
        else:
            cg.ss.pop(2)
        cg.ss.push(cg.index)
        print(cg.index)
        cg.index += 4

    @staticmethod
    def jp_finish(cg, token=None):
        cg.pb[cg.ss.top()] = '(JP, {}, , )'.format(str(cg.index))
        cg.ss.pop(2)

    @staticmethod
    def pop_1(cg, token=None):
        cg.ss.pop(1)

    @staticmethod
    def break_(cg, token=None):
        if 'while' not in cg.ss.stack and 'switch' not in cg.ss.stack:
            raise Exception('‫‪No‬‬ ‫’‪’while‬‬ ‫‪or‬‬ ‫’‪’switch‬‬ ‫‪found‬‬ ‫‪for‬‬ ‫‪’break’.‬‬')
        if 'switch' in cg.ss.stack and 'while' not in cg.ss.stack:
            return
        if 'switch' in cg.ss.stack and 'while' in cg.ss.stack:
            if cg.ss.get_index('switch') > 0 and cg.ss.get_index('while') > 0:
                if cg.ss.get_index('switch') > cg.ss.get_index('while'):
                    return

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

    @staticmethod
    def new_scope(cg, token=None):
        cg.scope_stack.push(cg.symbol_table.stack.__len__())

    @staticmethod
    def remove_scope(cg, token=None):
        while len(cg.symbol_table.stack) > cg.scope_stack.top():
            cg.symbol_table.pop()
        cg.scope_stack.pop()


    @staticmethod
    def param_dec(cg, token=None):
        last_token = cg.ss.top()
        if last_token == ']':

            if cg.ss.get_from_top(2) == 'void':
                raise Exception("‫‪Illegal‬‬ ‫‪type‬‬ ‫‪of‬‬ ‫‪void.‬‬")

            cg.symbol_table.push({
                'token': cg.ss.get_from_top(1),
                'type': cg.ss.get_from_top(2),
                'addr': cg.arg_index,
                'ref': True
            })
            cg.ss.pop(3)
        else:

            if cg.ss.get_from_top(1) == 'void':
                raise Exception("‫‪Illegal‬‬ ‫‪type‬‬ ‫‪of‬‬ ‫‪void.‬‬")

            cg.symbol_table.push({
                'token': cg.ss.top(),
                'type': cg.ss.get_from_top(1),
                'addr': cg.arg_index
            })
            cg.ss.pop(2)
        cg.arg_index += 4
        func = cg.ss.top()
        for symcell in cg.symbol_table.stack:
            if symcell['token'] == func and symcell.get('is_func', False):
                symcell['args'] += [cg.arg_index - 4]
                return
        raise Exception('could not find function')

    @staticmethod
    def set_result(cg, token=None):
        func = cg.ss.get_from_top(1)
        for symcell in cg.symbol_table.stack:
            if symcell['token'] == func and symcell.get('is_func', False):
                result_addr = symcell['result_addr']
                result = cg.ss.top()
                cg.pb[cg.index] = '(ASSIGN, {}, {}, )'.format(result, result_addr)
                cg.index += 4
                cg.ss.pop()
                return
        raise Exception('could not find function')

    @staticmethod
    def func_return(cg, token=None):
        # this should run too on every time function returns
        while cg.symbol_table.top()['token'] != 'NaK':
            cg.symbol_table.pop()
        cg.symbol_table.pop()
        cg.symbol_table.top()['jmp_position'] = cg.index
        cg.pb[cg.index] = '(JP, , , )'
        cg.index += 4

    @staticmethod
    def arg(cg, token=None):
        if cg.ss.get_from_top(1) == 'output':
            cg.pb[cg.index] = '(PRINT, {}, , )'.format(cg.ss.top())
            cg.index += 4
            cg.ss.pop()
        else:
            arg_addr = cg.get_arg_address_by_token_and_num(cg.ss.get_from_top(1), cg.current_arg)
            cg.pb[cg.index] = '(ASSIGN, {}, {}, )'.format(cg.ss.top(), arg_addr)
            cg.index += 4
            cg.ss.pop()
            cg.current_arg += 1

    @staticmethod
    def func_jmp(cg, token=None):
        func = cg.ss.top()
        cg.ss.pop()
        if func != 'output':
            func_addr = cg.get_address_by_token(func)
            for symcell in cg.symbol_table.stack:
                if symcell['token'] == func and symcell.get('is_func', False):
                    if cg.current_arg != len(symcell['args']):
                        raise Exception('Mismatch in numbers of arguments of ’{}’.'.format(func))
                    cg.pb[cg.index] = '(ASSIGN, #{}, {}, )'.format(cg.index + 8, symcell['jmp_position'])
                    cg.index += 4
                    cg.ss.push(symcell['result_addr'])
                    break
            cg.pb[cg.index] = '(JP, {}, , )'.format(func_addr)
            cg.index += 4
            cg.current_arg = 0

    @staticmethod
    def set_main(cg, token=None):
        for symcell in cg.symbol_table.stack:
            if symcell['token'] == 'main' and symcell['type'] == 'void' and len(symcell['args']) == 0:
                cg.pb[0] = '(JP, {}, , )'.format(symcell['addr'])
                return
        raise Exception('main function not found!')
