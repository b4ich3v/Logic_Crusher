from boolean_logic.helpers import *

class Node:
    def simplify(self):
        return self

    def evaluate(self, env):
        pass

    def to_zhegalkin(self, variables):
        pass

    def __eq__(self, other):
        return isinstance(other, Node) and self.__dict__ == other.__dict__

    def substitute(self, env):
        return self

    def to_graphviz(self, dot, counter):
        pass


class VariableNode(Node):
    def __init__(self, name):
        self.name = name

    def simplify(self):
        return self

    def evaluate(self, env):
        return env[self.name]

    def to_zhegalkin(self, variables):
        index = variables.index(self.name)
        monomial = 1 << index
        return {monomial}

    def substitute(self, env):
        if self.name in env and env[self.name] is not None:
            return ConstNode(env[self.name])
        else:
            return self

    def __str__(self):
        return self.name

    def to_graphviz(self, dot, counter):
        node_id = str(id(self))
        dot.node(node_id, self.name)

        return node_id


class ConstNode(Node):
    def __init__(self, value):
        self.value = value

    def simplify(self):
        return self

    def evaluate(self, env):
        return self.value

    def to_zhegalkin(self, variables):
        return {0} if self.value else set()

    def substitute(self, env):
        return self

    def __str__(self):
        return "1" if self.value else "0"

    def to_graphviz(self, dot, counter):
        node_id = str(id(self))
        label = "1" if self.value else "0"
        dot.node(node_id, label)
        return node_id


class NotNode(Node):
    def __init__(self, operand):
        self.operand = operand

    def simplify(self):
        operand = self.operand.simplify()
        if isinstance(operand, NotNode):
            return operand.operand
        if isinstance(operand, ConstNode):
            return ConstNode(not operand.value)
        return NotNode(operand)

    def evaluate(self, env):
        return not self.operand.evaluate(env)

    def to_zhegalkin(self, variables):
        operand_poly = self.operand.to_zhegalkin(variables)
        one_poly = {0} 
        return add_polynomials(one_poly, operand_poly)

    def substitute(self, env):
        new_operand = self.operand.substitute(env)
        return NotNode(new_operand).simplify()

    def __str__(self):
        return f"NOT {self.operand}"

    def to_graphviz(self, dot, counter):
        node_id = str(id(self))
        dot.node(node_id, "NOT")
        child_id = self.operand.to_graphviz(dot, counter)
        dot.edge(node_id, child_id)
        return node_id


class AndNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, ConstNode):
            return right if left.value else ConstNode(False)
        if isinstance(right, ConstNode):
            return left if right.value else ConstNode(False)

        if left == right:
            return left

        return AndNode(left, right)

    def evaluate(self, env):
        return self.left.evaluate(env) and self.right.evaluate(env)

    def to_zhegalkin(self, variables):
        left_poly = self.left.to_zhegalkin(variables)
        right_poly = self.right.to_zhegalkin(variables)
        return multiply_polynomials(left_poly, right_poly)

    def substitute(self, env):
        new_left = self.left.substitute(env)
        new_right = self.right.substitute(env)
        return AndNode(new_left, new_right).simplify()

    def __str__(self):
        return f'({self.left} AND {self.right})'

    def to_graphviz(self, dot, counter):
        node_id = str(id(self))
        dot.node(node_id, 'AND')
        left_id = self.left.to_graphviz(dot, counter)
        right_id = self.right.to_graphviz(dot, counter)
        dot.edge(node_id, left_id)
        dot.edge(node_id, right_id)
        return node_id


class OrNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, ConstNode):
            return ConstNode(True) if left.value else right
        if isinstance(right, ConstNode):
            return ConstNode(True) if right.value else left

        if left == right:
            return left

        return OrNode(left, right)

    def evaluate(self, env):
        return self.left.evaluate(env) or self.right.evaluate(env)

    def to_zhegalkin(self, variables):
        left_poly = self.left.to_zhegalkin(variables)
        right_poly = self.right.to_zhegalkin(variables)
        product = multiply_polynomials(left_poly, right_poly)
        return add_polynomials(add_polynomials(left_poly, right_poly), product)

    def substitute(self, env):
        new_left = self.left.substitute(env)
        new_right = self.right.substitute(env)
        return OrNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} OR {self.right})"

    def to_graphviz(self, dot, counter):
        node_id = str(id(self))
        dot.node(node_id, "OR")
        left_id = self.left.to_graphviz(dot, counter)
        right_id = self.right.to_graphviz(dot, counter)
        dot.edge(node_id, left_id)
        dot.edge(node_id, right_id)
        return node_id


class XorNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, ConstNode) and isinstance(right, ConstNode):
            return ConstNode(left.value != right.value)

        if isinstance(left, ConstNode):
            if left.value == False:
                return right
            else:  
                return NotNode(right).simplify()
        if isinstance(right, ConstNode):
            if right.value == False:
                return left
            else:  
                return NotNode(left).simplify()

        if left == right:
            return ConstNode(False)

        return XorNode(left, right)

    def evaluate(self, env):
        return self.left.evaluate(env) != self.right.evaluate(env)

    def to_zhegalkin(self, variables):
        left_poly = self.left.to_zhegalkin(variables)
        right_poly = self.right.to_zhegalkin(variables)
        return add_polynomials(left_poly, right_poly)

    def substitute(self, env):
        new_left = self.left.substitute(env)
        new_right = self.right.substitute(env)
        return XorNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} XOR {self.right})"

    def to_graphviz(self, dot, counter):
        node_id = str(id(self))
        dot.node(node_id, "XOR")
        left_id = self.left.to_graphviz(dot, counter)
        right_id = self.right.to_graphviz(dot, counter)
        dot.edge(node_id, left_id)
        dot.edge(node_id, right_id)
        return node_id


class ImpNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        return OrNode(NotNode(self.left), self.right).simplify()

    def evaluate(self, env):
        return (not self.left.evaluate(env)) or self.right.evaluate(env)

    def to_zhegalkin(self, variables):
        one_poly = {0}
        A_poly = self.left.to_zhegalkin(variables)
        B_poly = self.right.to_zhegalkin(variables)
        AB_poly = multiply_polynomials(A_poly, B_poly)
        result_poly = add_polynomials(one_poly, A_poly)
        result_poly = add_polynomials(result_poly, AB_poly)
        return result_poly

    def substitute(self, env):
        new_left = self.left.substitute(env)
        new_right = self.right.substitute(env)
        return ImpNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} IMP {self.right})"

    def to_graphviz(self, dot, counter):
        node_id = str(id(self))
        dot.node(node_id, "IMP")
        left_id = self.left.to_graphviz(dot, counter)
        right_id = self.right.to_graphviz(dot, counter)
        dot.edge(node_id, left_id)
        dot.edge(node_id, right_id)
        return node_id


class EqvNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        return NotNode(XorNode(self.left, self.right)).simplify()

    def evaluate(self, env):
        return self.left.evaluate(env) == self.right.evaluate(env)

    def to_zhegalkin(self, variables):
        left_poly = self.left.to_zhegalkin(variables)
        right_poly = self.right.to_zhegalkin(variables)
        xor_poly = add_polynomials(left_poly, right_poly)
        return add_polynomials({0}, xor_poly)

    def substitute(self, env):
        new_left = self.left.substitute(env)
        new_right = self.right.substitute(env)
        return EqvNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} EQV {self.right})"

    def to_graphviz(self, dot, counter):
        node_id = str(id(self))
        dot.node(node_id, "EQV")
        left_id = self.left.to_graphviz(dot, counter)
        right_id = self.right.to_graphviz(dot, counter)
        dot.edge(node_id, left_id)
        dot.edge(node_id, right_id)
        return node_id


class NandNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        return NotNode(AndNode(self.left, self.right)).simplify()

    def evaluate(self, env):
        return not (self.left.evaluate(env) and self.right.evaluate(env))

    def to_zhegalkin(self, variables):
        and_poly = AndNode(self.left, self.right).to_zhegalkin(variables)
        return add_polynomials({0}, and_poly)

    def substitute(self, env):
        new_left = self.left.substitute(env)
        new_right = self.right.substitute(env)

        return NandNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} NAND {self.right})"

    def to_graphviz(self, dot, counter):
        node_id = str(id(self))
        dot.node(node_id, "NAND")
        left_id = self.left.to_graphviz(dot, counter)
        right_id = self.right.to_graphviz(dot, counter)
        dot.edge(node_id, left_id)
        dot.edge(node_id, right_id)

        return node_id


class NorNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        return NotNode(OrNode(self.left, self.right)).simplify()

    def evaluate(self, env):
        return not (self.left.evaluate(env) or self.right.evaluate(env))

    def to_zhegalkin(self, variables):
        left_poly = self.left.to_zhegalkin(variables)
        right_poly = self.right.to_zhegalkin(variables)
        product = multiply_polynomials(left_poly, right_poly)
        or_poly = add_polynomials(add_polynomials(left_poly, right_poly), product)
        return add_polynomials({0}, or_poly)

    def substitute(self, env):
        new_left = self.left.substitute(env)
        new_right = self.right.substitute(env)
        return NorNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} NOR {self.right})"

    def to_graphviz(self, dot, counter):
        node_id = str(id(self))
        dot.node(node_id, "NOR")
        left_id = self.left.to_graphviz(dot, counter)
        right_id = self.right.to_graphviz(dot, counter)
        dot.edge(node_id, left_id)
        dot.edge(node_id, right_id)

        return node_id
