class Util:
    @classmethod
    def read(cls, file_name):
        with open(file_name + '.c', 'r') as content_file:
            content = content_file.read()
        return content


file = Util.read('file')
unread_parts = file
line_num = 1
errors = {}
tokens = {}
# except for = and ==
symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '<', '>', '\'']
keywords = ['if', 'else', 'void', 'int', 'while', 'break', 'continue', 'switch', 'default', 'case', 'return', 'float']
spaces = [' ', '\n', '\t']


def report():
    global tokens, errors
    with open('lexical_errors.txt', 'w+') as errors_file:
        for i in errors.keys():
            errors_file.write('{}. '.format(i))
            for v in errors[i]:
                errors_file.write('{}'.format(v))
            errors_file.write('\n')

    with open('scanner.txt', 'w+') as tokens_file:
        for i in tokens.keys():
            tokens_file.write('{}. '.format(i))
            for v in tokens[i]:
                tokens_file.write('{}'.format(v))
            tokens_file.write('\n')


def omit_start(token_type, token_len):
    global unread_parts
    token = unread_parts[:token_len]
    unread_parts = unread_parts[token_len:]
    return token_type, token


def get_next_token():
    global line_num, unread_parts
    if len(unread_parts) == 0:
        return 'EOF', 'EOF'
    if unread_parts[0].isspace():
        for i in range(len(unread_parts)):
            if not unread_parts[i].isspace():
                return omit_start('WHITESPACE', i)
            elif unread_parts[i] == '\n':
                line_num += 1
    if unread_parts[0] == '/':
        if len(unread_parts) > 1 and unread_parts[1] == '/':
            for i in range(len(unread_parts)):
                if unread_parts[i] == '\n':
                    return omit_start('COMMENT', i)
            return 'COMMENT', unread_parts
        elif unread_parts[1] == '*':
            for i in range(len(unread_parts)):
                if unread_parts[i] == '*' and i + 1 < len(unread_parts) and unread_parts[i + 1] == '/':
                    return omit_start('COMMENT', i + 2)
            # not sure of it
            return 'UNFINISHED_COMMENT_ERROR', unread_parts
        return omit_start('SYMBOL', 1)
    if unread_parts[0] == '=':
        if len(unread_parts) > 1 and unread_parts[1] == '=':
            return omit_start('SYMBOL', 2)
        return omit_start('SYMBOL', 1)
    if unread_parts[0] in symbols:
        return omit_start('SYMBOL', 1)
    if unread_parts[0].isalpha():
        length = len(unread_parts)
        for i in range(len(unread_parts)):
            if not unread_parts[i].isalnum():
                if unread_parts[i] in symbols + spaces:
                    length = i
                    break
                else:
                    return omit_start('ERROR', i + 1)
        if unread_parts[:length] in keywords:
            return omit_start('KEYWORD', length)
        else:
            return omit_start('ID', length)
    if unread_parts[0].isnumeric():
        for i in range(len(unread_parts)):
            if not unread_parts[i].isnumeric():
                if unread_parts[i] in symbols + spaces:
                    return omit_start('NUM', i)
                else:
                    return omit_start('ERROR', i + 1)
    if unread_parts[0] in spaces:
        return omit_start('WHITESPACE', 1)
    return omit_start('ERROR', 1)


while True:
    token = get_next_token()
    if token[0] == 'EOF':
        break
    if token[0].endswith('ERROR'):
        if line_num in errors.keys():
            errors[line_num] += ' (' + token[1] + ', invalid input)'
        else:
            errors[line_num] = '(' + token[1] + ', invalid input)'
    else:
        if token[0] == 'WHITESPACE' or token[0] == 'COMMENT':
            continue
        if line_num in tokens.keys():
            tokens[line_num] += ' (' + token[0] + ', ' + token[1] + ')'
        else:
            tokens[line_num] = '(' + token[0] + ', ' + token[1] + ')'


report()
