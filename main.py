
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
    def __init__(self: 'Lexer', text: str) -> None:
        self.set_text(text)

    def set_text(self: 'Lexer', text: str) -> None:
        self.text = text
        self.pos = -1
        self.current_character = ''
        self.last_character = ''
        self.advance()

    def advance(self: 'Lexer') -> None:
        self.pos += 1
        self.last_character = self.current_character
        self.current_character = self.text[self.pos] if len(self.text) > self.pos else ''
    
    def build_identifier(self: 'Lexer') -> tuple[int, str]:
        iden = self.current_character
        self.advance()
        while not self.current_character.isspace() and not self.current_character == '':
            iden += self.current_character
            self.advance()
        
        if self.last_character == ',':
            return None, 'Commas cannot be followed by spaces!'
    
        if iden in OPCODES:
            return (TokenType.OPCODE, iden), None
        elif ',' in iden:
            return (TokenType.OPERANDS, iden), None

        if iden in LABELS:
            return None, 'Label already taken!'
        
        LABELS.append(iden)
        return (TokenType.LABEL, iden), None
    
    def lex(self: 'Lexer') -> list[(int, str)]:
        tokens = []
        while self.current_character != '':
            if self.current_character.isspace():
                continue
            elif self.current_character in 'abcdefghijklmnopqrstuvwxyz'.upper():
                tkn, error = self.build_identifier()
                if error:
                    return None, error
                tokens.append(tkn)
            elif self.current_character == ';':
                break
            else:
                return None, 'Unexpected character!'
            
            self.advance()
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
    def __init__(self: 'ParserObject', tokens: list[(int, str)]) -> None:
        self.tokens = tokens

        self.load_commands()
    
    @staticmethod
    def clean_args(str_args: list[str]) -> list[(int, str|int)]:
        args = []
        for arg in str_args:
            if arg[0] == 'x':
                args.append((ParserArgType.NUMBER, int('0' + arg, 16)))
            elif arg[0] == 'R':
                args.append((ParserArgType.REGISTER, arg[1:]))
            else:
                return None, f'Invalid operand type "{arg[0]}".'
        return args, None
    
    def load_commands(self: 'ParserObject') -> None:
        label = ''
        command = ''
        args = []
        err = None
        for token in self.tokens:
            if token[0] == TokenType.LABEL and not label:
                label = token[1]
            elif token[0] == TokenType.OPCODE and not command:
                command = token[1]
            elif token[0] == TokenType.OPERANDS and not args:
                str_args = token[1].split(',')
                args, err = self.clean_args(str_args)
        self.label = label
        self.command = command
        self.args = args
        self.error = err
                
    def __repr__(self: 'ParserObject') -> str:
        return f'Label: {self.label}; Opcode: {self.command}; Operands: {self.args};'

'''
PARSER

This will make the syntax correct.
'''
class Parser():
    def __init__(self: 'Parser', tokens: list[(int, str)]) -> None:
        self.tokens = tokens
    
    def set_tokens(self: 'Parser', tokens: list[(int, str)]) -> None:
        self.tokens = tokens
    
    def parse(self: 'Parser') -> ParserObject:
        po = ParserObject(self.tokens)
        if po.error:
            return None, po.error
        return po, None

'''
MAIN

Run the program.
'''
def main() -> None:
    l = Lexer(input('$ '))

    tokens, error = l.lex()
    if error is not None:
        raise Exception(error)
    
    p = Parser(tokens)

    po, error = p.parse()
    if error is not None:
        raise Exception(error)
    print(repr(po))

'''
AAAAAAA

Fun Python syntax
'''
if __name__ == '__main__':
    main()