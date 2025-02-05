## Table of Contents

- Start
  - Input Expressions
  - Select Active Expression
  - Enter Variable
  - Display Results
  - Buttons
- Features
  - Simplification of Boolean Expressions
  - Generating Zhegalkin Polynomials
  - Checking Function Properties
  - Minimizing Expressions
  - Decomposition of Expressions
  - Generating Karnaugh Maps
  - Visualization of Abstract Syntax Trees (AST)
  - Generating Circuits
  - Checking Equivalence Between Expressions
  - Set Operations
- Theoretical Background
  - Boolean Algebra
  - Quine-McCluskey Algorithm
  - Karnaugh Maps
  - Zhegalkin Polynomials
  - Abstract Syntax Trees (AST)
  - Generating Circuits
  - Set Operations
- Examples

---

### Start

#### Input Expressions
- Enter up to two Boolean expressions for comparison or dual operations.

#### Select Active Expression
- Choose which expression (1 or 2) is active for the operations.

#### Enter Variable
- Specify a variable for decomposition operations.

#### Display Results
- View the results of the operations in the designated area.

#### Buttons
- Access various functionalities through clearly labeled buttons.

---

## Features

### Simplification of Boolean Expressions

**Description:** Simplifies the selected Boolean expression to its minimal form.

**How to use:**

1. Enter the Boolean expression in the "`Expression 1`" or "`Expression 2`" field.
2. Select the active expression using the radio buttons.
3. Click the "`Simplification`" button.
4. View the simplified expression in the results display.

**Example:**

- **Input:** `(A AND B) OR (A AND NOT B)`
- **Simplified Output:** `A`

---

### Generating Zhegalkin Polynomials

**Description:** Converts the selected Boolean expression into its corresponding Zhegalkin polynomial.

**How to use:**

1. Enter the Boolean expression.
2. Select the active expression.
3. Click the "`Zhegalkin polynomial`" button.
4. The Zhegalkin polynomial will be displayed.

**Example:**

- **Input:** `A XOR B`
- **Zhegalkin Polynomial:** `A ⊕ B`

---

### Checking Function Properties

**Description:** Analyzes the selected Boolean function for various properties such as preserving zero and one, self-duality, monotonicity, and linearity.

**How to use:**

1. Enter the Boolean expression.
2. Select the active expression.
3. Click the "`Property check`" button.
4. View the properties in the results display.

**Properties Checked:**

- **Preserving Zero:** The function outputs zero when all inputs are zero.
- **Preserving One:** The function outputs one when all inputs are one.
- **Self-duality:** The function is equal to its dual.
- **Monotonicity:** The function’s output does not decrease when any input bit transitions from `0` to `1`.
- **Linearity:** The function can be expressed as a linear combination of the input variables.

---

### Minimizing Expressions

**Description:** Minimizes the selected Boolean expression using the `Quine-McCluskey` algorithm.

**How to use:**

1. Enter the Boolean expression.
2. Select the active expression.
3. Click the "`Minimize`" button.
4. The minimized expression will be displayed.

**Example:**

- **Input:** `A OR (A AND B)`
- **Minimized Output:** `A`

---

### Decomposition of Expressions

**Description:** Decomposes the selected Boolean expression based on the specified variable, providing cofactors for both possible values of that variable (`0` and `1`).

**How to use:**

1. Enter the Boolean expression.
2. Select the active expression.
3. Enter the variable you want to decompose in the "`Variable to decompose`" field.
4. Click the "`Factoring in a variable`" button.
5. View the cofactors in the results display.

**Example:**

- **Expression:** `A AND B OR A AND NOT B`
- **Variable for Decomposition:** `A`
- **Cofactor for A=0:** `0`
- **Cofactor for A=1:** `B OR NOT B` (which simplifies to `1`)

---

### Generating Karnaugh Maps

**Description:** Generates and displays a Karnaugh map for the selected Boolean expression. Supported for 2 to 4 variables.

**How to use:**

1. Enter the Boolean expression.
2. Select the active expression.
3. Click the "`Generate a Karnaugh map`" button.
4. The Karnaugh map will be displayed in a new window.

**Example:**

- **Expression:** `A AND B OR A AND C`
- **Karnaugh Map:** A graphical representation showing grouped minterms for simplification.

---

### Visualization of Abstract Syntax Trees (AST)

