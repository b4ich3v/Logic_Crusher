class GateNode:
    def __init__(self, gate_type, children=None):
        self.gate_type = gate_type  
        self.children = children if children else []

def parse_minimized_expression(expr):
    expr = expr.strip()
    
    if expr.isalnum() or expr in ("1","0"):
        return GateNode("VAR", [expr])

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
            expr = expr[1:-1].strip()

    if expr.startswith("NOT "):
        sub_expr = expr[4:].strip()
        child = parse_minimized_expression(sub_expr)
        return GateNode("NOT", [child])

    def find_top_level_operator(expression):
        count = 0
        operators = []
        for i, ch in enumerate(expression):
            if ch == '(':
                count += 1
            elif ch == ')':
                count -= 1
            else:
                if count == 0:
                    if expression[i:].startswith("AND "):
                        return "AND", i
                    if expression[i:].startswith("OR "):
                        return "OR", i
        return None, None

    op, idx = find_top_level_operator(expr)
    if op is not None:
        if op == "AND":
            left = expr[:idx].strip()
            right = expr[idx+4:].strip() 
            left_node = parse_minimized_expression(left)
            right_node = parse_minimized_expression(right)
            return GateNode("AND", [left_node, right_node])
        elif op == "OR":
            left = expr[:idx].strip()
            right = expr[idx+3:].strip() 
            left_node = parse_minimized_expression(left)
            right_node = parse_minimized_expression(right)
            return GateNode("OR", [left_node, right_node])

    if expr.startswith("NOT("):
        sub_expr = expr[3:].strip()
        if sub_expr.startswith("(") and sub_expr.endswith(")"):
            sub_expr = sub_expr[1:-1].strip()
        child = parse_minimized_expression(sub_expr)
        return GateNode("NOT", [child])

    raise Exception(f"Cannot parse expression: {expr}")

def gate_ast_to_graphviz(node, dot):
    node_id = str(id(node))
    if node.gate_type == "VAR":
        dot.node(node_id, node.children[0], shape="circle")
    else:
        dot.node(node_id, node.gate_type, shape="box")

    for child in node.children:
        if isinstance(child, GateNode):
            child_id = gate_ast_to_graphviz(child, dot)
            dot.edge(node_id, child_id)
        else:
            c_id = str(id(child))
            dot.node(c_id, str(child), shape="circle")
            dot.edge(node_id, c_id)
    return node_id