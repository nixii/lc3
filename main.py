
OPCODES = 'ADD AND NOT OR LDR STR HALT LDI STI BRz BR BRn BRp'.split(' ')

class TokenType():
    LABEL = 0
    OPCODE = 1
    OPERANDS = 2

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
        
        if iden.upper() in OPCODES:
            return (TokenType.OPCODE, iden)
        elif ',' in iden:
            return (TokenType.OPERANDS, iden)
        return (TokenType.LABEL, iden)
    
    def lex(self: 'Lexer') -> list[(int, str)]:
        tokens = []
        while self.current_character != '':
            if self.current_character.isspace():
                continue
            elif self.current_character in 'abcdefghijklmnopqrstuvwxyz'.upper():
                tokens.append(self.build_identifier())
            elif self.current_character == ';':
                break
            else:
                return None, 'Unexpected character!'
            
            self.advance()
        return tokens, None

def main() -> None:
    l = Lexer(input('$ '))

    tokens, error = l.lex()
    if error is not None:
        raise Exception(error)

if __name__ == '__main__':
    main()