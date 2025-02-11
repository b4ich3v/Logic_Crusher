import re


class Token:
    """
    A simple container for the type and value of a lexed token.
    For example: Token(AND, '&&') or Token(IDENTIFIER, 'A').
    """

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"
    
    def __eq__(self, other):
        return isinstance(other, Token) and self.type == other.type and self.value == other.value


class Lexer:
    """
    Responsible for converting a Boolean expression string into a list of tokens
    by matching against defined regular expression patterns.
    """

    def __init__(self, text):
        self.text = text
        self.token_specification = [
            ("NAND",       r"NAND\b|nand\b|!&|¬&|↑"),
            ("NOR",        r"NOR\b|nor\b|!v|¬∨|↓"), 
            ("AND",        r"AND\b|and\b|&&|&|∧"),       
            ("OR",         r"OR\b|or\b|\|\||\||∨"),     
            ("NOT",        r"NOT\b|not\b|!|~|¬"),
            ("XOR",        r"XOR\b|xor\b|\^|⊕"),     
            ("IMP",        r"IMP\b|imp\b|=>|→|⇒"),
            ("EQV",        r"EQV\b|eqv\b|<=>|↔|=="),
            ("LPAREN",     r"\("),
            ("RPAREN",     r"\)"),
            ("CONST",      r"1\b|0\b|true\b|false\b"),
            ("IDENTIFIER", r"[A-Za-z]+"),
            ("SKIP",       r"[ \t]+"),
            ("MISMATCH",   r".")
        ]

        # Build a single regex that alternates named groups for each token type
        self.token_regex = "|".join(
            f"(?P<{pair[0]}>{pair[1]})" for pair in self.token_specification
        )

    def tokenize(self):
        """
        Yields a list of Token objects based on the input text.
        Raises an exception if an invalid character is encountered.
        """
        tokens = []

        for token_match in re.finditer(self.token_regex, self.text):
            kind = token_match.lastgroup
            value = token_match.group(kind)

            if kind in {"IDENTIFIER", "CONST"}:
                tokens.append(Token(kind, value))
            elif kind in {
                "NOT", "AND", "OR",
                "XOR", "NAND", "NOR",
                "IMP", "EQV", "LPAREN", "RPAREN"
                }:
                tokens.append(Token(kind, value))
            elif kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise ValueError(
                    f"Invalid character {value!r} at position {token_match.start() + 1}")
            
        tokens.append(Token("EOF", None))
        return tokens
    
    def __iter__(self):
        return iter(self.tokenize())
