import unittest
import tempfile

from gui.gui_main import 
from gui.gui_actions import *
from parser_lexer.lexer import Lexer
from parser_lexer.parser import Parser
from boolean_logic.boolean_functions import BooleanFunctionSet
from boolean_logic.quine_mccluskey import quine_mccluskey

class TestLexer(unittest.TestCase):
    def test_basic_tokens(self):
        expressions = [
            "A AND B",
            "A OR B",
            "A XOR B",
            "NOT A",
            "(A AND B) NAND C",
            "1 OR false NAND 0",
            "XOR nand nor eqv imp"
        ]

        for expression in expressions:
            lexer = Lexer(expression)
            tokens = lexer.tokenize()
            self.assertIn("EOF", [t.type for t in tokens])

    def test_invalid_character(self):
        expression2 = "A ? B"
        lexer2 = Lexer(expression2)
        
        with self.assertRaises(Exception):
            _ = lexer2.tokenize()

    def test_operators_standard_case(self):
        expression = "A AND B OR C NOT D"
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        expected_types = ["IDENTIFIER", "AND", "IDENTIFIER", "OR", "IDENTIFIER", "NOT", "IDENTIFIER", "EOF"]
        self.assertEqual([t.type for t in tokens], expected_types)

    def test_all_synonyms_nand_nor(self):
        expression = "A NAND B   C nand D   E !& F   G ¬& H   I ↑ J   K NOR L   M nor N  O !v P  Q ¬∨ R  S ↓ T"
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        self.assertIn("EOF", [t.type for t in tokens])
        nand_nor_count = sum(1 for t in tokens if t.type in ["NAND","NOR"])
        self.assertEqual(nand_nor_count, 10)


class TestParser(unittest.TestCase):
    def test_simple_parse(self):
        expression = "(A AND B) OR NOT(C)"
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_parser_error(self):
        expression = "(A AND B"
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        parser = Parser(tokens)

        with self.assertRaises(Exception):
            parser.parse()

    def test_nested_parentheses(self):
        expression = "(A AND (B OR (C XOR D)))"
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)
        self.assertEqual(str(ast), "(A AND (B OR (C XOR D)))")


class TestAST(unittest.TestCase):
    def test_evaluate_simple(self):
        expression = "A AND NOT B"
        boolean_function = BooleanFunction(expression)
        self.assertTrue(boolean_function.evaluate({"A":1, "B":0}))
        self.assertFalse(boolean_function.evaluate({"A":1, "B":1}))
        self.assertFalse(boolean_function.evaluate({"A":0, "B":0}))

    def test_simplify(self):
        expression1 = "1 AND A"
        boolean_function1 = BooleanFunction(expression1)
        self.assertEqual(boolean_function1.simplify(), "A")  

        expression2 = "0 OR B"
        boolean_function2 = BooleanFunction(expression2)
        self.assertEqual(boolean_function2.simplify(), "B")

        expression3 = "A AND A"
        boolean_function3 = BooleanFunction(expression3)
        self.assertEqual(boolean_function3.simplify(), "A")

        expression4 = "A XOR A"
        boolean_function4 = BooleanFunction(expression4)
        self.assertEqual(boolean_function4.simplify(), "0")

    def test_substitute(self):
        boolean_function = BooleanFunction("A AND B")
        new_boolean_function1 = boolean_function.cofactor("A", 1)
        self.assertEqual(new_boolean_function1.simplify(), "B")
        new_boolean_function2 = boolean_function.cofactor("B", 0)
        self.assertEqual(new_boolean_function2.simplify(), "0")

    def test_evaluate_mixed_operators(self):
        expression = "((A AND B) XOR (NOT C OR 1)) NAND (D IMP (E NOR 0))"
        boolean_function = BooleanFunction(expression)
        for values in product([0,1], repeat=5):
            variables = dict(zip(["A","B","C","D","E"], values))
            result = boolean_function.evaluate(variables)
            self.assertIn(result, [True, False])

    def test_substitute_multiple(self):
        expression = "(A AND B) OR (C XOR D)"
        boolean_function = BooleanFunction(expression)
        new_boolean_function = boolean_function.ast.substitute({"A":1, "C":0}).simplify()
        self.assertEqual(str(new_boolean_function), "(B OR D)")


