#  {'src':, 'dst':, 'condition':, 'callback': }
PROGRAM = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'DL', 'name': 'Program'},
           {'src': 1, 'dst': 2, 'condition': 'EOF', 'callback': None, 'Finish': True, 'post': 'set_main'})

DL = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'DL1', 'Finish': True, 'name': 'DL'}, None)

DL1 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Dec', 'name': 'DL1'},
       {'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'Finish': True},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'DL1', 'Finish': True})

Dec = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'TS', 'name': 'Dec', 'post': 'plast'},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FTS2', 'Finish': True})

FTS2 = ({'src': 0, 'dst': 1, 'condition': 'id', 'callback': None, 'name': 'FTS2', 'post': 'plast'},
        {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Fid4', 'Finish': True, 'post': 'vardec'})

Fid4 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Fid1', 'Finish': True, 'name': 'Fid4'},
        {'src': 0, 'dst': 2, 'condition': '(', 'callback': None, 'post': 'fundec'},
        {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Params'},
        {'src': 3, 'dst': 4, 'condition': ')', 'callback': None},
        {'src': 4, 'dst': 2, 'condition': None, 'callback': 'CompStmt', 'Finish': True})

Fid1 = ({'src': 0, 'dst': 1, 'condition': ';', 'callback': None, 'Finish': True, 'name': 'Fid1', 'post': 'plast'},
        {'src': 0, 'dst': 2, 'condition': '[', 'callback': None},
        {'src': 2, 'dst': 3, 'condition': 'num', 'callback': None, 'post': 'plast'},
        {'src': 3, 'dst': 4, 'condition': ']', 'callback': None, 'post': 'plast'},
        {'src': 4, 'dst': 5, 'condition': ';', 'callback': None, 'Finish': True})

TS = ({'src': 0, 'dst': 1, 'condition': 'int', 'callback': None, 'name': 'TS', 'Finish': True},
      {'src': 0, 'dst': 2, 'condition': 'void', 'callback': None, 'Finish': True})

Params = ({'src': 0, 'dst': 1, 'condition': 'void', 'callback': None, 'name': 'Params', 'post': 'plast'},
          {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FParam', 'Finish': True},
          {'src': 0, 'dst': 3, 'condition': 'int', 'callback': None, 'post': 'plast'},
          {'src': 3, 'dst': 4, 'condition': None, 'callback': 'FTS1', 'post': 'param_dec'},
          {'src': 4, 'dst': 5, 'condition': None, 'callback': 'PL1', 'Finish': True})

FParam = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'FTS1', 'name': 'FParam', 'post': 'param_dec'},
         {'src': 1, 'dst': 2, 'condition': None, 'callback': 'PL1', 'Finish': True},
         {'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'Finish': True, 'post': 'pop_1'})

PL1 = ({'src': 0, 'dst': 1, 'condition': ',', 'callback': None, 'name': 'PL1'},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Param', 'post': 'param_dec'},
       {'src': 2, 'dst': 3, 'condition': None, 'callback': 'PL1', 'Finish': True},
       {'src': 0, 'dst': 3, 'condition': '', 'callback': None, 'Finish': True})

Param = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'TS', 'name': 'Param', 'post': 'plast'},
         {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FTS1', 'Finish': True})

FTS1 = ({'src': 0, 'dst': 1, 'condition': 'id', 'callback': None, 'name': 'FTS1', 'post': 'plast'},
        {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Fid2', 'Finish': True})

Fid2 = ({'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'name': 'Fid2', 'Finish': True},
        {'src': 0, 'dst': 1, 'condition': '[', 'callback': None},
        {'src': 1, 'dst': 2, 'condition': ']', 'callback': None, 'Finish': True, 'post': 'plast'})

CompStmt = ({'src': 0, 'dst': 1, 'condition': '{', 'callback': None, 'name': 'CompStmt', 'post': 'new_scope'},
            {'src': 1, 'dst': 2, 'condition': None, 'callback': 'DL'},
            {'src': 2, 'dst': 3, 'condition': None, 'callback': 'SL', 'post': 'remove_scope'},
            {'src': 3, 'dst': 4, 'condition': '}', 'callback': None, 'Finish': True})

SL = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'SL1', 'name': 'SL', 'Finish': True}, None)

SL1 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Stmt', 'name': 'SL1'},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'SL1', 'Finish': True},
       {'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'Finish': True})

Stmt = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'ExpStmt', 'Finish': True, 'name': 'Stmt'},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'CompStmt', 'Finish': True},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'SelStmt', 'Finish': True},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'IterStmt', 'Finish': True},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'RetStmt', 'Finish': True},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'SwitchStmt', 'Finish': True})

