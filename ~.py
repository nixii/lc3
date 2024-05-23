'''

for i, token in enumerate(self.tokens):

    # Set the correct value
    if token[0] == TokenType.LABEL:
        if i != 0:
            if command != '':
                args.append((ParserArgType.LABEL, token[1]))
            else:
                err = 'Cannot set the label late!'
                break
        if not label:
            label = token[1]
        else:
            err = 'Cannot set a label twice in one line!'
            break
    elif token[0] == TokenType.OPCODE:
        if not command:
            command = token[1]
        else:
            err = 'Cannot set a command twice in one line!'
            break
    elif token[0] == TokenType.OPERANDS:
        print(args)
        if len(args) == 0 or len(args) == 1:
            str_args = token[1].split(',')
            _args, err = self.clean_args(str_args)
            if not err:
                args += _args
        else:
            err = 'Operands cannot come in two groups!'
            break
    
# Set all the values
self.label = label
self.command = command
self.args = args
self.error = err

# Other errors
if not err:
    if command == '' and len(self.tokens) != 0:
        err = 'You need a command!'
        self.error = err

'''