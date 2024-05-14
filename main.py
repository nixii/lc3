
'''
CONSTANTS

Just constant variables
'''
OPCODES = 'ADD AND NOT OR LDR STR HALT LDI STI BRz BR BRn BRp'.split(' ')
LABELS = []

'''
TOKENS

This is just the token objects.
'''
class TokenType():
    LABEL = 0
    OPCODE = 1
    OPERANDS = 2

'''
LEXER

This turns the text into tokens
'''
class Lexer():

    # Initialize the lexer
    def __init__(self: 'Lexer', text: str) -> None:
        self.set_text(text)

    # Set the text object so the lexer is reusable
    def set_text(self: 'Lexer', text: str) -> None:
        self.text = text
        self.pos = -1
        self.current_character = ''
        self.last_character = ''
        self.advance()

    # Advance to the next character
    def advance(self: 'Lexer') -> None:
        self.pos += 1
        self.last_character = self.current_character
        self.current_character = self.text[self.pos] if len(self.text) > self.pos else ''
    
    # Create an identifier
    def build_identifier(self: 'Lexer') -> tuple[int, str]:
        iden = self.current_character
        self.advance()

        # While it is one identifier
        while not self.current_character.isspace() and not self.current_character == '':
            iden += self.current_character
            self.advance()
        
        # You need commas by themselves
        if self.last_character == ',':
            return None, 'Commas cannot be followed by spaces!'
    
        # Make sure to return the correct type
        if iden in OPCODES and not iden[0] in 'xb#':
            return (TokenType.OPCODE, iden), None
        elif ',' in iden or iden[0] in 'xb#':
            return (TokenType.OPERANDS, iden), None

        # If it is a label that is taken
        if iden in LABELS:
            return None, 'Label already taken!'
        
        # Return the label
        LABELS.append(iden)
        return (TokenType.LABEL, iden), None
    
    # Lex the text
    def lex(self: 'Lexer') -> list[(int, str)]:
        tokens = []

        # While there is a character
        while self.current_character != '':

            # Ignore spaces
            if self.current_character.isspace():
                continue

            # If it is a letter, build an identifier
            elif self.current_character in 'abcdefghijklmnopqrstuvwxyz'.upper() + 'abcdefghijklmnopqrstuvwxyz':
                tkn, error = self.build_identifier()
                if error:
                    return None, error
                tokens.append(tkn)
            
            # Semicolons are comments
            elif self.current_character == ';':
                break
            
            # Error if there is a bad character
            else:
                return None, 'Unexpected character!'
            
            # Advance
            self.advance()
        
        # Return the tokens
        return tokens, None

'''
PARSER ARG TYPE

This is the type for an operand.
'''
class ParserArgType():
    NUMBER = 0
    REGISTER = 1
    ADDRESS = 2

'''
PARSER OBJECT

This is a line of code from the parser that the interpreter can run.
'''
class ParserObject():

    # Initialize a new parser object
    def __init__(self: 'ParserObject', tokens: list[(int, str)]) -> None:
        self.tokens = tokens

        self.load_commands()
    
    # Clean the args into a usable format
    @staticmethod
    def clean_args(str_args: list[str]) -> list[(int, str|int)]:
        args = []

        # For each argument
        for arg in str_args:

            # Hex numbers
            if arg[0] == 'x':
                args.append((ParserArgType.NUMBER, int('0' + arg, 16)))

            # Decimal numbers
            elif arg[0] == '#':
                args.append((ParserArgType.NUMBER, int(arg[1:])))
            
            # Binary numbers
            elif arg[0] == 'b':
                args.append((ParserArgType.NUMBER, int('0' + arg, 2)))
            
            # Registers
            elif arg[0] == 'R':
                args.append((ParserArgType.REGISTER, arg[1:]))
            
            # Errors
            else:
                return None, f'Invalid operand type "{arg[0]}".'

        # Return the args
        return args, None
    
    def load_commands(self: 'ParserObject') -> None:

        # Get defaults
        label = ''
        command = ''
        args = []
        err = None

        # For each token
        for i, token in enumerate(self.tokens):

            # Set the correct value
            if token[0] == TokenType.LABEL:
                if i != 0:
                    err = 'Labels must come first!'
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
                if not args:
                    str_args = token[1].split(',')
                    args, err = self.clean_args(str_args)
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
            if command == '':
                err = 'You need a command!'
                self.error = err
    
    # For debugging
    def __repr__(self: 'ParserObject') -> str:
        return f'Label: {self.label}; Opcode: {self.command}; Operands: {self.args};'

'''
PARSER

This will make the syntax correct.
'''
class Parser():

    # Create a parser
    def __init__(self: 'Parser', tokens: list[(int, str)]) -> None:
        self.tokens = tokens
    
    # Set the tokens for the parser
    def set_tokens(self: 'Parser', tokens: list[(int, str)]) -> None:
        self.tokens = tokens

    # Parse the line
    def parse(self: 'Parser') -> ParserObject:
        po = ParserObject(self.tokens)
        if po.error:
            return None, po.error
        return po, None

'''
INTERPRETER

This will interpret the entire program.
'''
class Interpreter():
    def __init__(self: 'Interpreter', parser_object: ParserObject) -> None:
        self.parser_object = parser_object

'''
MAIN

Run the program.
'''
def main() -> None:

    # Lexerification
    l = Lexer(input('$ '))

    tokens, error = l.lex()
    if error is not None:
        raise Exception(error)
    
    # Parserification
    p = Parser(tokens)

    po, error = p.parse()
    if error is not None:
        raise Exception(error)
    print(repr(po))

    # Interpreterification

'''
AAAAAAA

Fun Python syntax
'''
if __name__ == '__main__':
    main()