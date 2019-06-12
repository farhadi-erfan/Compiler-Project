class SemanticRoutines:

    @staticmethod
    def label(cg, token=None):
        cg.ss.push(cg.index)

    @staticmethod
    def plast(cg, token):
        cg.ss.push(token)

    @staticmethod
    def assign(cg, addr_from, addr_to):
        cg.pb[cg.index] = '(ASSIGN, {}, {})'.format(addr_from, addr_to)
        cg.index += 4

    @staticmethod
    def vardec(cg, token=None):
        identifier_token = cg.ss.top()

        if identifier_token == ';':
            # paddr
            cg.symbol_table.push({
                'token': cg.ss.get_from_top(1),
                'type': cg.ss.get_from_top(2),
                'addr': cg.data_index,
                'ref': True
            })
            cg.data_index += 4
            cg.ss.pop(3)

        elif identifier_token == ']':
            cg.symbol_table.push({
                'token': cg.ss.get_from_top(2),
                'type': cg.ss.get_from_top(3),
                'addr': cg.ss.data_index
            })
            SemanticRoutines.assign(cg, '#{}'.format(cg.data_index + 4), '{}'.format(cg.data_index))
            arr_size = cg.ss.get_from_top(1)
            cg.data_index += 4 * (arr_size + 1)
            cg.ss.pop(4)

        elif identifier_token == ')':
            pass    # TODO: function dec

    def null(self, cg):
        cg.ss.push('NaK') # not an important key

    def paddr(self, cg, id):
        cg.ss.push(cg.get_address_by_token(id))