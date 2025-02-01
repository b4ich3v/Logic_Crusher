class GateNode:
    """
    Represents a node in a logic gate AST, storing a gate type
    (e.g., "AND", "OR", "NOT", or "VAR") and its child nodes.
    """

    def __init__(self, gate_type, children=None):
        self.gate_type = gate_type  
        self.children = children if children else []


def parse_minimized_expression(expression):
    """
    Parse a minimized Boolean expression (e.g., "A AND B", "(NOT A) OR B")
    into a GateNode AST structure suitable for further processing or visualization.
    """
    expression = expression.strip()

    if expression.isalnum() or expression in ("1", "0"):
        return GateNode("VAR", [expression])

    if expression.startswith("(") and expression.endswith(")"):
        count = 0
        remove = True

        for i, ch in enumerate(expression):
            if ch == "(":
                count += 1
            elif ch == ")":
                count -= 1
            if count == 0 and i < len(expression) - 1:
                remove = False
                break
        if remove:
            expression = expression[1:-1].strip()

    def find_top_level_operator(expression):
        count = 0

        for i, ch in enumerate(expression):
            if ch == "(":
                count += 1
            elif ch == ")":
                count -= 1
            else:
                if count == 0:
                    if expression[i:].startswith("AND"):
                        next_index = i + 3
                        if next_index >= len(expression) or expression[next_index] in (" ", "("):
                            return "AND", i
                    if expression[i:].startswith("OR"):
                        next_index = i + 2
                        if next_index >= len(expression) or expression[next_index] in (" ", "("):
                            return "OR", i
        return None, None

    operator, index = find_top_level_operator(expression)

    if operator is not None:
        if operator == "AND":
            left = expression[:index].strip()
            right = expression[index+3:].strip()

            if right.startswith(" "):
                right = right[1:].strip()

            left_node = parse_minimized_expression(left)
            right_node = parse_minimized_expression(right)

            return GateNode("AND", [left_node, right_node])

        elif operator == "OR":
            left = expression[:index].strip()
            right = expression[index+2:].strip()

            if right.startswith(" "):
                right = right[1:].strip()

            left_node = parse_minimized_expression(left)
            right_node = parse_minimized_expression(right)

            return GateNode("OR", [left_node, right_node])

    if expression.startswith("NOT"):
        sub_expression = expression[3:].strip()

        if sub_expression.startswith("(") and sub_expression.endswith(")"):
            pass
        child = parse_minimized_expression(sub_expression)
        return GateNode("NOT", [child])

    if expression.startswith("NOT("):
        sub_expression = expression[3:].strip()
        if sub_expression.startswith("(") and sub_expression.endswith(")"):
            sub_expression = sub_expression[1:-1].strip()

        child = parse_minimized_expression(sub_expression)
        return GateNode("NOT", [child])

    raise Exception(f"Cannot parse expression: {expression}")

def gate_ast_to_graphviz(node, graph):
    """
    Recursively add the given GateNode (and any children) to a graphviz Digraph.
    Each node is drawn as a box or circle (for variables), with edges to its children.
    """
    node_id = str(id(node))

    if node.gate_type == "VAR":
        graph.node(node_id, node.children[0], shape="circle")
    else:
        graph.node(node_id, node.gate_type, shape="box")

    for child in node.children:
        if isinstance(child, GateNode):
            child_id = gate_ast_to_graphviz(child, graph)
            graph.edge(node_id, child_id)
        else:
            c_id = str(id(child))
            graph.node(c_id, str(child), shape="circle")
            graph.edge(node_id, c_id)
            
    return node_id