**Description:** Visualizes the Abstract Syntax Tree of the selected Boolean expression, illustrating the hierarchical structure of the operations.

**How to use:**

1. Enter the Boolean expression.
2. Select the active expression.
3. Click the "`Visualization of AST`" button.
4. The AST will be visualized and displayed as an image.

**Example:**

- **Expression:** `A AND (B OR C)`
- **AST Visualization:** Shows `AND` as the root with `A` and `OR` as children, which in turn have `B` and `C`.

---

### Generating Circuits

**Description:** Automatically generates a digital circuit diagram from the simplified Boolean expression.

**How to use:**

1. Enter the Boolean expression.
2. Select the active expression.
3. Click the "`Generate Circuit`" button.
4. The circuit diagram will be rendered and displayed as an image.

**Example:**

- **Expression:** `A AND B OR NOT C`
- **Circuit Diagram:** Shows the AND, OR, and NOT gates, connected accordingly.

---

### Checking Equivalence Between Expressions

**Description:** Determines whether two Boolean expressions are logically equivalent by comparing their Zhegalkin polynomials and calculating the difference measure.

**How to use:**

1. Enter two Boolean expressions in the "`Expression 1`" and "`Expression 2`" fields.
2. Click the "`Equivalence check`" button.
3. View the equivalence result and the difference measure in the results display.

**Example:**

- **Expression 1:** `A OR B`
- **Expression 2:** `B OR A`
- **Result:** Equivalent.

---

### Set Operations

**Description:** Performs various set operations such as union, intersection, difference, symmetric difference, Cartesian product, power sets, and checks relations like discreteness. Supported by visual aids like Venn diagrams.

**How to use:**

1. Enter sets `A` and `B` in the respective fields, separating elements with commas.
2. Click the "`Sets`" button to open the set operations window.
3. Use the available buttons to perform the desired operations.
4. View the results and visualizations in the set operations window.

**Examples:**

- **Sets:**
  - **Set A:** `1, 2, 3`
  - **Set B:** `3, 4, 5`
  - **Union (A ∪ B):** `1, 2, 3, 4, 5`
  - **Intersection (A ∩ B):** `3`
  - **Difference (A - B):** `1, 2`
  - **Symmetric Difference (A Δ B):** `1, 2, 4, 5`
  - **Venn Diagram:** Visual representation of the intersection and union.
  - **Cartesian Product (A × B):** `{(1,3), (1,4), (1,5), (2,3), (2,4), (2,5), (3,3), (3,4), (3,5)}`
  - **Power Set of A:** `{{}, {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}}`

---

## Theoretical Background

### Boolean Algebra

Boolean algebra is a branch of mathematics dealing with variables that have two possible values: true (1) and false (0). It is fundamental in the design and analysis of digital circuits, computer programming, and various fields of engineering and computer science.

**Basic operations in Boolean algebra include:**

- **AND:** The result is true only if both variables are true.
- **OR:** The result is true if at least one of the variables is true.
- **NOT:** Inverts the value of the variable.
- **XOR (Exclusive OR):** The result is true only if exactly one of the variables is true.

Boolean algebra is used to represent and simplify logical expressions that form the basis of digital electronic circuits and computer programs.

---

### Quine-McCluskey Algorithm

The Quine-McCluskey algorithm is a method used to minimize Boolean functions. It systematically reduces a Boolean expression to its simplest form by identifying and eliminating redundant terms. This algorithm is particularly useful for functions with a large number of variables, where manual simplification becomes impractical.

**Algorithm steps:**

1. **Grouping minterms:** Minterms (terms) are grouped according to the number of 1s in their binary representation.
2. **Combining minterms:** Adjacent groups are combined, noting the differences between terms.
3. **Determining prime implicants:** Terms that cannot be combined further are identified as prime implicants.
4. **Constructing implicants:** The prime implicants are used to build the minimized expressions.

The Quine-McCluskey algorithm offers a systematic approach to minimization, ensuring the discovery of the smallest possible expression.

---

### Karnaugh Maps

A Karnaugh map (K-map) is a visual tool used to simplify Boolean expressions. By arranging minterms in a grid based on their binary representations, K-maps allow easy identification of common patterns and simplifications, reducing the complexity of Boolean functions.

**Characteristics of Karnaugh Maps:**