ExpStmt = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Expr', 'post': 'pop_1', 'name': 'ExpStmt'},
           {'src': 1, 'dst': 2, 'condition': ';', 'callback': None, 'Finish': True},
           {'src': 0, 'dst': 3, 'condition': 'continue', 'callback': None, 'post': 'continue_'},
           {'src': 3, 'dst': 2, 'condition': ';', 'callback': None, 'Finish': True},
           {'src': 0, 'dst': 4, 'condition': 'break', 'callback': 'SL', 'post': 'break_'},
           {'src': 4, 'dst': 2, 'condition': ';', 'callback': None, 'Finish': True},
           {'src': 0, 'dst': 2, 'condition': ';', 'callback': None, 'Finish': True})

SelStmt = ({'src': 0, 'dst': 1, 'condition': 'if', 'callback': None, 'name': 'SelStmt'},
           {'src': 1, 'dst': 2, 'condition': '(', 'callback': None},
           {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Expr'},
           {'src': 3, 'dst': 4, 'condition': ')', 'callback': None, 'post': 'save'},
           {'src': 4, 'dst': 5, 'condition': None, 'callback': 'Stmt', 'post': 'save_jpf'},
           {'src': 5, 'dst': 6, 'condition': 'else', 'callback': None},
           {'src': 6, 'dst': 7, 'condition': None, 'callback': 'Stmt', 'post': 'jp', 'Finish': True})

IterStmt = ({'src': 0, 'dst': 1, 'condition': 'while', 'callback': None, 'name': 'IterStmt', 'post': 'plast'},
            {'src': 1, 'dst': 2, 'condition': '(', 'callback': None},
            {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Expr'},
            {'src': 3, 'dst': 4, 'condition': ')', 'callback': None, 'post': 'save'},
            {'src': 4, 'dst': 5, 'condition': None, 'callback': 'Stmt', 'Finish': True, 'post': 'breaks_jpf_jp'})

RetStmt = ({'src': 0, 'dst': 1, 'condition': 'return', 'callback': None, 'name': 'RetStmt'},
           {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Fret', 'Finish': True, 'post': 'func_return'})

Fret = ({'src': 0, 'dst': 2, 'condition': ';', 'callback': None, 'name': 'Fret', 'Finish': True},
        {'src': 0, 'dst': 1, 'condition': None, 'callback': 'Expr', 'post': 'set_result'},
        {'src': 1, 'dst': 2, 'condition': ';', 'callback': 'None', 'Finish': True})

SwitchStmt = ({'src': 0, 'dst': 1, 'condition': 'switch', 'callback': None, 'name': 'SwitchStmt', 'post': 'plast'},
              {'src': 1, 'dst': 2, 'condition': '(', 'callback': None},
              {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Expr'},
              {'src': 3, 'dst': 4, 'condition': ')', 'callback': None},
              {'src': 4, 'dst': 5, 'condition': '{', 'callback': None},
              {'src': 5, 'dst': 6, 'condition': None, 'callback': 'CaseStmts'},
              {'src': 6, 'dst': 7, 'condition': None, 'callback': 'DefaultStmt', 'post': 'jp_finish'},
              {'src': 7, 'dst': 8, 'condition': '}', 'callback': None, 'Finish': True})

CaseStmts = ({'src': 0, 'pre': 'null', 'dst': 1, 'condition': None, 'callback': 'CaseStmts_1', 'name': 'CaseStmts',
              'Finish': True}, None)

CaseStmts_1 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'CaseStmt', 'name': 'CaseStmts_1'},
               {'src': 1, 'dst': 2, 'condition': None, 'callback': 'CaseStmts_1', 'Finish': True},
               {'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'Finish': True})

CaseStmt = ({'src': 0, 'dst': 1, 'condition': 'case', 'callback': None, 'name': 'CaseStmt'},
            {'src': 1, 'dst': 2, 'condition': 'num', 'callback': None, 'post': 'eq_save'},
            {'src': 2, 'dst': 3, 'condition': ':', 'callback': None},
            {'src': 3, 'dst': 4, 'condition': None, 'callback': 'SL', 'Finish': True, 'post': 'jp_save_jpf'})

DefaultStmt = ({'src': 0, 'dst': 1, 'condition': 'default', 'callback': None, 'name': 'DefaultStmt'},
               {'src': 1, 'dst': 2, 'condition': ':', 'callback': None},
               {'src':2, 'dst': 3, 'condition': None, 'callback': 'SL', 'Finish': True},
               {'src': 0, 'dst': 3, 'condition': '', 'callback': None, 'Finish': True})

Expr = ({'src': 0, 'dst': 1, 'condition': 'id', 'callback': None, 'name': 'Expr', 'post': 'plast'},
        {'src': 1, 'dst': 4, 'condition': None, 'callback': 'FExpr', 'Finish': True},
        {'src': 0, 'dst': 2, 'condition': None, 'callback': 'Term_2'},
        {'src': 2, 'dst': 3, 'condition': None, 'callback': 'AdditiveExpr_1'},
        {'src': 3, 'dst': 4, 'condition': None, 'callback': 'FAdditiveExpr', 'Finish': True})

FExpr = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Fid', 'name': 'FExpr', 'post': 'calc_addr'},
         {'src': 1, 'dst': 2, 'condition': None, 'callback': 'FExpr1', 'Finish': True},
         {'src': 0, 'dst': 2, 'condition': '(', 'callback': None},
         {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Args'},
         {'src': 3, 'dst': 4, 'condition': ')', 'callback': None, 'post': 'func_jmp'},
         {'src': 4, 'dst': 5, 'condition': None, 'callback': 'Term_1'},
         {'src': 5, 'dst': 6, 'condition': None, 'callback': 'AdditiveExpr_1'},
         {'src': 6, 'dst': 7, 'condition': None, 'callback': 'FAdditiveExpr', 'Finish': True})

FExpr1 = ({'src': 0, 'dst': 1, 'condition': '=', 'callback': None, 'name': 'FExpr1', 'post': 'rhs'},
          {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Expr', 'Finish': True, 'post': 'assign_expr'},
          {'src': 0, 'dst': 5, 'condition': None, 'callback': 'Term_1'},
          {'src': 5, 'dst': 6, 'condition': None, 'callback': 'AdditiveExpr_1'},
          {'src': 6, 'dst': 7, 'condition': None, 'callback': 'FAdditiveExpr', 'Finish': True})

Fid = ({'src': 0, 'dst': 1, 'condition': '[', 'callback': None, 'name': 'Fid'},
       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Expr'},
       {'src': 2, 'dst': 3, 'condition': ']', 'callback': None, 'Finish': True},
       {'src': 0, 'dst': 1, 'condition': '', 'callback': None, 'Finish': True})

FAdditiveExpr = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Relop', 'name': 'FAdditiveExpr',
                  'post': 'plast'},
                       {'src': 1, 'dst': 2, 'condition': None, 'callback': 'AdditiveExpr', 'Finish': True,
                        'post': 'calc_relop'},
                       {'src': 0, 'dst': 2, 'condition': '', 'callback': None, 'Finish': True})

Relop = ({'src': 0, 'dst': 1, 'condition': '<', 'callback': None, 'name': 'Relop', 'Finish': True},
         {'src': 0, 'dst': 1, 'condition': '==', 'callback': None, 'Finish': True})

AdditiveExpr = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Term', 'name': 'AdditiveExpr'},
                      {'src': 1, 'dst': 2, 'condition': None, 'callback': 'AdditiveExpr_1', 'Finish': True})

AdditiveExpr_1 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Addop', 'name': 'AdditiveExpr_1'},
                  {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Term', 'post': 'calc_addop'},
                  {'src': 2, 'dst': 3, 'condition': None, 'callback': 'AdditiveExpr_1', 'Finish': True},
                  {'src': 0, 'dst': 3, 'condition': '', 'callback': None, 'Finish': True})

Addop = ({'src': 0, 'dst': 1, 'condition': '+', 'callback': None, 'name': 'Addop', 'Finish': True, 'post': 'plast'},
         {'src': 0, 'dst': 1, 'condition': '-', 'callback': None, 'name': 'Addop', 'Finish': True, 'post': 'plast'})

Term = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'SignedFactor', 'name': 'Term'},
        {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Term_1', 'Finish': True})

Term_1 = ({'src': 0, 'dst': 1, 'condition': '*', 'callback': None, 'name': 'Term_1'},
          {'src': 1, 'dst': 2, 'condition': None, 'callback': 'SignedFactor', 'post': 'calc_mult'},
          {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Term_1', 'Finish': True},
          {'src': 0, 'dst': 3, 'condition': '', 'callback': None, 'Finish': True})

Term_2 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'SignedFactor2', 'name': 'Term_2'},
        {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Term_1', 'Finish': True})


SignedFactor = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Factor', 'Finish': True,
                 'name': 'SignedFactor', 'pre': 'null', 'post': 'calc_sign'},
                {'src': 0,'dst': 2, 'condition': '+', 'callback': None, 'post': 'plast'},
                {'src': 2, 'dst': 1, 'condition': None, 'callback': 'Factor', 'post': 'calc_sign', 'Finish': True},
                {'src': 0, 'dst': 3, 'condition': '-', 'callback': None, 'post': 'plast'},
                {'src': 3, 'dst': 1, 'condition': None, 'callback': 'Factor', 'post': 'calc_sign', 'Finish': True})

SignedFactor2 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Factor2', 'Finish': True,
                  'name': 'SignedFactor2', 'pre': 'null', 'post': 'calc_sign'},
                {'src': 0, 'dst': 2, 'condition': '+', 'callback': None, 'post': 'plast'},
                {'src': 2, 'dst': 1, 'condition': None, 'callback': 'Factor', 'Finish': True, 'post': 'calc_sign'},
                {'src': 0, 'dst': 3, 'condition': '-', 'callback': None, 'post': 'plast'},
                {'src': 3, 'dst': 1, 'condition': None, 'callback': 'Factor', 'Finish': True, 'post': 'calc_sign'})


