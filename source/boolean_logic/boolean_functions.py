from parser_lexer.lexer import *
from parser_lexer.parser import *
from boolean_logic.helpers import *
from functools import lru_cache
from itertools import product
from boolean_logic.quine_mccluskey import * 

def get_variables(node):
    variables = set()
    if isinstance(node, VariableNode):
        variables.add(node.name)
    elif isinstance(node, NotNode):
        variables.update(get_variables(node.operand))
    elif isinstance(node, (AndNode, OrNode, XorNode, ImpNode, EqvNode, NandNode, NorNode)):
        variables.update(get_variables(node.left))
        variables.update(get_variables(node.right))
    return variables

class BooleanFunction:
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
        if self._simplified_cache is not None:
            return self._simplified_cache
        self.ast = self.ast.simplify()
        simplified_expr = str(self.ast) 
        simplified_expr = self.remove_outer_parens(simplified_expr)
        self._simplified_cache = simplified_expr
        return simplified_expr

    def remove_outer_parens(self, expr):
        expr = expr.strip()
        if expr.startswith("(") and expr.endswith(")"):
            count = 0
            remove = True
            for i, ch in enumerate(expr):
                if ch == '(':
                    count += 1
                elif ch == ')':
                    count -= 1
                if count == 0 and i < len(expr)-1:
                    remove = False
                    break
            if remove:
                return expr[1:-1].strip()
        return expr

    @lru_cache(None)
    def to_zhegalkin(self):
        if self._zhegalkin_cache is not None:
            return self._zhegalkin_cache
        poly = self.ast.to_zhegalkin(self.variables)
        self._zhegalkin_cache = zhegalkin_poly_to_str(poly, self.variables)
        return self._zhegalkin_cache

    def get_truth_table(self):
        if self._truth_table_cache is not None:
            return self._truth_table_cache
        num_vars = len(self.variables)
        truth_table = []
        for values in product([0, 1], repeat=num_vars):
            env = dict(zip(self.variables, values))
            result = int(self.evaluate(env))
            truth_table.append((values, result))
        self._truth_table_cache = truth_table
        return truth_table

    def evaluate(self, env):
        return self.ast.evaluate(env)

    def preserves_zero(self):
        if "preserves_zero" in self._properties_cache:
            return self._properties_cache["preserves_zero"]
        env = {var: 0 for var in self.variables}
        val = (self.evaluate(env) == 0)
        self._properties_cache["preserves_zero"] = val
        return val

    def preserves_one(self):
        if "preserves_one" in self._properties_cache:
            return self._properties_cache["preserves_one"]
        env = {var: 1 for var in self.variables}
        val = (self.evaluate(env) == 1)
        self._properties_cache["preserves_one"] = val
        return val

    def is_self_dual(self):
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
        if "is_linear" in self._properties_cache:
            return self._properties_cache["is_linear"]
        poly = self.ast.to_zhegalkin(self.variables)
        for monomial in poly:
            if bin(monomial).count('1') > 1:
                self._properties_cache["is_linear"] = False
                return False
        self._properties_cache["is_linear"] = True
        return True

    def minimize(self):
        if self._minimized_cache is not None:
            return self._minimized_cache

        truth_table = self.get_truth_table()
        minterms = [values for values, result in truth_table if result == 1]
        num_vars = len(self.variables)

        if not minterms:
            self._minimized_cache = "0"
            return "0"
        if len(minterms) == 2 ** num_vars:
            self._minimized_cache = "1"
            return "1"

        minterm_nums = [sum(val << (num_vars - idx - 1) for idx, val in enumerate(values)) for values in minterms]
        minimized_terms = quine_mccluskey(minterm_nums, num_vars)

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
        if variable not in self.variables:
            raise ValueError(f"The variable {variable} is not part of the function.")

        env = {var: value if var == variable else None for var in self.variables}
        new_ast = self.ast.substitute(env).simplify()
        new_expr = str(new_ast)
        return BooleanFunction(new_expr)

    def decompose(self, variable):
        if variable not in self.variables:
            raise ValueError(f"The variable {variable} is not part of the function.")

        cofactor_0 = self.cofactor(variable, 0)
        cofactor_1 = self.cofactor(variable, 1)

        return cofactor_0, cofactor_1

    def __eq__(self, other):
        if not isinstance(other, BooleanFunction):
            return NotImplemented
        return self.expression == other.expression

    def __hash__(self):
        return hash(self.expression)
    

class BooleanFunctionSet:
    def __init__(self):
        self.functions = set()  

    def add_function(self, boolean_function):
        self.functions.add(boolean_function)

    def get_functions_info(self):
        functions_info = []
        for f in self.functions:
            info = {
                "expression": f.expression,
                "simplified": f.simplify(),
                "zhegalkin": f.to_zhegalkin(),
                "properties": {
                    "preserves_zero": f.preserves_zero(),
                    "preserves_one": f.preserves_one(),
                    "is_self_dual": f.is_self_dual(),
                    "is_monotonic": f.is_monotonic(),
                    "is_linear": f.is_linear(),
                },
                "minimized": f.minimize(),
                "number_of_variables": len(f.variables),
                "truth_table": self._format_truth_table(f.get_truth_table(), f.variables)
            }
            functions_info.append(info)
        return functions_info

    def _format_truth_table(self, truth_table, variables):
        formatted = []
        for inputs, result in truth_table:
            input_dict = {var: val for var, val in zip(variables, inputs)}
            formatted.append({"inputs": input_dict, "output": result})
        return formatted