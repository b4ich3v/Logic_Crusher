from functools import lru_cache
from itertools import product

from parser_lexer.lexer import Lexer
from parser_lexer.parser import Parser
from ast_nodes.nodes import (
    EqvNode, ImpNode, OrNode, NorNode, 
    XorNode, AndNode, NandNode, NotNode, 
    VariableNode
)
from boolean_logic.helpers import zhegalkin_polynomial_to_str
from boolean_logic.quine_mccluskey import quine_mccluskey


def get_variables(node):
    """
    Recursively gather all variable names from the given AST node.
    For example, if the node is (A AND (NOT B)), returns {'A', 'B'}.
    """
    variables = set()

    if isinstance(node, VariableNode):
        variables.add(node.name)
    elif isinstance(node, NotNode):
        variables.update(get_variables(node.operand))
    elif isinstance(node, (
        AndNode, OrNode, XorNode, ImpNode, 
        EqvNode, NandNode, NorNode)
        ):
        variables.update(get_variables(node.left))
        variables.update(get_variables(node.right))

    return variables


class BooleanFunction:
    """
    A class representing a Boolean expression and providing methods
    for simplification, minimization, property checks, and more.
    """

    def __init__(self, expression):
        self.expression = expression
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        self.ast = parser.parse()
        self.variables = sorted(list(get_variables(self.ast)))

        self._truth_table_cache = None
        self._zhegalkin_cache = None
        self._minimized_cache = None
        self._properties_cache = {}  
        self._simplified_cache = None

    def simplify(self):
        """
        Return a simplified string representation of the Boolean function,
        caching the result if already computed.
        """
        if self._simplified_cache is not None:
            return self._simplified_cache
        
        self.ast = self.ast.simplify()
        simplified_expression = str(self.ast) 
        simplified_expression = self.remove_outer_parens(simplified_expression)
        self._simplified_cache = simplified_expression

        return simplified_expression

    def remove_outer_parens(self, expression):
        expression = expression.strip()

        if expression.startswith("(") and expression.endswith(")"):
            count = 0
            remove = True

            for i, ch in enumerate(expression):
                if ch == "(":
                    count += 1
                elif ch == ")":
                    count -= 1
                if count == 0 and i < len(expression)-1:
                    remove = False
                    break
            if remove:
                return expression[1:-1].strip()
        return expression

    @lru_cache(None)
    def to_zhegalkin(self):
        """
        Return the Zhegalkin polynomial representation of this Boolean function as a string.
        Uses caching to avoid recomputation.
        """
        if self._zhegalkin_cache is not None:
            return self._zhegalkin_cache
        
        polynomial = self.ast.to_zhegalkin(self.variables)
        self._zhegalkin_cache = zhegalkin_polynomial_to_str(polynomial, self.variables)

        return self._zhegalkin_cache

    def get_truth_table(self):
        """
        Build and cache the truth table (list of (input_tuple, result) pairs)
        for the current Boolean function.
        """
        if self._truth_table_cache is not None:
            return self._truth_table_cache
        
        variables_count = len(self.variables)
        truth_table = []

        for values in product([0, 1], repeat=variables_count):
            env = dict(zip(self.variables, values))
            result = int(self.evaluate(env))
            truth_table.append((values, result))

        self._truth_table_cache = truth_table
        return truth_table

    def evaluate(self, variables):
        """
        Evaluate the AST with a given dictionary of variable assignments.
        """
        return self.ast.evaluate(variables)

    def preserves_zero(self):
        """
        Check if the function preserves zero (returns 0 when all variables are 0).
        """
        if "preserves_zero" in self._properties_cache:
            return self._properties_cache["preserves_zero"]
        
        new_variables = dict.fromkeys(self.variables, 0)
        value = self.evaluate(new_variables) == 0
        self._properties_cache["preserves_zero"] = value

        return value

    def preserves_one(self):
        """
        Check if the function preserves one (returns 1 when all variables are 1).
        """
        if "preserves_one" in self._properties_cache:
            return self._properties_cache["preserves_one"]
        
        new_variables = dict.fromkeys(self.variables, 1)
        value = self.evaluate(new_variables) == 1
        self._properties_cache["preserves_one"] = value

        return value

    def is_self_dual(self):
        """
        Check if the function is self-dual, i.e., F(~x) = ~F(x).
        """
        if "is_self_dual" in self._properties_cache:
            return self._properties_cache["is_self_dual"]
        
        truth_table = self.get_truth_table()
        mapping = {}

        for values, result in truth_table:
            inverted_values = tuple(1 - v for v in values)
            mapping[inverted_values] = 1 - result

        for values, result in truth_table:
            if result != mapping.get(values, result):
                self._properties_cache["is_self_dual"] = False
                return False
        self._properties_cache["is_self_dual"] = True

        return True

    def is_monotonic(self):
        """
        Check if the function is monotonic, i.e., non-decreasing when inputs are flipped from 0 to 1.
        """
        if "is_monotonic" in self._properties_cache:
            return self._properties_cache["is_monotonic"]
        
        truth_table = self.get_truth_table()

        for (values1, result1) in truth_table:
            for (values2, result2) in truth_table:
                if all(v1 <= v2 for v1, v2 in zip(values1, values2)):
                    if result1 > result2:
                        self._properties_cache["is_monotonic"] = False
                        return False
                    
        self._properties_cache["is_monotonic"] = True
        return True

    def is_linear(self):
        """
        Check if the function is linear, meaning each monomial in its Zhegalkin polynomial
        has at most one variable (no products of multiple variables).
        """
        if "is_linear" in self._properties_cache:
            return self._properties_cache["is_linear"]
        
        polynomial = self.ast.to_zhegalkin(self.variables)

        for monomial in polynomial:
            if bin(monomial).count("1") > 1:
                self._properties_cache["is_linear"] = False
                return False
            
        self._properties_cache["is_linear"] = True
        return True

    def minimize(self):
        """
        Minimize the function using the Quine-McCluskey algorithm.
        Returns a string of the minimized expression.
        """
        if self._minimized_cache is not None:
            return self._minimized_cache

        truth_table = self.get_truth_table()
        minterms = [values for values, result in truth_table if result == 1]
        variables_count = len(self.variables)

        if not minterms:
            self._minimized_cache = "0"
            return "0"
        
        if len(minterms) == 2 ** variables_count:
            self._minimized_cache = "1"
            return "1"

        minterm_numbers = [
            sum(val << (variables_count - idx - 1) for idx, val
            in enumerate(values)) for values in minterms
            ]
        minimized_terms = quine_mccluskey(minterm_numbers, variables_count)
        terms_str = []

        for term in minimized_terms:
            literals = []

            for idx, val in enumerate(term):
                if val == "1":
                    literals.append(self.variables[idx])
                elif val == "0":
                    literals.append(f"NOT {self.variables[idx]}")

            if not literals:
                term_str = "1"
            else:
                if len(literals) == 1:
                    term_str = literals[0]
                else:
                    term_str = " AND ".join(literals)
                    term_str = f"({term_str})"

            terms_str.append(term_str)

        minimized_expression = " OR ".join(terms_str)
        minimized_expression = self.remove_outer_parens(minimized_expression)
        self._minimized_cache = minimized_expression

        return minimized_expression

    def cofactor(self, variable, value):
        """
        Return a new BooleanFunction that is the cofactor of self by setting
        a given variable to a specified value (0 or 1).
        """
        if variable not in self.variables:
            raise ValueError(f"The variable {variable} is not part of the function.")

        new_variables = {var: value if var == variable else None for var in self.variables}
        new_ast = self.ast.substitute(new_variables).simplify()
        new_expression = str(new_ast)

        return BooleanFunction(new_expression)

    def decompose(self, variable):
        """
        Decompose this Boolean function into two cofactors with respect to 'variable':
        one where variable=0 and one where variable=1.
        """
        if variable not in self.variables:
            raise ValueError(f"The variable {variable} is not part of the function.")

        cofactor0 = self.cofactor(variable, 0)
        cofactor1 = self.cofactor(variable, 1)

        return cofactor0, cofactor1

    def __eq__(self, other):
        if not isinstance(other, BooleanFunction):
            return NotImplemented
        return self.expression == other.expression

    def __hash__(self):
        return hash(self.expression)
    

