import json
from itertools import product
from tkinter import messagebox, filedialog
import graphviz

from boolean_logic.boolean_functions import BooleanFunction
from boolean_logic.validator import Validator
from boolean_logic.karnaugh import KarnaughMap
from boolean_logic.gate_parser import parse_minimized_expression, gate_ast_to_graphviz

from . import gui_main

def get_active_expression():
    if gui_main.active_expression.get() == 1:
        return gui_main.first_expression_entry.get()
    elif gui_main.active_expression.get() == 2:
        return gui_main.second_expression_entry.get()
    return ""

def simplify_expression():
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning(
            "Error", "Please enter the selected boolean expression."
            )
        return
    
    is_valid, error_message = Validator.validate(expression_text)

    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        gui_main.function_set.add_function(boolean_function)
        simplified_expression = boolean_function.simplify()
        gui_main.expression_result_display.config(
            text=f"Simplified expression:\n{simplified_expression}"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))

def zhegalkin_polynomial():
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning(
            "Error", "Please enter the selected boolean expression."
            )
        return
    
    is_valid, error_message = Validator.validate(expression_text)

    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        gui_main.function_set.add_function(boolean_function)
        zhegalkin = boolean_function.to_zhegalkin()
        gui_main.expression_result_display.config(
            text=f"Zhegalkin polynomial:\n{zhegalkin}"
            )
    except Exception as e:
        messagebox.showerror("Eror", str(e))

def check_properties():
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning(
            "Error", "Please enter the selected boolean expression."
            )
        return
    
    is_valid, error_message = Validator.validate(expression_text)

    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        gui_main.function_set.add_function(boolean_function)
        properties = []

        if boolean_function.preserves_zero():
            properties.append("Preserves the zero.")
        else:
            properties.append("Does not preserve zero.")
        if boolean_function.preserves_one():
            properties.append("Preserves the one.")
        else:
            properties.append("Does not preserve the one.")
        if boolean_function.is_self_dual():
            properties.append("Self-dual.")
        else:
            properties.append("It is not self-dual.")
        if boolean_function.is_monotonic():
            properties.append("Monotonous.")
        else:
            properties.append("It is not monotonous.")
        if boolean_function.is_linear():
            properties.append("Linear.")
        else:
            properties.append("Non-linear.")

        gui_main.expression_result_display.config(
            text=f"Function properties:\n" + "\n".join(properties)
            )
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def minimize_expression():
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning(
            "Error", "Please enter the selected boolean expression."
            )
        return
    
    is_valid, error_message = Validator.validate(expression_text)

    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        gui_main.function_set.add_function(boolean_function)
        minimized_expression = boolean_function.minimize()
        gui_main.expression_result_display.config(
            text=f"Minimized expression:\n{minimized_expression}"
            )
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def decompose_expression():
    expression_text = get_active_expression()
    variable = gui_main.variable_entry.get()

    if not expression_text or not variable:
        messagebox.showwarning(
            "Error", "Please enter the selected Boolean expression and decomposition variable."
            )
        return
    
    is_valid, error_message = Validator.validate(expression_text)

    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        gui_main.function_set.add_function(boolean_function)
        cofactor_0, cofactor_1 = boolean_function.decompose(variable)
        gui_main.expression_result_display.config(
            text=f"Decomposition by {variable}:\n\n"
            f"Cofactor at {variable}=0:\n{cofactor_0.simplify()}\n\n"
            f"Cofactor at {variable}=1:\n{cofactor_1.simplify()}"
            )
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def generate_kmap():
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning(
            "Error", "Please enter the selected boolean expression."
            )
        return
    
    is_valid, error_message = Validator.validate(expression_text)

    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        gui_main.function_set.add_function(boolean_function)
        number_of_variables = len(boolean_function.variables)
        if number_of_variables < 2 or number_of_variables > 4:
            messagebox.showwarning(
                "Error", "Karnaugh maps are only supported for 2 to 4 variables."
                )
            return
    
        kmap = KarnaughMap(boolean_function)
        kmap.plot_map()

    except Exception as e:
        messagebox.showerror("Error.", str(e))

def visualize_ast():
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning(
            "Error", "Please enter the selected boolean expression."
            )
        return
    
    is_valid, error_message = Validator.validate(expression_text)

    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        gui_main.function_set.add_function(boolean_function)
        abstract_syntax_tree = boolean_function.ast
        graph = graphviz.Digraph()
        counter = [0]
        abstract_syntax_tree.to_graphviz(graph, counter)
        graph.render("ast_output", view=True, format="png")
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def generate_circuit():
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning(
            "Error", "Please enter the selected boolean expression."
            )
        return
    
    is_valid, error_message = Validator.validate(expression_text)

    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        gui_main.function_set.add_function(boolean_function)
        minimized_expression = boolean_function.minimize()
        gate_root = parse_minimized_expression(minimized_expression)
        graph = graphviz.Digraph()
        gate_ast_to_graphviz(gate_root, graph)
        graph.render("circuit_output", view=True, format="png")
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def difference_measure(f1, f2):
    expression_variables = sorted(list(set(f1.variables).union(set(f2.variables))))
    difference_count = 0

    for values in product([0, 1], repeat=len(expression_variables)):
        evaluation_context = dict(zip(expression_variables, values))
        f1_result = f1.evaluate(evaluation_context)
        f2_result = f2.evaluate(evaluation_context)
        if f1_result != f2_result:
            difference_count += 1

    return difference_count

def check_equivalence():
    expression_text1 = gui_main.first_expression_entry.get()
    expression_text2 = gui_main.second_expression_entry.get()

    if not expression_text1 or not expression_text2:
        messagebox.showwarning(
            "Error", "Please enter the two boolean expressions."
            )
        return

    is_valid1, error1 = Validator.validate(expression_text1)
    is_valid2, error2 = Validator.validate(expression_text2)

    if not is_valid1:
        messagebox.showerror("Syntax error in the first expression.", error1)
        return
    if not is_valid2:
        messagebox.showerror("Syntax error in the second expression.", error2)
        return

    try:
        boolean_function1 = BooleanFunction(expression_text1)
        boolean_function2 = BooleanFunction(expression_text2)
        gui_main.function_set.add_function(boolean_function1)
        gui_main.function_set.add_function(boolean_function2)

        zhegalkin_polynomial1 = boolean_function1.to_zhegalkin()
        zhegalkin_polynomial2 = boolean_function2.to_zhegalkin()

        if zhegalkin_polynomial1 == zhegalkin_polynomial2:
            gui_main.expression_result_display.config(
                text=f"The expressions are equivalent.\n"
                     f"Zhegalkin polynomial:\n{zhegalkin_polynomial1}"
            )
        else:
            difference = difference_measure(boolean_function1, boolean_function2)
            gui_main.expression_result_display.config(
                text=(
                    f"The expressions are not equivalent.\n\n"
                    f"Zhegalkin polynomial of the first expression:\n{zhegalkin_polynomial1}\n"
                    f"Zhegalkin polynomial of the second expression:\n{zhegalkin_polynomial2}\n\n"
                    f"Difference measure (number of input assignments where they differ): {difference}"
                )
            )
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def save_to_file():
    functions_info = gui_main.function_set.get_functions_info()
    
    if not functions_info:
        messagebox.showwarning(
            "Error", "No functions to save."
            )
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".json",
    filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
    
    if not file_path:
        return  

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(functions_info, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Success", f"The information is saved in the file: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write to file: {str(e)}")