Factor = ({'src': 0, 'dst': 1, 'condition': '(', 'callback': None, 'name': 'Factor'},
          {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Expr'},
          {'src': 2, 'dst': 3, 'condition': ')', 'callback': None, 'Finish': True},
          {'src': 0, 'dst': 4, 'condition': 'id', 'callback': None, 'post': 'plast'},
          {'src': 4, 'dst': 3, 'condition': None, 'callback': 'Fid3', 'Finish': True},
          {'src': 0, 'dst': 3, 'condition': 'num', 'callback': None, 'Finish': True, 'post': 'pnum'})

Factor2 = ({'src': 0, 'dst': 1, 'condition': '(', 'callback': None, 'name': 'Factor'},
          {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Expr'},
          {'src': 2, 'dst': 3, 'condition': ')', 'callback': None, 'Finish': True},
          {'src': 0, 'dst': 3, 'condition': 'num', 'callback': None, 'Finish': True, 'post': 'pnum'})

Fid3 = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Fid', 'name': 'Fid3', 'Finish': True,
         'post': 'calc_addr'},
          {'src': 0, 'dst': 2, 'condition': '(', 'callback': None},
          {'src': 2, 'dst': 3, 'condition': None, 'callback': 'Args'},
          {'src': 3, 'dst': 4, 'condition': ')', 'callback': None, 'Finish': True, 'post': 'func_jmp'})


Args = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'ArgList', 'name': 'Args', 'Finish': True},
        {'src': 0, 'dst': 1, 'condition': '', 'callback': None, 'Finish': True})

ArgList = ({'src': 0, 'dst': 1, 'condition': None, 'callback': 'Expr', 'name': 'ArgList', 'post': 'arg'},
           {'src': 1, 'dst': 2, 'condition': None, 'callback': 'ArgList_1', 'Finish': True})

ArgList_1 = ({'src': 0, 'dst': 1, 'condition': ',', 'callback': None, 'name': 'ArgList_1'},
             {'src': 1, 'dst': 2, 'condition': None, 'callback': 'Expr', 'post': 'arg'},
             {'src': 2, 'dst': 3, 'condition': None, 'callback': 'ArgList_1', 'Finish': True},
             {'src': 0, 'dst': 3, 'condition': '', 'callback': None, 'Finish': True})