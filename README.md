# **Logic crusher**

## **Description:**

Logic Crusher is a graphical application that allows users to type, 
simplify and minimize boolean expressions. The application uses the Quine–McCluskey algorithm to 
minification and rendering visualization through carno maps and Abstract Syntax Tree (AST). The main goal is to reduce the complexity of logic formulas for better comprehensibility and efficiency, and to facilitate the analysis and optimization of logical expressions for educational and professional purposes.

## **Supported operators:**

| Binary logical operators | Supported alternatives |
|----------|----------|
| Disjunction | OR, or, ∨, \|, \|\| |
| Conjunction |  AND, and, &, ∧, && |
| Exclusive or |  XOR, xor, ^, ⊕ |
| Equivalence | EQV, eqv, <=>, ↔, ==|
| Implication | IMP, imp, =>, →, ⇒|
| Not AND | NAND, nand, !&, ¬&, ↑ |
| Not OR | NOR, nor, !v, ¬∨, ↓ |

| Unary logical operators  | Supported alternatives |
|----------|----------|
| Negation | NOT, not, !, ~, ¬ |

## **Functionalities:**

* Entering a boolean expression through the user interface.
* Expression syntax validation.
* Simplify the expression.
* Checking logical properties: monotonicity, linearity, self-duality, preservation of zero and one.
* Minimizing Boolean expressions with the Quine–McCluskey algorithm.
* Generating a Zhegalkin polynomial.
* Generate and visualize Carnot maps for 2 to 4 variables.
* Abstract Syntax Tree (AST) Visualization with Graphviz.
* Display results and minimized expressions in the GUI.
* Factoring in a variable.
* Option to save a specific expression as a file.
