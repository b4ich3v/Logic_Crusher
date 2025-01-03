from boolean_logic.helpers import add_polynomials, multiply_polynomials

class Node:
    def simplify(self):
        return self

    def evaluate(self, variables):
        pass

    def to_zhegalkin(self, variables):
        pass

    def __eq__(self, other):
        return isinstance(other, Node) and self.__dict__ == other.__dict__

    def substitute(self, variables):
        return self

    def to_graphviz(self, graph, counter):
        pass


class VariableNode(Node):
    def __init__(self, name):
        self.name = name

    def simplify(self):
        return self

    def evaluate(self, variables):
        return variables[self.name]

    def to_zhegalkin(self, variables):
        index = variables.index(self.name)
        monomial = 1 << index
        return {monomial}

    def substitute(self, variables):
        if self.name in variables and variables[self.name] is not None:
            return ConstNode(variables[self.name])
        else:
            return self

    def __str__(self):
        return self.name

    def to_graphviz(self, graph, counter):
        node_id = str(id(self))
        graph.node(node_id, self.name)

        return node_id


class ConstNode(Node):
    def __init__(self, value):
        self.value = value

    def simplify(self):
        return self

    def evaluate(self, variables):
        return self.value

    def to_zhegalkin(self, variables):
        return {0} if self.value else set()

    def substitute(self, variables):
        return self

    def __str__(self):
        return "1" if self.value else "0"

    def to_graphviz(self, graph, counter):
        node_id = str(id(self))
        label = "1" if self.value else "0"
        graph.node(node_id, label)

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

    def evaluate(self, variables):
        return not self.operand.evaluate(variables)

    def to_zhegalkin(self, variables):
        operand_polynomial = self.operand.to_zhegalkin(variables)
        one_polynomial = {0} 

        return add_polynomials(one_polynomial, operand_polynomial)

    def substitute(self, variables):
        new_operand = self.operand.substitute(variables)

        return NotNode(new_operand).simplify()

    def __str__(self):
        return f"NOT {self.operand}"

    def to_graphviz(self, graph, counter):
        node_id = str(id(self))
        graph.node(node_id, "NOT")
        child_id = self.operand.to_graphviz(graph, counter)
        graph.edge(node_id, child_id)

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

    def evaluate(self, variables):
        return self.left.evaluate(variables) and self.right.evaluate(variables)

    def to_zhegalkin(self, variables):
        left_polynomial = self.left.to_zhegalkin(variables)
        right_polynomial = self.right.to_zhegalkin(variables)

        return multiply_polynomials(left_polynomial, right_polynomial)

    def substitute(self, variables):
        new_left = self.left.substitute(variables)
        new_right = self.right.substitute(variables)

        return AndNode(new_left, new_right).simplify()

    def __str__(self):
        return f'({self.left} AND {self.right})'

    def to_graphviz(self, graph, counter):
        node_id = str(id(self))
        graph.node(node_id, "AND")
        left_id = self.left.to_graphviz(graph, counter)
        right_id = self.right.to_graphviz(graph, counter)
        graph.edge(node_id, left_id)
        graph.edge(node_id, right_id)

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

    def evaluate(self, variables):
        return self.left.evaluate(variables) or self.right.evaluate(variables)

    def to_zhegalkin(self, variables):
        left_polynomial = self.left.to_zhegalkin(variables)
        right_polynomial = self.right.to_zhegalkin(variables)
        product = multiply_polynomials(left_polynomial, right_polynomial)

        return add_polynomials(add_polynomials(left_polynomial, right_polynomial), product)

    def substitute(self, variables):
        new_left = self.left.substitute(variables)
        new_right = self.right.substitute(variables)

        return OrNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} OR {self.right})"

    def to_graphviz(self, graph, counter):
        node_id = str(id(self))
        graph.node(node_id, "OR")
        left_id = self.left.to_graphviz(graph, counter)
        right_id = self.right.to_graphviz(graph, counter)
        graph.edge(node_id, left_id)
        graph.edge(node_id, right_id)

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

    def evaluate(self, variables):
        return self.left.evaluate(variables) != self.right.evaluate(variables)

    def to_zhegalkin(self, variables):
        left_polynomial = self.left.to_zhegalkin(variables)
        right_polynomial = self.right.to_zhegalkin(variables)

        return add_polynomials(left_polynomial, right_polynomial)

    def substitute(self, variables):
        new_left = self.left.substitute(variables)
        new_right = self.right.substitute(variables)

        return XorNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} XOR {self.right})"

    def to_graphviz(self, graph, counter):
        node_id = str(id(self))
        graph.node(node_id, "XOR")
        left_id = self.left.to_graphviz(graph, counter)
        right_id = self.right.to_graphviz(graph, counter)
        graph.edge(node_id, left_id)
        graph.edge(node_id, right_id)

        return node_id


class ImpNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        return OrNode(NotNode(self.left), self.right).simplify()

    def evaluate(self, variables):
        return (not self.left.evaluate(variables)) or self.right.evaluate(variables)

    def to_zhegalkin(self, variables):
        one_polynomial = {0}
        A_polynomial = self.left.to_zhegalkin(variables)
        B_polynomial = self.right.to_zhegalkin(variables)
        AB_polynomial = multiply_polynomials(A_polynomial, B_polynomial)
        result_polynomial = add_polynomials(one_polynomial, A_polynomial)
        result_polynomial = add_polynomials(result_polynomial, AB_polynomial)

        return result_polynomial

    def substitute(self, variables):
        new_left = self.left.substitute(variables)
        new_right = self.right.substitute(variables)

        return ImpNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} IMP {self.right})"

    def to_graphviz(self, graph, counter):
        node_id = str(id(self))
        graph.node(node_id, "IMP")
        left_id = self.left.to_graphviz(graph, counter)
        right_id = self.right.to_graphviz(graph, counter)
        graph.edge(node_id, left_id)
        graph.edge(node_id, right_id)

        return node_id


class EqvNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        return NotNode(XorNode(self.left, self.right)).simplify()

    def evaluate(self, variables):
        return self.left.evaluate(variables) == self.right.evaluate(variables)

    def to_zhegalkin(self, variables):
        left_polynomial = self.left.to_zhegalkin(variables)
        right_polynomial = self.right.to_zhegalkin(variables)
        xor_polynomial = add_polynomials(left_polynomial, right_polynomial)

        return add_polynomials({0}, xor_polynomial)

    def substitute(self, variables):
        new_left = self.left.substitute(variables)
        new_right = self.right.substitute(variables)

        return EqvNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} EQV {self.right})"

    def to_graphviz(self, graph, counter):
        node_id = str(id(self))
        graph.node(node_id, "EQV")
        left_id = self.left.to_graphviz(graph, counter)
        right_id = self.right.to_graphviz(graph, counter)
        graph.edge(node_id, left_id)
        graph.edge(node_id, right_id)

        return node_id


class NandNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        return NotNode(AndNode(self.left, self.right)).simplify()

    def evaluate(self, variables):
        return not (self.left.evaluate(variables) and self.right.evaluate(variables))

    def to_zhegalkin(self, variables):
        and_polynomial = AndNode(self.left, self.right).to_zhegalkin(variables)

        return add_polynomials({0}, and_polynomial)

    def substitute(self, variables):
        new_left = self.left.substitute(variables)
        new_right = self.right.substitute(variables)

        return NandNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} NAND {self.right})"

    def to_graphviz(self, graph, counter):
        node_id = str(id(self))
        graph.node(node_id, "NAND")
        left_id = self.left.to_graphviz(graph, counter)
        right_id = self.right.to_graphviz(graph, counter)
        graph.edge(node_id, left_id)
        graph.edge(node_id, right_id)

        return node_id


class NorNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        return NotNode(OrNode(self.left, self.right)).simplify()

    def evaluate(self, variables):
        return not (self.left.evaluate(variables) or self.right.evaluate(variables))

    def to_zhegalkin(self, variables):
        left_polynomial = self.left.to_zhegalkin(variables)
        right_polynomial = self.right.to_zhegalkin(variables)
        product = multiply_polynomials(left_polynomial, right_polynomial)
        or_polynomial = add_polynomials(add_polynomials(left_polynomial, right_polynomial), product)

        return add_polynomials({0}, or_polynomial)

    def substitute(self, variables):
        new_left = self.left.substitute(variables)
        new_right = self.right.substitute(variables)

        return NorNode(new_left, new_right).simplify()

    def __str__(self):
        return f"({self.left} NOR {self.right})"

    def to_graphviz(self, graph, counter):
        node_id = str(id(self))
        graph.node(node_id, "NOR")
        left_id = self.left.to_graphviz(graph, counter)
        right_id = self.right.to_graphviz(graph, counter)
        graph.edge(node_id, left_id)
        graph.edge(node_id, right_id)

        return node_id