class BooleanFunctionSet:
    """
    Maintains a set of BooleanFunction objects and can provide collective information.
    """

    def __init__(self):
        self.functions = set()  

    def add_function(self, boolean_function):
        """
        Add a BooleanFunction instance to the set.
        """
        self.functions.add(boolean_function)

    def get_functions_info(self):
        """
        Collect descriptive information about each stored BooleanFunction,
        including its properties, minimized expression, and truth table.
        """
        functions_info = []

        for current_function in self.functions:
            info = {
                "expression": current_function.expression,
                "simplified": current_function.simplify(),
                "zhegalkin": current_function.to_zhegalkin(),
                "properties": {
                    "preserves_zero": current_function.preserves_zero(),
                    "preserves_one": current_function.preserves_one(),
                    "is_self_dual": current_function.is_self_dual(),
                    "is_monotonic": current_function.is_monotonic(),
                    "is_linear": current_function.is_linear(),
                },
                "minimized": current_function.minimize(),
                "number_of_variables": len(current_function.variables),
                "truth_table": self._format_truth_table(
                    current_function.get_truth_table(), 
                    current_function.variables
                    )
            }
            functions_info.append(info)

        return functions_info

    def _format_truth_table(self, truth_table, variables):
        """
        Convert a list of (input_tuple, output) pairs into a more readable structure.
        """
        formatted = []

        for inputs, result in truth_table:
            input_dict = {var: val for var, val in zip(variables, inputs)}
            formatted.append({"inputs": input_dict, "output": result})
            
        return formatted
