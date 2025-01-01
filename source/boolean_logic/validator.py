from parser_lexer.lexer import Lexer
from parser_lexer.parser import Parser

class Validator:
    @staticmethod
    def validate(expression):
        try:
            lexer = Lexer(expression)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            parser.parse()
            return True, None
        except Exception as e:
            return False, str(e)