class TestZhegalkin(unittest.TestCase):
    def test_not_node(self):
        expression = "NOT A"
        boolean_function = BooleanFunction(expression)
        polynomial = boolean_function.to_zhegalkin()
        polynomial_split = set(polynomial.replace(" ", "").split("+"))
        self.assertEqual(polynomial_split, {"1", "A"})

    def test_and(self):
        expression = "A AND B"
        boolean_function = BooleanFunction(expression)
        polynomial = boolean_function.to_zhegalkin()
        self.assertIn("A*B", polynomial.replace(" ", ""))

    def test_or(self):
        expression = "A OR B"
        boolean_function = BooleanFunction(expression)
        polynomial = boolean_function.to_zhegalkin()
        expected_parts = {"A", "B", "A*B"}
        polynomial_parts = set(part.strip() for part in polynomial.split("+"))
        self.assertSetEqual(expected_parts, polynomial_parts)


class TestProperties(unittest.TestCase):
    def test_preserves_zero(self):
        boolean_function1 = BooleanFunction("A AND B")
        self.assertTrue(boolean_function1.preserves_zero()) 
        boolean_function2 = BooleanFunction("A OR B")
        self.assertTrue(boolean_function2.preserves_zero())

    def test_preserves_one(self):
        boolean_function1 = BooleanFunction("A AND B")
        self.assertTrue(boolean_function1.preserves_one())
        boolean_function2 = BooleanFunction("A XOR B")
        self.assertFalse(boolean_function2.preserves_one())

    def test_is_self_dual(self):
        boolean_function_nor = BooleanFunction("A AND B")
        self.assertFalse(boolean_function_nor.is_self_dual())
        boolean_function_nand = BooleanFunction("A NAND B")
        self.assertFalse(boolean_function_nand.is_self_dual())

    def test_is_monotonic(self):
        boolean_function_and = BooleanFunction("A AND B")
        self.assertTrue(boolean_function_and.is_monotonic())
        boolean_function_xor = BooleanFunction("A XOR B")
        self.assertFalse(boolean_function_xor.is_monotonic())

    def test_is_linear(self):
        boolean_function_xor = BooleanFunction("A XOR B")
        self.assertTrue(boolean_function_xor.is_linear())
        boolean_function_and = BooleanFunction("A AND B")
        self.assertFalse(boolean_function_and.is_linear())


class TestMinimizeAndQuine(unittest.TestCase):
    def test_minimize_simple(self):
        boolean_function = BooleanFunction("(A AND B) OR (NOT A AND NOT B)")
        minimized = boolean_function.minimize()

        for (A_value, B_value) in product([0,1],[0,1]):
            original = boolean_function.evaluate({"A":A_value, "B":B_value})
            test_boolean_function = BooleanFunction(minimized)
            minimized_evaluation = test_boolean_function.evaluate({"A":A_value, "B":B_value})
            self.assertEqual(original, minimized_evaluation)

    def test_quine_with_dontcare(self):
        minterms = [0b0110, 0b0111]  
        dont_cares = [0b0000, 0b1111]
        pis = quine_mccluskey(minterms, 4, dont_cares)
        self.assertTrue(len(pis) > 0)

    def test_minimize_equiv_expression(self):
        boolean_function = BooleanFunction("A EQV B")
        min_expression = boolean_function.minimize()
        test_boolean_function = BooleanFunction(min_expression)

        for (A_value, B_value) in product([0,1],[0,1]):
            self.assertEqual(
                boolean_function.evaluate({"A": A_value, "B": B_value}),
                test_boolean_function.evaluate({"A": A_value, "B": B_value})
            )


