firsts = {
    'Program': ['EOF', 'int', 'void'],
    'DL1': ['int', 'void'],
    'FTS2': ['id'],
    'Dec': ['int', 'void'],
    'VarDec': ['int', 'void'],
    'Fid4': ['(', ';', '['],
    'FTS': ['id'],
    'Fid1': [';', '['],
    'FunDec': ['void', 'int'],
    'Params': ['void', 'int'],
    'FParam': ['id'],
    'FVoid': ['id'],
    'PL': ['void', 'int'],
    'PL1': [','],
    'Param': ['int', 'void'],
    'TS': ['int', 'void'],
    'FTS1': ['id'],
    'DL': ['int', 'void'],
    'SL1': ['num', 'id', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-', '('],
    'CompStmt': ['{'],
    'ExpStmt': ['num', 'id', 'continue', 'break', '+', '-', '('],
    'SelStmt': ['if'],
    'IterStmt': ['while'],
    'Fid2': ['['],
    'Stmt': ['num', 'id', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-', '('],
    'RetStmt': ['return'],
    'Fret': ['num', 'id', ';', '+', '-', '('],
    'SwitchStmt': ['switch'],
    'CaseStmts': ['case'],
    'CaseStmts_1': ['case'],
    'CaseStmt': ['case'],
    'DefaultStmt': ['default'],
    'SL': ['num', 'id', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-', '('],
    'FExpr': ['(', '[', '=', '*', '+', '-', '<', '=='],
    'FExpr1': ['=', '*', '+', '-', '<', '=='],
    'Var': ['id'],
    'SimplExpr': ['num', 'id', '+', '-', '('],
    'FAdditiveExpr': ['<', '=='],
    'Relop': ['<', '=='],
    'AdditiveExpr': ['num', 'id', '+', '-', '('],
    'AdditiveExpr_1': ['+', '-'],
    'Addop': ['+', '-'],
    'Term': ['num', 'id', '+', '-', '('],
    'Term_1': ['*'],
    'Term_2': ['num', '+', '-', '('],
    'SignedFactor': ['num', 'id', '+', '-', '('],
    'SignedFactor2': ['num', '+', '-', '('],
    'Factor': ['num', 'id', '('],
    'Args': ['num', 'id', '+', '-', '('],
    'ArgList': ['num', 'id', '+', '-', '('],
    'Expr': ['num', 'id', '+', '-', '('],
    'ArgList_1': [','],
    'Call': ['id'],
    'Factor2': ['(', 'num'],
    'Fid3': ['(', '['],
    'Fid': ['[']
}


follows = {
    'Program': ['eps'],
    'DL1': ['num', 'id', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
            '(', '}'],
    'DL': ['num', 'id',
           'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
           '(', '}'],
    'Dec': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
            'switch', '+', '-', '(', '}'],
    'FTS2': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
             'switch', '+', '-', '(', '}'],
    'Fid1': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
             'switch', '+', '-', '(', '}'],
    'VarDec': ['eps'],
    'Fid4': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
             'switch', '+', '-', '(', '}'],
    'FTS': ['eps'],
    'FunDec': ['eps'],
    'TS': ['id'],
    'Params': [')'],
    'FParam': [')'],
    'PL': ['eps'],
    'FVoid': [')'],
    'PL1': [')'],
    'Param': [')', ','],
    'FTS1': [')', ','],
    'Fid2': [')', ','],
    'CompStmt': ['num', 'id', 'case', 'default', 'else','int', 'void', 'EOF', 'continue', 'break', ';', '{',
                 'if', 'while', 'return', 'switch', '+', '-', '(', '}'],
    'Stmt': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
             'switch', '+', '-', '(', '}'],
    'ExpStmt': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
                'switch', '+', '-', '(', '}'],
    'SelStmt': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
                'switch', '+', '-', '(', '}'],
    'IterStmt': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
                 'switch', '+', '-', '(', '}'],
    'RetStmt': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
                'switch', '+', '-', '(', '}'],
    'Fret': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
             'switch', '+', '-', '(', '}'],
    'SwitchStmt': ['num', 'id', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return',
                   'switch', '+', '-', '(', '}'],
    'SL': ['case', 'default', '}'],
    'SL1': ['case', 'default', '}'],
    'CaseStmts': ['default', '}'],
    'CaseStmts_1': ['default', '}'],
    'CaseStmt': ['case', 'default', '}'],
    'DefaultStmt': ['}'],
    'FExpr': [';', ']', ')', ','],
    'FExpr1': [';', ']', ')', ','],
    'Var': ['eps'],
    'SimplExpr': ['eps'],
    'Expr': [';', ']', ')', ','],
    'Fid': ['=', '*', '+', '-', '<', '==', ';', ']', ')', ','],
    'FAdditiveExpr': [';', ']', ')', ','],
    'Relop': ['num', '+', '-', '(', 'id'],
    'AdditiveExpr': [';', ']', ')', ','],
    'AdditiveExpr_1': ['<', '==', ';', ']', ')', ','],
    'Addop': ['num', 'id', '+', '-', '('],
    'Term': ['+', '-', '<', '==', ';', ']', ')', ','],
    'Term_1': ['+', '-', '<', '==', ';', ']', ')', ','],
    'Term_2': ['+', '-', '<', '==', ';', ']', ')', ','],
    'SignedFactor': ['*', '+', '-', '<', '==', ';', ']', ')', ','],
    'SignedFactor2': ['*', '+', '-', '<', '==', ';', ']', ')', ','],
    'Factor': ['*', '+', '-', '<', '==', ';', ']', ')', ','],
    'Factor2': ['*', '+', '-', '<', '==', ';', ']', ')', ','],
    'Fid3': ['*', '+', '-', '<', '==', ';', ']', ')', ','],
    'Args': [')'],
    'ArgList': [')'],
    'ArgList_1': [')'],
    'Call': ['eps'],
}

