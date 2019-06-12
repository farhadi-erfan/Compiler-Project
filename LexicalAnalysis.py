class Util:
    @classmethod
    def read(cls, file_name):
        with open('in_out/' + file_name + '.c', 'r') as content_file:
            content = content_file.read()
        return content


# except for = and ==
symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '<', '>', '\'']
keywords = ['if', 'else', 'void', 'int', 'while', 'break', 'continue', 'switch', 'default', 'case', 'return', 'float']
spaces = [' ', '\n', '\t']


class LexicalAnalyzer:
    def __init__(self):
        self.line_num = 1
        self.file = Util.read('sample')
        self.unread_parts = self.file
        self.errors, self.tokens = {}, {}

    def omit_start(self, token_type, token_len):
        token = self.unread_parts[:token_len]
        self.unread_parts = self.unread_parts[token_len:]
        return token_type, token

    def get_next_token_lexical(self):
        if len(self.unread_parts) == 0:
            return 'EOF', 'EOF'
        if self.unread_parts[0].isspace():
            for i in range(len(self.unread_parts)):
                if not self.unread_parts[i].isspace():
                    return self.omit_start('WHITESPACE', i)
                elif self.unread_parts[i] == '\n':
                    self.line_num += 1
        if self.unread_parts[0] == '/':
            if len(self.unread_parts) > 1 and self.unread_parts[1] == '/':
                for i in range(len(self.unread_parts)):
                    if self.unread_parts[i] == '\n':
                        return self.omit_start('COMMENT', i)
                return 'COMMENT', self.unread_parts
            elif self.unread_parts[1] == '*':
                for i in range(len(self.unread_parts)):
                    if self.unread_parts[i] == '*' and i + 1 < len(self.unread_parts) and self.unread_parts[i + 1] == '/':
                        return self.omit_start('COMMENT', i + 2)
                # not sure of it
                return 'UNFINISHED_COMMENT_ERROR', self.unread_parts
            return self.omit_start('SYMBOL', 1)
        if self.unread_parts[0] == '=':
            if len(self.unread_parts) > 1 and self.unread_parts[1] == '=':
                return self.omit_start('SYMBOL', 2)
            return self.omit_start('SYMBOL', 1)
        if self.unread_parts[0] in symbols:
            return self.omit_start('SYMBOL', 1)
        if self.unread_parts[0].isalpha():
            length = len(self.unread_parts)
            for i in range(len(self.unread_parts)):
                if not self.unread_parts[i].isalnum():
                    if self.unread_parts[i] in symbols + spaces:
                        length = i
                        break
                    else:
                        return self.omit_start('ERROR', i + 1)
            if self.unread_parts[:length] in keywords:
                return self.omit_start('KEYWORD', length)
            else:
                return self.omit_start('ID', length)
        if self.unread_parts[0].isnumeric():
            for i in range(len(self.unread_parts)):
                if not self.unread_parts[i].isnumeric():
                    if self.unread_parts[i] in symbols + spaces or self.unread_parts[i].isalpha():
                        return self.omit_start('NUM', i)
                    else:
                        return self.omit_start('ERROR', i + 1)
        if self.unread_parts[0] in spaces:
            return self.omit_start('WHITESPACE', 1)
        return self.omit_start('ERROR', 1)

# la = LexicalAnalyzer()
# # lexical analysis
# while True:
#     token = la.get_next_token_lexical()
#     if token[0].endswith('ERROR'):
#         if la.line_num in la.errors.keys():
#             la.errors[la.line_num] += ' (' + token[1] + ', invalid input)'
#         else:
#             la.errors[la.line_num] = '(' + token[1] + ', invalid input)'
#     else:
#         if token[0] == 'WHITESPACE' or token[0] == 'COMMENT':
#             continue
#         if la.line_num in la.tokens.keys():
#             la.tokens[la.line_num] += ' (' + token[0] + ', ' + token[1] + ')'
#             # la.tokens[la.line_num] += [token]
#         else:
#             la.tokens[la.line_num] = '(' + token[0] + ', ' + token[1] + ')'
#             # la.tokens[la.line_num] = [token]
#         if token[0] == 'EOF':
#             break