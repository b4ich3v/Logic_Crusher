from parser_lexer.lexer import Lexer
from parser_lexer.parser import Parser


class Validator:
    """
    Provides a static method for validating whether a given Boolean expression
    can be successfully parsed by the Lexer and Parser.
    """

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
