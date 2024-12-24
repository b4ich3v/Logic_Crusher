import re

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
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

        self.token_regex = '|'.join(
            f"(?P<{pair[0]}>{pair[1]})" for pair in self.token_specification)

    def tokenize(self):
        tokens = []
        for mo in re.finditer(self.token_regex, self.text):
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == "IDENTIFIER" or kind == "CONST":
                tokens.append(Token(kind, value))
            elif kind in ("NOT", "AND", "OR", "XOR", "NAND", "NOR", "IMP", "EQV", "LPAREN", "RPAREN"):
                tokens.append(Token(kind, value))
            elif kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise Exception(
                    f"Invalid character {value!r} at position {mo.start() + 1}")
        tokens.append(Token("EOF", None))
        return tokens