
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
        self.advance()

    def advance(self: 'Lexer') -> None:
        self.pos += 1
        self.current_character = self.text[self.pos] if len(self.text) > self.pos else ''
    
    def build_identifier(self: 'Lexer') -> tuple[int, str]:
        iden = self.current_character
        self.advance()
        while not self.current_character.isspace() and not self.current_character == '':
            iden += self.current_character
            self.advance()
    
        if iden in OPCODES:
            return (TokenType.OPCODE, iden)
        elif ',' in iden:
            return (TokenType.OPERANDS, iden)

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
PARSER OBJECT

This is a line of code from the parser that the interpreter can run.
'''
class ParserObject():
    def __init__(self: 'ParserObject', tokens: list[(int, str)]) -> None:
        self.tokens = tokens

        self.load_commands()
    
    def load_commands(self: 'ParserObject') -> None:
        pass

'''
PARSER

This will make the syntax correct.
'''
class Parser():
    pass

'''
MAIN

Run the program.
'''
def main() -> None:
    l = Lexer(input('$ '))

    tokens, error = l.lex()
    if error is not None:
        raise Exception(error)

'''
AAAAAAA

Fun Python syntax
'''
if __name__ == '__main__':
    main()