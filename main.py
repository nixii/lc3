'''
IMPORTS

Some libraries I need
'''
import sys

'''
CONSTANTS

Just constant variables
'''
OPCODES = 'ADD SUB AND NOT OR LDR STR LDI STI BRz BR BRn BRp TRAP HALT IN OUT GETC PUTS .ORIG .END .BLKW .FILL .STRINGZ'.split(' ')
TRAPCODES = {
    'HALT': 0x25,
    'IN': 0x23,
    'OUT': 0x21,
    'GETC': 0x20,
    'PUTS': 0x22
}
TRAPCODE_LIST = list(TRAPCODES.keys())
LABELS = []

'''
TOKENS

This is just the token objects.
'''
class TokenType():
    LABEL = 0
    OPCODE = 1
    OPERANDS = 2
    LABEL_REF = 3

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
        elif ',' in iden or iden[0] in 'Rxb#' or iden in LABELS or self.pos <= len(iden):
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
        if len(self.text) == 0 or self.text[0] == ';' or self.text[0] == '\n':
            return [], None

        # While there is a character
        while self.current_character != '':

            # Ignore spaces
            if self.current_character.isspace():
                self.advance()
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
    LABEL = 3

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
                if arg in LABELS:
                    args.append((ParserArgType.LABEL, arg))
                # else:
                #     return None, f'Invalid operand type "{arg[0]}".'

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
GLOBAL ENVIRONMENT

The environment that the program runs in
'''
class ProgramEnvironment():
    def __init__(self: 'ProgramEnvironment') -> None:
        self.registers = {
            f'R{i}': 0 for i in range(10)
        }
        self.memory = {

        }
        self.lines = []
        self.labels = {}
        self.last_value = 0
    
    def get_register(self: 'ProgramEnvironment', register_id: int) -> tuple[int|None, str|None]:
        val = self.registers.get(f'R{register_id}', None)
        return val, 'Register doesn\'t exist!' if val is None else None
    def set_register(self: 'ProgramEnvironment', register_id: int, register_value: int) -> str|None:
        if self.registers.get(f'R{register_id}', None) == None:
            return 'Register doesn\'t exist!'
        self.registers[f'R{register_id}'] = register_value
        return None
    
    def get_memory(self: 'ProgramEnvironment', address: int) -> int:
        val = self.memory.get(str(address))
        return val or 0x0000
    def set_memory(self: 'ProgramEnvironment', address: int, val: int) -> None:
        self.memory.set(str(address), val)
    
    def get_value_of(self: 'ProgramEnvironment', o: tuple[int, str]) -> int:
        if o[0] == ParserArgType.NUMBER:
            return int(o[1])
        elif o[0] == ParserArgType.REGISTER:
            val, err = self.get_register(int(o[1]))
            if err: raise Exception(err)
            return val
        return 0

    def add_line(self: 'ProgramEnvironment', line: ParserObject) -> None:
        self.lines.append(line)
        if line.label:
            self.labels[line.label] = len(self.lines) - 1

'''
INTERPRETER

This will interpret the entire program.
'''
class Interpreter():
    def __init__(self: 'Interpreter', parser_object: ParserObject) -> None:
        self.parser_object = parser_object
        self.env = ProgramEnvironment()

    def set_parser_object(self: 'Interpreter', parser_object: ParserObject) -> None:
        self.parser_object = parser_object

    def command_void(self: 'Interpreter') -> None:
        raise Exception('Unknown command!')

    def command_ADD(self: 'Interpreter', sign: int = 1) -> None:
        arg_0 = self.parser_object.args[0]
        arg_1 = self.parser_object.args[1]
        arg_2 = self.parser_object.args[2]
        val = self.env.get_value_of(arg_0)
        val += self.env.get_value_of(arg_1) * sign
        if arg_2[0] != ParserArgType.REGISTER:
            raise Exception('Expected a register to return the value into.')
        err = self.env.set_register(arg_2[1], val)
        if err:
            raise Exception(err)
        self.env.last_value = val
    
    def command_NOT(self: 'Interpreter') -> None:
        arg_0 = self.parser_object.args[0]
        arg_1 = self.parser_object.args[1]
        val = ~self.env.get_value_of(arg_0)
        if arg_1[0] != ParserArgType.REGISTER:
            raise Exception('Expected a register to return the value into.')
        err = self.env.set_register(arg_1[1], val)
        if err:
            raise Exception(err)
        self.env.last_value = val
    
    def command_BR(self: 'Interpreter') -> int:
        arg_0 = self.parser_object.args[0]
        if arg_0[0] != ParserArgType.LABEL or not arg_0[1] in LABELS:
            raise Exception('Expected a label to go to!')
        return self.env.labels[arg_0[1]]
    
    def command_BRp(self: 'Interpreter') -> int|None:
        if self.env.last_value > 0:
            return self.command_BR()
    def command_BRn(self: 'Interpreter') -> int|None:
        if self.env.last_value < 0:
            return self.command_BR()
    def command_BRz(self: 'Interpreter') -> int|None:
        print(self.env.last_value)
        if self.env.last_value == 0:
            return self.command_BR()
        
    def command_SUB(self: 'Interpreter') -> None:
        self.command_ADD(-1)
    
    def interpret(self: 'Interpreter') -> int|None:
        if self.parser_object.command == '':
            return
        return getattr(self, f'command_{self.parser_object.command}', 'command_void')()
    
    def register(self: 'Interpreter', line: ParserObject) -> None:
        self.env.add_line(line)

'''
MAIN

Run the program.
'''

def reg_run(t: str, l: Lexer, p: Parser, i: Interpreter) -> None:
    l.set_text(t)
    tokens, error = l.lex()
    if error is not None:
        raise Exception(error)
    
    # Parserification
    p.set_tokens(tokens)
    po, error = p.parse()
    if error is not None:
        raise Exception(error)
    print(po)
    
    # Interpreterification
    i.register(po)

def run(l: Lexer, p: Parser, i: Interpreter) -> None:
    j = 0
    while j < len(i.env.lines):
        line = i.env.lines[j]
        i.set_parser_object(line)
        res = i.interpret()
        j = j if res is None else res
        j += 1

def main() -> None:

    # Lexerification
    l = Lexer('')
    p = Parser(None)
    i = Interpreter(None)

    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            lines = list(map(lambda x: x.replace('\n', ''), f.readlines()))
            lines = filter(lambda x: x != '' and not x.isspace() and x != '\n' and x[0] != ';', lines)
            for line in lines:
                reg_run(line, l, p, i)
            run(l, p, i)
    print(i.env.registers)

'''
RUN

Fun Python syntax
'''
if __name__ == '__main__':
    main()