- **Grid structure:** K-maps are represented as a grid where rows and columns correspond to different variables.
- **Grouping of 1s:** The 1s in the map are grouped in contiguous cells, aiming for the largest possible groups (prime implicants).
- **Minimization:** By grouping, the variables that do not affect the overall result are eliminated, leading to a simpler expression.

Karnaugh maps are especially useful for functions with up to six variables, where visual representation makes finding the optimal expression easier.

---

### Zhegalkin Polynomials

A Zhegalkin polynomial is a unique representation of Boolean functions, using XOR and AND operations without using OR. It is useful in areas such as coding theory and cryptography, providing an alternative approach to Boolean function analysis.

**Features of Zhegalkin Polynomials:**

- **Binary representation:** Every Boolean expression can be represented as a Zhegalkin polynomial, which is a sum (XOR) of products (AND) of variables.
- **Linearization:** This approach enables the linearization of non-linear functions, simplifying analysis and synthesis in cryptographic systems.
- **Uniqueness:** The Zhegalkin polynomial is unique for every Boolean function, making it useful for equivalence testing.

**Example:**

- **Boolean expression:** `A XOR B`
- **Zhegalkin Polynomial:** `A ⊕ B`

Zhegalkin polynomials provide a powerful tool for working with Boolean functions, especially in the context of cryptography and information theory.

---

### Abstract Syntax Trees (AST)

An Abstract Syntax Tree (AST) is a tree representation of the abstract syntactic structure of source code or expressions. In the context of Boolean expressions, an AST visualizes the hierarchical relationships between different operations (e.g., AND, OR, NOT).

**Elements of an AST:**

- **Nodes:** Represent operations (e.g., AND, OR) or variables.
- **Children:** Represent the operands of a given operation.
- **Root:** Represents the main operation or the result of the expression.

**Example:**

For the expression `A AND (B OR C)`:

- **Root:** AND
  - **Left child:** `A`
  - **Right child:** OR
    - **Left child:** `B`
    - **Right child:** `C`

ASTs allow for the analysis and visualization of complex expressions, making it easier to understand their structure and relationships.

---

### Generating Circuits

Automatically generating digital circuits from simplified Boolean expressions enables the physical realization of logical functions in hardware. This process involves translating logical operations into interconnected logic gates, which can then be implemented on hardware platforms such as FPGAs or ASICs.

**Circuit generation process:**

1. **Expression simplification:** Using methods such as Quine-McCluskey or Karnaugh maps to minimize the expression.
2. **Translation into logic gates:** Converting the minimized expression into a combination of logic gates (AND, OR, NOT, XOR, etc.).
3. **Visualization:** Generating a graphical representation of the circuit, showing connections between the different gates.
4. **Export:** Optionally exporting the circuit in formats suitable for hardware synthesis or simulation.

Circuit generation automates the digital system design process, reducing time and errors associated with manual design.

---

### Set Operations

Set operations such as union, intersection, difference, and Cartesian product are fundamental in mathematics and computer science. Visual tools like Venn diagrams help understand the relationships between different sets and their combinations.

**Key operations:**

- **Union (∪):** Combines the elements of two sets without repetition.
- **Intersection (∩):** Returns the common elements of two sets.
- **Difference (-):** Returns the elements that are in one set but not in the other.
- **Symmetric Difference (Δ):** Returns the elements that are in exactly one of the two sets.
- **Cartesian Product (×):** Returns all possible ordered pairs from the elements of two sets.
- **Power Set (P):** Returns all possible subsets of a given set.

**Additional operations:**

- **Discreteness check:** Analyzes whether given sets are discrete according to certain criteria.
- **Visualization:** Using Venn diagrams to graphically represent the relationships between sets.

**Examples:**

- **Sets A and B:**
  - **A:** `1, 2, 3`
  - **B:** `3, 4, 5`

- **Union (A ∪ B):** `1, 2, 3, 4, 5`
- **Intersection (A ∩ B):** `3`
- **Difference (A - B):** `1, 2`
- **Symmetric Difference (A Δ B):** `1, 2, 4, 5`
- **Cartesian Product (A × B):** `{(1,3), (1,4), (1,5), (2,3), (2,4), (2,5), (3,3), (3,4), (3,5)}`
- **Power Set of A:** `{{}, {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}}`

**Visual Tools:**

- **Venn Diagrams:** Help visualize intersections and unions of sets.
- **Set operation graphs:** Allow easier understanding of complex combinations of set operations.

---
