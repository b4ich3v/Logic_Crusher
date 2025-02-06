# **Logic Crusher**

## **Description**

**Logic Crusher** is a graphical application that allows users to input, simplify, and minimize Boolean expressions. The application uses the Quine–McCluskey algorithm for minimization and offers visual tools such as Karnaugh maps and visualization of the Abstract Syntax Tree (AST).

The goal is to simplify logical formulas for better understanding and efficiency, making the tool useful for both educational and professional purposes.

---

## **Supported Operators**

### **Binary Logical Operators**

| Operator                  | Supported Alternatives        |
|---------------------------|-------------------------------|
| Disjunction (OR)          | OR, or, ∨, \|, \|\|           |
| Conjunction (AND)         | AND, and, &, ∧, &&            |
| Exclusive OR (XOR)        | XOR, xor, ^, ⊕               |
| Equivalence (EQV)         | EQV, eqv, <=>, ↔, ==          |
| Implication (IMP)         | IMP, imp, =>, →, ⇒            |
| NAND                       | NAND, nand, !&, ¬&, ↑         |
| NOR                        | NOR, nor, !v, ¬∨, ↓          |

### **Unary Logical Operators**

| Operator      | Supported Alternatives |
|---------------|------------------------|
| Negation (NOT) | NOT, not, !, ~, ¬      |

### **Constants**

| Constant | Supported Alternatives |
|----------|------------------------|
| True     | true, 1               |
| False    | false, 0              |

---

## **Features**

- **Input and prioritization of Boolean expressions:**
  - Enter and select one or two Boolean expressions for further operations.
  
- **Syntax validation:**
  - Checks the correctness of the syntax of the entered Boolean expressions.
  
- **Expression simplification:**
  - Simplifies expressions to their shortest form.
  
- **Checking logical properties:**
  - **Monotonicity:** Checks if the function is monotonic.
  - **Linearity:** Checks if the function is linear.
  - **Self-duality:** Checks if the function is self-dual.
  - **Preserving zero:** Checks if the function preserves zero.
  - **Preserving one:** Checks if the function preserves one.
  
- **Expression minimization:**
  - Minimizes expressions using the Quine–McCluskey algorithm.
  
- **Generating Zhegalkin polynomials:**
  - Generates Zhegalkin polynomials for the selected Boolean expressions.
  
- **Karnaugh map visualization:**
  - Generates and visualizes Karnaugh maps for Boolean functions with 2–4 variables.
  
- **Abstract Syntax Tree (AST) visualization:**
  - Visualizes the AST of the selected Boolean expressions using Graphviz.
  
- **Generating logic circuits (Circuit Diagram):**
  - Generates and visualizes logic circuits of minimized expressions.
  
- **Saving expressions and properties:**
  - Saves all stored expressions and their properties in JSON format files.
  
- **Checking equivalence between two expressions:**
  - Checks if two Boolean expressions are equivalent and shows the difference in the number of input combinations.

- **Set operations:**
  - **Union:** Unites two sets.
  - **Intersection:** Finds the common elements of two sets.
  - **Difference:** Finds the elements that are in one set but not in the other.
  - **Symmetric difference:** Finds the elements that are in either set but not in both.
  - **Venn diagrams:** Visualizes Venn diagrams for two sets.
  - **Cartesian product:** Computes the Cartesian product of two sets.
  - **Cardinality:** Computes the number of elements in both sets.
  - **Power sets:** Generates the power sets of both sets.
  - **Relation checks:** Checks various relations between the sets such as subset, superset, equality, and discreteness.

---

## **Rules**

- **Entering Boolean Expressions:**
  - Variables must consist of letters (a-z, A-Z).
  - Reserved keywords (`true`, `false`) cannot be used as variable names.
  - Expressions without parentheses are evaluated left to right according to operator precedence.
  - Expressions must be syntactically correct with parentheses where needed.
  - Use the supported logical operators and constants.

- **Entering Sets:**
  - Enter the elements of the sets, separated by commas (e.g., A, B, C).
  - Use the alternative operator names as needed.

- **Selecting the Active Expression:**
  - Choose which expression (1 or 2) to use for operations.

- **Variable for Decomposition:**
  - Specify a variable from the active expression for decomposition. Case-sensitive (e.g., `A` ≠ `a`).

- **Factoring by Variable:**
  - Decomposes the active expression with respect to the specified variable.

- **Karnaugh Map Generation:**
  - Only supported for Boolean functions with 2–4 variables.

- **Saving to File:**
  - Saves all stored expressions and their properties as a JSON file.

- **Equivalence Check:**
  - Both expressions must be valid and entered in the respective fields.

---
<br><br>
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <img src="screenshots/screenshot1.png" alt="Image 1" width="1000"/>
</div>
<br><br>
<br><br>
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <img src="screenshots/screenshot2.png" alt="Image 1" width="1000"/>
</div>
<br><br>
<br><br>
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <img src="screenshots/screenshot6.png" alt="Image 1" width="1000"/>
</div>
<br><br>