class TestKarnaughMap(unittest.TestCase):
    def test_kmap_2vars(self):
        boolean_function = BooleanFunction("A XOR B")
        kmap = KarnaughMap(boolean_function)
        arr, _ = kmap.generate_map()
        self.assertEqual(arr.shape, (2,2))
        self.assertEqual(arr[0,0], "0")
        self.assertEqual(arr[0,1], "1")
        self.assertEqual(arr[1,0], "1")
        self.assertEqual(arr[1,1], "0")

    def test_kmap_3vars_nontrivial(self):
        boolean_function = BooleanFunction("(A AND B) OR C")
        kmap = KarnaughMap(boolean_function)
        arr, _ = kmap.generate_map()
        self.assertEqual(arr.shape, (2,4))
        self.assertEqual(arr[0,0], "0")
        self.assertEqual(arr[0,1], "1")
        self.assertEqual(arr[1,2], "1")

    def test_kmap_4vars(self):
        boolean_function = BooleanFunction("A AND B AND C AND D")
        kmap = KarnaughMap(boolean_function)
        arr, _ = kmap.generate_map()
        self.assertEqual(arr.shape, (4,4))
        all_positions = [arr[i,j] for i in range(4) for j in range(4)]
        self.assertEqual(all_positions.count("1"), 1)
        self.assertEqual(all_positions.count("0"), 15)

    
class TestEquivalence(unittest.TestCase):
    def test_equivalence(self):
        boolean_function1 = BooleanFunction("A XOR B")
        boolean_function2 = BooleanFunction("(A AND NOT B) OR (NOT A AND B)")
        difference1 = difference_measure(boolean_function1, boolean_function2)
        self.assertEqual(difference1, 0)

        boolean_function3 = BooleanFunction("A AND B")
        difference2 = difference_measure(boolean_function1, boolean_function3)
        self.assertNotEqual(difference2, 0)

    def test_equivalence_zhegalkin(self):
        boolean_function1 = BooleanFunction("A NOR B")  
        boolean_function2 = BooleanFunction("NOT(A OR B)")
        polynomial1 = boolean_function1.to_zhegalkin()
        polynomial2 = boolean_function2.to_zhegalkin()
        self.assertEqual(polynomial1, polynomial2)


class TestParseMinimizedExpression(unittest.TestCase):
    def test_parse_minimized_simple(self):
        expression = "NOT A AND B"
        node = parse_minimized_expression(expression)
        self.assertEqual(node.gate_type, "AND")
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].gate_type, "NOT")
        self.assertEqual(node.children[1].gate_type, "VAR")

    def test_parse_minimized_or(self):
        expression = "(A AND B) OR (NOT A)"
        node = parse_minimized_expression(expression)
        self.assertEqual(node.gate_type, "OR")


class TestSets(unittest.TestCase):
    def setUp(self):
        self.set1 = {"dog", "1", "cat"}
        self.set2 = {"1", "2"}

    def test_union(self):
        union_set = self.set1.union(self.set2)
        self.assertEqual(union_set, {"dog", "1", "cat","2"})

    def test_intersection(self):
        intersection = self.set1.intersection(self.set2)
        self.assertEqual(intersection, {"1"})

    def test_difference(self):
        differece = self.set1.difference(self.set2)
        self.assertEqual(differece, {"dog","cat"})

    def test_symdiff(self):
        symmetrical_difference = self.set1.symmetric_difference(self.set2)
        self.assertEqual(symmetrical_difference, {"dog","cat","2"})

    def test_subset(self):
        self.assertFalse(self.set2.issubset(self.set1))
        self.assertTrue({"1"}.issubset(self.set1))
        self.assertFalse(self.set1.issubset(self.set2))

    def test_disjoint(self):
        self.assertFalse(self.set1.isdisjoint(self.set2))
        self.assertTrue({"xxx"}.isdisjoint(self.set2))

    def test_powerset(self):
        example_set = {"A","B"}
        powerset = []

        for mask in range(2**len(example_set)):
            subset = []

            for i, element in enumerate(sorted(list(example_set))):
                if mask & (1 << i):
                    subset.append(element)
            powerset.append(frozenset(subset))

        self.assertEqual(len(powerset), 4)
        self.assertIn(frozenset(), powerset)
        self.assertIn(frozenset({"A","B"}), powerset)

    def test_cartesian_product_empty(self):
        example_set1 = {"x","y"}
        example_set2 = set()
        product_result = [(a,b) for a in example_set1 for b in example_set2]
        self.assertEqual(len(product_result), 0)
        