nullables = ['DL1', 'FParam', 'PL', 'PL1', 'Fid2', 'DL', 'SL1', 'CaseStmts', 'CaseStmts_1', 'DefaultStmt',
             'SL', 'FExpr', 'FExpr1', 'FAdditiveExpr', 'AdditiveExpr_1', 'Term_1', 'Fid3', 'Fid', 'Args',
             'ArgList_1']

error_messages = {
    'Program': 'Give a correct program.',
    'DL': 'Decleration is not correct.',
    'DL1': 'Decleration is not correct.',
    'Dec': 'Decleration is not correct.',
    'FTS2': 'Type specification is not correct.',
    'FTS': 'Type specification is not correct.',
    'FID1': 'Type specification is not correct.',
    'Params': 'Parameter specification is not correct.',
    'FVoid': 'Void is not used correct.',
    'PL1': 'Parameter list specification is not correct.',
    'Param': 'Parameter specification is not correct.',
    'FTS1': 'Type specification is not correct.',
    'FID2': 'ID is not correct.',
    'CompStmt': 'Statement specification is not correct.',
    'SL': 'Statement specification is not correct.',
    'SL1': 'Statement specification is not correct.',
    'Stmt': 'Statement specification is not correct.',
    'ExpStmt': 'Expression specification is not correct.',
    'SelStmt': 'Statement specification is not correct.',
    'IterStmt': 'Statement specification for loop is not correct.',
    'RetStmt': 'Statement specification for return is not correct.',
    'Fret': 'Statement specification for return is not correct.',
    'SwitchStmt': 'Statement specification for switch is not correct.',
    'CaseStmts': 'Statement specification for case is not correct.',
    'CaseStmts_1': 'Statement specification for case is not correct.',
    'CaseStmt': 'Statement specification for case is not correct.',
    'DefaultStmt': 'Statement specification for default is not correct.',
    'Expr': 'Statement specification for expression is not correct.',
    'Var': 'Variable usage is not correct.',
    'FID': 'ID specification is not correct.',
    'SimpleExpr': 'Expression is not correct.',
    'FAdditiveExpr': 'Expression is not correct.',
    'Relop': 'Expression is not correct.',
    'AdditiveExpr': 'Algebraic expression is not correct.',
    'AdditiveExpr_1': 'Algebraic expression is not correct.',
    'Addop': 'Algebraic expression for sum and minus is not correct.',
    'Term': 'Algebraic expression for sum and minus is not correct.',
    'Term_1': 'Algebraic expression for product is not correct.',
    'SignedFactor': 'Algebraic expression for is not correct.',
    'Factor': 'Algebraic expression is not correct.',
    'Call': 'Calling is not correct.',
    'Args': 'Argument expression is not correct.',
    'ArgList': 'Argument expression is not correct.',
    'ArgList_1': 'Argument expression is not correct.',
}
