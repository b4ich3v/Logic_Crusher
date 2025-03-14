from ast_nodes.nodes import (
    EqvNode, ImpNode, OrNode, NorNode, 
    XorNode, AndNode, NandNode, NotNode, 
    VariableNode, ConstNode
)


class Parser:
    """
    Parses a list of tokens (from the Lexer) into an abstract syntax tree (AST).
    Implements a recursive descent parser for Boolean expressions.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]

    def eat(self, token_type):
        """
        Consume the current token if it matches the expected type,
        otherwise raise an exception.
        """
        if self.current_token.type == token_type:
            self.position += 1
            self.current_token = self.tokens[self.position]
        else:
            raise ValueError(
                f"Expected token {token_type} but received {self.current_token.type} at position {self.position + 1}"
            )

    def parse(self):
        """
        Initiates parsing and returns the root of the resulting AST.
        Raises an exception if tokens remain after a complete parse.
        """
        node = self.expr()

        if self.current_token.type != "EOF":
            raise ValueError(f"Unexpected token {self.current_token.type} at position {self.position + 1}")
        return node

    def expr(self):
        return self.equiv_expr()

    def equiv_expr(self):
        node = self.imp_expr()

        while self.current_token.type == "EQV":
            self.eat("EQV")
            node = EqvNode(node, self.imp_expr())

        return node

    def imp_expr(self):
        node = self.or_expr()

        while self.current_token.type == "IMP":
            self.eat("IMP")
            node = ImpNode(node, self.or_expr())

        return node

    def or_expr(self):
        node = self.xor_expr()

        while self.current_token.type in {"OR", "NOR"}:
            op = self.current_token.type
            self.eat(op)
            node = OrNode(node, self.xor_expr()) if op == "OR" else NorNode(node, self.xor_expr())

        return node

    def xor_expr(self):
        node = self.and_expr()

        while self.current_token.type == "XOR":
            self.eat("XOR")
            node = XorNode(node, self.and_expr())

        return node

    def and_expr(self):
        node = self.nand_expr()

        while self.current_token.type in ("AND",):
            self.eat("AND")
            node = AndNode(node, self.nand_expr())

        return node

    def nand_expr(self):
        node = self.factor()

        while self.current_token.type == "NAND":
            self.eat("NAND")
            node = NandNode(node, self.factor())

        return node

    def factor(self):
        token = self.current_token
        
        if token.type == "NOT":
            self.eat("NOT")
            node = NotNode(self.factor())
            return node
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return VariableNode(token.value)
        elif token.type == "CONST":
            self.eat("CONST")
            value = True if token.value.lower() in {"1", "true"} else False
            return ConstNode(value)
        elif token.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expr()
            self.eat("RPAREN")
            return node
        
        raise ValueError(f"Unexpected token {token.type} at position {self.position + 1}")