class TestBooleanFunctionSet(unittest.TestCase):
    def test_add_function_and_export(self):
        boolean_function_set1 = BooleanFunctionSet()
        boolean_function_set2 = BooleanFunction("A AND B")
        boolean_function_set3 = BooleanFunction("A OR B")
        boolean_function_set1.add_function(boolean_function_set2)
        boolean_function_set1.add_function(boolean_function_set3)
        info = boolean_function_set1.get_functions_info()
        self.assertEqual(len(info), 2)

        for item in info:
            self.assertIn("expression", item)
            self.assertIn("simplified", item)
            self.assertIn("zhegalkin", item)
            self.assertIn("properties", item)
            self.assertIn("minimized", item)
            self.assertIn("number_of_variables", item)
            self.assertIn("truth_table", item)


class TestFileExport(unittest.TestCase):
    def test_export_json(self):
        boolean_function = BooleanFunction("A AND B")
        function_set.add_function(boolean_function)

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.json")
            info = function_set.get_functions_info()

            with open(test_file, "w", encoding="utf-8") as f:
                json.dump(info, f, ensure_ascii=False, indent=4)

            self.assertTrue(os.path.exists(test_file))
            with open(test_file, "r", encoding="utf-8") as ff:
                data = json.load(ff)

            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)

    def test_save_and_reload(self):
        boolean_function1 = BooleanFunction("A AND B")
        boolean_function2 = BooleanFunction("NOT(A OR 0)")

        function_set.add_function(boolean_function1)
        function_set.add_function(boolean_function2)

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test_export.json")
            info = function_set.get_functions_info()

            with open(test_file, "w", encoding="utf-8") as f:
                json.dump(info, f, ensure_ascii=False, indent=4)

            with open(test_file, "r", encoding="utf-8") as f:
                data = json.load(f)

        self.assertEqual(len(data), 2)

        and_function_entry = next((item for item in data if item["expression"] == "A AND B"), None)
        self.assertIsNotNone(and_function_entry)

        not_or_function_entry = next((item for item in data if item["expression"] == "NOT(A OR 0)"), None)
        self.assertIsNotNone(not_or_function_entry,)

        self.assertTrue(and_function_entry["simplified"],)
        self.assertTrue(and_function_entry["zhegalkin"],)
        self.assertTrue(and_function_entry["minimized"])
        self.assertIn("preserves_zero", and_function_entry["properties"])
        self.assertIn("preserves_one", and_function_entry["properties"])
        self.assertIn("is_self_dual", and_function_entry["properties"])
        self.assertIn("is_monotonic", and_function_entry["properties"])
        self.assertIn("is_linear", and_function_entry["properties"])
        self.assertEqual(and_function_entry["number_of_variables"], 2)
        self.assertEqual(len(and_function_entry["truth_table"]), 4)

        self.assertTrue(not_or_function_entry["simplified"])
        self.assertTrue(not_or_function_entry["zhegalkin"])
        self.assertTrue(not_or_function_entry["minimized"])
        self.assertIn("preserves_zero", not_or_function_entry["properties"])
        self.assertIn("preserves_one", not_or_function_entry["properties"])
        self.assertIn("is_self_dual", not_or_function_entry["properties"])
        self.assertIn("is_monotonic", not_or_function_entry["properties"])
        self.assertIn("is_linear", not_or_function_entry["properties"])
        self.assertEqual(not_or_function_entry["number_of_variables"], 1)
        self.assertEqual(len(not_or_function_entry["truth_table"]), 2)


if __name__ == "__main__":
    unittest.main()
