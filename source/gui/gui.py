import ctypes
import json
import os
import platform
import sys
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox

import graphviz
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles
from PIL import Image, ImageSequence, ImageTk

from boolean_logic.boolean_functions import *
from boolean_logic.gate_parser import *
from boolean_logic.karnaugh import *
from boolean_logic.validator import *

function_set = BooleanFunctionSet()

def simplify_expression():
    global first_expression_entry, second_expression_entry, active_expression, expression_result_display, function_set
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning("Error", "Please enter the selected boolean expression.")
        return
    is_valid, error_message = Validator.validate(expression_text)
    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        function_set.add_function(boolean_function)
        simplified_expression = boolean_function.simplify()
        expression_result_display.config(text=f"Simplified expression:\n{simplified_expression}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def zhegalkin_polynomial():
    global first_expression_entry, second_expression_entry, active_expression, expression_result_display, function_set
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning("Error", "Please enter the selected boolean expression.")
        return
    is_valid, error_message = Validator.validate(expression_text)
    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        function_set.add_function(boolean_function)
        zhegalkin = boolean_function.to_zhegalkin()
        expression_result_display.config(text=f"Zhegalkin polynomial:\n{zhegalkin}")
    except Exception as e:
        messagebox.showerror("Eror", str(e))

def check_properties():
    global first_expression_entry, second_expression_entry, active_expression, expression_result_display, function_set
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning("Error", "Please enter the selected boolean expression.")
        return
    is_valid, error_message = Validator.validate(expression_text)
    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        function_set.add_function(boolean_function)
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
        expression_result_display.config(text=f"Function properties:\n" + "\n".join(properties))
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def minimize_expression():
    global first_expression_entry, second_expression_entry, active_expression, expression_result_display, function_set
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning("Error", "Please enter the selected boolean expression.")
        return
    is_valid, error_message = Validator.validate(expression_text)
    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        function_set.add_function(boolean_function)
        minimized_expression = boolean_function.minimize()
        expression_result_display.config(text=f"Minimized expression:\n{minimized_expression}")
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def decompose_expression():
    global first_expression_entry, second_expression_entry, active_expression, expression_result_display, variable_entry, function_set
    expression_text = get_active_expression()
    variable = variable_entry.get()

    if not expression_text or not variable:
        messagebox.showwarning("Error", "Please enter the selected Boolean expression and decomposition variable.")
        return
    is_valid, error_message = Validator.validate(expression_text)
    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        function_set.add_function(boolean_function)
        cofactor_0, cofactor_1 = boolean_function.decompose(variable)
        expression_result_display.config(text=f"Decomposition by {variable}:\n\n"
                                 f"Cofactor at {variable}=0:\n{cofactor_0.simplify()}\n\n"
                                 f"Cofactor at {variable}=1:\n{cofactor_1.simplify()}")
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def generate_kmap():
    global first_expression_entry, second_expression_entry, active_expression, expression_result_display, function_set
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning("Error", "Please enter the selected boolean expression.")
        return
    is_valid, error_message = Validator.validate(expression_text)
    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        function_set.add_function(boolean_function)
        number_of_variables = len(boolean_function.variables)
        if number_of_variables < 2 or number_of_variables > 4:
            messagebox.showwarning("Error", "Karnaugh maps are only supported for 2 to 4 variables.")
            return
        kmap = KarnaughMap(boolean_function)
        kmap.plot_map()
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def save_to_file():
    global function_set
    functions_info = function_set.get_functions_info()

    if not functions_info:
        messagebox.showwarning("Error", "No functions to save.")
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

def visualize_ast():
    global first_expression_entry, second_expression_entry, active_expression, function_set
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning("Error", "Please enter the selected boolean expression.")
        return
    is_valid, error_message = Validator.validate(expression_text)
    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        function_set.add_function(boolean_function)
        abstract_syntax_tree = boolean_function.ast
        graph = graphviz.Digraph()
        counter = [0]
        abstract_syntax_tree.to_graphviz(graph, counter)
        graph.render("ast_output", view=True, format="png")
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def difference_measure(f1, f2):
    expression_variables = sorted(list(set(f1.variables).union(set(f2.variables))))
    difference_count = 0

    for values in product([0,1], repeat=len(expression_variables)):
        evaluation_context = dict(zip(expression_variables, values))
        f1_result = f1.evaluate(evaluation_context)
        f2_result = f2.evaluate(evaluation_context)
        if f1_result  != f2_result :
            difference_count += 1
    return difference_count

def check_equivalence():
    global first_expression_entry, second_expression_entry, active_expression, expression_result_display, function_set
    expression_text1 = first_expression_entry.get()
    expression_text2 = second_expression_entry.get()

    if not expression_text1 or not expression_text2:
        messagebox.showwarning("Error", "Please enter the two boolean expressions.")
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
        function_set.add_function(boolean_function1)
        function_set.add_function(boolean_function2)

        zhegalkin_polynomial1 = boolean_function1.to_zhegalkin()
        zhegalkin_polynomial2 = boolean_function2.to_zhegalkin()

        if zhegalkin_polynomial1 == zhegalkin_polynomial2:
            expression_result_display.config(text=f"The expressions are equivalent.\nZhegalkin polynomial:\n{zhegalkin_polynomial1}")
        else:
            difference = difference_measure(boolean_function1, boolean_function2)
            expression_result_display.config(
                text=f"The expressions are not equivalent.\n\n"
                     f"Zhegalkin polynomial of the first expression:\n{zhegalkin_polynomial1}\n"
                     f"Zhegalkin polynomial of the second expression:\n{zhegalkin_polynomial2}\n\n"
                     f"Difference measure (number of input assignments where they differ): {difference}"
            )

    except Exception as e:
        messagebox.showerror("Error.", str(e))

def get_active_expression():
    if active_expression.get() == 1:
        return first_expression_entry.get()
    elif active_expression.get() == 2:
        return second_expression_entry.get()
    return ""

def open_help_website():
    help_url = "https://github.com/b4ich3v/Logic_Crusher/tree/main/instructions" 
    webbrowser.open(help_url)

def generate_circuit():
    global first_expression_entry, second_expression_entry, active_expression, expression_result_display, function_set
    expression_text = get_active_expression()

    if not expression_text:
        messagebox.showwarning("Error", "Please enter the selected boolean expression.")
        return
    is_valid, error_message = Validator.validate(expression_text)
    if not is_valid:
        messagebox.showerror("Syntax error.", error_message)
        return
    try:
        boolean_function = BooleanFunction(expression_text)
        function_set.add_function(boolean_function)
        minimized_expression = boolean_function.minimize()
        gate_root = parse_minimized_expression(minimized_expression)
        graph = graphviz.Digraph()
        gate_ast_to_graphviz(gate_root, graph)
        graph.render("circuit_output", view=True, format="png")
    except Exception as e:
        messagebox.showerror("Error.", str(e))

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def open_sets_window():
    global root

    sets_window = tk.Toplevel(root)
    sets_window.title("Set operations")
    sets_window.geometry("900x600")
    sets_window.resizable(False, False)
    
    try:
        background_image = Image.open(resource_path("secondary_background.jpg"))
        background_image = background_image.resize((900, 600), Image.LANCZOS)  
        background_photo = ImageTk.PhotoImage(background_image)
    except Exception as e:
        messagebox.showerror("Error", f"The background image was not loaded: {str(e)}")
        background_photo = None
    
    canvas = tk.Canvas(sets_window, width=900, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    if background_photo:
        canvas.create_image(0, 0, anchor="nw", image=background_photo)
        sets_window.bg_photo = background_photo 
    else:
        canvas.configure(bg="lightgray")

    result_label_sets = tk.Label(
        sets_window,
        text="The result will be displayed here.",
        wraplength=300,
        justify="left",
        font=("Comic Sans MS", 12, "bold"),
        bg="#ffffff",
        bd=2,
        relief="groove"
    )

    canvas.create_window(
        575, 20,
        anchor="nw",
        window=result_label_sets
    )

    set1_label = tk.Label(
        sets_window,
        text="Set A (separate with commas):",
        font=("Comic Sans MS", 12, "bold"),
        bg="#ffffff"
    )
    canvas.create_window(20, 20, anchor="nw", window=set1_label)

    set1_entry = tk.Entry(
        sets_window,
        width=35,
        font=("Comic Sans MS", 12, "bold"),
        bg="#ffffff"
    )
    canvas.create_window(20, 55, anchor="nw", window=set1_entry)

    set2_label = tk.Label(
        sets_window,
        text="Set B (separate with commas):",
        font=("Comic Sans MS", 12, "bold"),
        bg="#ffffff"
    )
    canvas.create_window(20, 90, anchor="nw", window=set2_label)

    set2_entry = tk.Entry(
        sets_window,
        width=35,
        font=("Comic Sans MS", 12, "bold"),
        bg="#ffffff"
    )
    canvas.create_window(20, 125, anchor="nw", window=set2_entry)

    def sets_to_bitmasks(set1, set2):
        all_elements = sorted(set1.union(set2))
        index_map = {elm: i for i, elm in enumerate(all_elements)}
        
        bitmask1 = 0
        for current in set1:
            bitmask1 |= (1 << index_map[current])
        
        bitmask2 = 0
        for current in set2:
            bitmask2 |= (1 << index_map[current])
        
        return bitmask1, bitmask2, all_elements

    def bitmask_to_set(bitmask, all_elements):
        result = set()

        for i, current in enumerate(all_elements):
            if bitmask & (1 << i):
                result.add(current)
        return result

    def parse_set(entry):
        text = entry.get().strip()

        if not text:
            return set()
        return set(map(str.strip, text.split(',')))

    def perform_set_operation(entry1, entry2, operation):
        try:
            set1 = parse_set(entry1)
            set2 = parse_set(entry2)

            bitmask1, bitmask2, all_elements = sets_to_bitmasks(set1, set2)
            
            if operation == "union":
                result_mask = bitmask1 | bitmask2
                op_symbol = "∪"
            elif operation == "intersection":
                result_mask = bitmask1 & bitmask2
                op_symbol = "∩"
            elif operation == "difference":
                result_mask = bitmask1 & ~bitmask2
                op_symbol = "-"
            elif operation == "symmetric_difference":
                result_mask = bitmask1 ^ bitmask2
                op_symbol = "Δ"
            else:
                raise ValueError("Invalid operation.")
            
            result = bitmask_to_set(result_mask, all_elements)
            result_text = ', '.join(sorted(result)) if result else "∅ (empty set)"
            
            result_label_sets.config(text=f"Result ({op_symbol}): {result_text}")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def check_all_relations():
        try:
            set1 = parse_set(set1_entry)
            set2 = parse_set(set2_entry)
            
            bitmask1, bitmask2, all_elements = sets_to_bitmasks(set1, set2)
            
            subset_a_b = ((bitmask1 | bitmask2) == bitmask2)     
            proper_subset_a_b = subset_a_b and (bitmask1 != bitmask2)
            subset_b_a = ((bitmask2 | bitmask1) == bitmask1)     
            proper_subset_b_a = subset_b_a and (bitmask2 != bitmask1)
            is_equal = (bitmask1 == bitmask2)
            superset_a_b = subset_b_a           
            superset_b_a = subset_a_b           
            
            lines = []
            lines.append("A is a proper subset of B." if proper_subset_a_b else "A is not a proper subset of B.")
            lines.append("B is a proper subset of A." if proper_subset_b_a else "B is not a proper subset of A.")
            lines.append("A and B are equal." if is_equal else "A and B are not equal.")
            lines.append("A is a subset of B." if subset_a_b else "A is not a subset of B.")
            lines.append("B is a subset of A." if subset_b_a else "B is not a subset of A.")
            lines.append("A is a superset of B." if superset_a_b else "A is not a superset of B.")
            lines.append("B is a superset of A." if superset_b_a else "B is not a superset of A.")
            
            result_label_sets.config(text="\n".join(lines))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def perform_set_relation(entry1, entry2, relation):
        try:
            set1 = parse_set(entry1)
            set2 = parse_set(entry2)
            
            bitmask1, bitmask2, all_elements = sets_to_bitmasks(set1, set2)
            
            if relation == "disjoint":
                is_disjoint = ((bitmask1 & bitmask2) == 0)
                relation_str = ("Sets are discrete (have no elements in common)."
                                if is_disjoint
                                else "Sets are not discrete (have elements in common).")
            else:
                relation_str = "This relation is not implemented."
            
            result_label_sets.config(text=relation_str)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def power_set_both():
        try:
            set1 = parse_set(set1_entry)
            set2 = parse_set(set2_entry)
            
            all_elements1 = sorted(set1)
            set1_size = len(all_elements1)
            power_set_a = set()

            for mask in range(2**set1_size):
                subset = set()
                for i in range(set1_size):
                    if mask & (1 << i):
                        subset.add(all_elements1[i])
                power_set_a.add(frozenset(subset))
            
            power_set_str_a = ', '.join(
                f"{{{', '.join(sorted(x))}}}" for x in power_set_a
            ) if power_set_a else "{}"
            
            all_elements2 = sorted(set2)
            set2_size = len(all_elements2)
            power_set_b = set()

            for mask in range(2**set2_size):
                subset = set()
                for i in range(set2_size):
                    if mask & (1 << i):
                        subset.add(all_elements2[i])
                power_set_b.add(frozenset(subset))
            
            power_set_str_b = ', '.join(
                f"{{{', '.join(sorted(x))}}}" for x in power_set_b
            ) if power_set_b else "{}"
            
            output = (f"Power Set for A:\n{power_set_str_a}\n\n"
                      f"Power Set for B:\n{power_set_str_b}")
            result_label_sets.config(text=output)
    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def plot_venn():
        try:
            set1 = parse_set(set1_entry)
            set2 = parse_set(set2_entry)
            
            if not set1 and not set2:
                messagebox.showwarning("Warning", "Please enter at least one set.")
                return
            
            plt.figure(figsize=(8, 6))
            venn_figure = venn2([set1, set2], set_labels=("Set A", "Set B"))
            venn2_circles([set1, set2], linestyle="dotted")
            plt.title("Venn diagram")
            
            label_set1_only = venn_figure.get_label_by_id("10")
            if label_set1_only:
                text_s1_only = ", ".join(sorted(set1 - set2))
                label_set1_only.set_text(text_s1_only if text_s1_only else "∅")
            
            label_set2_only = venn_figure.get_label_by_id("01")
            if label_set2_only:
                text_s2_only = ", ".join(sorted(set2 - set1))
                label_set2_only.set_text(text_s2_only if text_s2_only else "∅")
            
            label_intersect = venn_figure.get_label_by_id("11")
            if label_intersect:
                text_intersect = ", ".join(sorted(set1 & set2))
                label_intersect.set_text(text_intersect if text_intersect else "∅")
            
            plt.show()
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while rendering the Venn diagram: {str(e)}")

    def cartesian_product(entry1, entry2):
        try:
            set1 = parse_set(entry1)
            set2 = parse_set(entry2)

            list_A = sorted(set1)
            list_B = sorted(set2)

            product = [(a, b) for a in list_A for b in list_B]

            if product:
                product_str = ', '.join(f"({p[0]}, {p[1]})" for p in product)
            else:
                product_str = "Empty product."

            result_label_sets.config(text=f"Cartesian product (A × B): {product_str}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating the Cartesian product: {str(e)}")

    def cardinality(entry1, entry2):
        try:
            set1 = parse_set(entry1)
            set2 = parse_set(entry2)
            count1 = len(set1)
            count2 = len(set2)
            result_label_sets.config(
                text=f"Cardinality of A: {count1}\n"
                     f"Cardinality of B: {count2}"
            )
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating the cardinality: {str(e)}")

    btn_union = tk.Button(
        sets_window,
        text="Union (A ∪ B)",
        width=35,
        font=("Comic Sans MS", 10, "bold"),
        bg="#f0f0f0",
        command=lambda: perform_set_operation(set1_entry, set2_entry, "union")
    )
    canvas.create_window(60, 170, anchor="nw", window=btn_union)

    btn_intersect = tk.Button(
        sets_window,
        text="Intersection (A ∩ B)",
        width=35,
        font=("Comic Sans MS", 10, "bold"),
        bg="#f0f0f0",
        command=lambda: perform_set_operation(set1_entry, set2_entry, "intersection")
    )
    canvas.create_window(60, 212, anchor="nw", window=btn_intersect)

    btn_diff = tk.Button(
        sets_window,
        text="Difference (A - B)",
        width=35,
        font=("Comic Sans MS", 10, "bold"),
        bg="#f0f0f0",
        command=lambda: perform_set_operation(set1_entry, set2_entry, "difference")
    )
    canvas.create_window(60, 255, anchor="nw", window=btn_diff)

    btn_symdiff = tk.Button(
        sets_window,
        text="Symmetric difference (A Δ B)",
        width=35,
        font=("Comic Sans MS", 10, "bold"),
        bg="#f0f0f0",
        command=lambda: perform_set_operation(set1_entry, set2_entry, "symmetric_difference")
    )
    canvas.create_window(60, 298, anchor="nw", window=btn_symdiff)

    venn_button = tk.Button(
        sets_window,
        text="Venn diagram",
        width=35,
        font=("Comic Sans MS", 10, "bold"),
        bg="#f0f0f0",
        command=plot_venn
    )
    canvas.create_window(60, 341, anchor="nw", window=venn_button)

    btn_disjoint = tk.Button(
        sets_window,
        text="Discretion check",
        width=35,
        font=("Comic Sans MS", 10, "bold"),
        bg="#f0f0f0",
        command=lambda: perform_set_relation(set1_entry, set2_entry, "disjoint")
    )
    canvas.create_window(60, 384, anchor="nw", window=btn_disjoint)

    btn_cartprod = tk.Button(
        sets_window,
        text="Cartesian product (A × B)",
        width=35,
        font=("Comic Sans MS", 10, "bold"),
        bg="#f0f0f0",
        command=lambda: cartesian_product(set1_entry, set2_entry)
    )
    canvas.create_window(60, 427, anchor="nw", window=btn_cartprod)

    btn_cardinality = tk.Button(
        sets_window,
        text="Cardinality",
        width=35,
        font=("Comic Sans MS", 10, "bold"),
        bg="#f0f0f0",
        command=lambda: cardinality(set1_entry, set2_entry)
    )
    canvas.create_window(60, 470, anchor="nw", window=btn_cardinality)

    btn_power = tk.Button(
        sets_window,
        text="Power Set of A and B",
        width=35,
        font=("Comic Sans MS", 10, "bold"),
        bg="#f0f0f0",
        command=power_set_both
    )
    canvas.create_window(60, 513, anchor="nw", window=btn_power)

    btn_relations = tk.Button(
        sets_window,
        text="Relations between A and B",
        width=35,
        font=("Comic Sans MS", 10, "bold"),
        bg="#f0f0f0",
        command=check_all_relations
    )
    canvas.create_window(60, 556, anchor="nw", window=btn_relations)

def run():
    global root, first_expression_entry, second_expression_entry, active_expression, expression_result_display, variable_entry, function_set

    root = tk.Tk()
    root.title("Logic crusher")
    root.geometry("1000x600")
    root.resizable(False, False)
    
    if platform.system() == "Windows":
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
        style &= ~0x10000  
        ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
    
    canvas = tk.Canvas(root, width=1000, height=600)
    canvas.pack(fill="both", expand=True)
    
    try:
        background_image = Image.open(resource_path("main_background.gif"))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load background image: {e}")
        background_image = None

    if background_image:
        frames = [ImageTk.PhotoImage(frame.copy().resize((1000, 600), Image.LANCZOS)) for frame in ImageSequence.Iterator(background_image)]
        frame_count = len(frames)
        current_frame = 0

        background_label = canvas.create_image(0, 0, image=frames[0], anchor="nw")

        def update_background():
            nonlocal current_frame
            current_frame = (current_frame + 1) % frame_count
            canvas.itemconfig(background_label, image=frames[current_frame])
            root.after(100, update_background)  

        root.after(0, update_background)
    
    active_expression = tk.IntVar(value=1) 
    
    expression_label_1 = tk.Label(root, text="Enter boolean expression 1:", bg="#ffffff", font=("Comic Sans MS", 12, "bold"))
    first_expression_entry = tk.Entry(root, width=40, font=("Comic Sans MS", 12, "bold"), bg="#ffffff")
    
    expression_label_2 = tk.Label(root, text="Enter boolean expression 2:", bg="#ffffff", font=("Comic Sans MS", 12, "bold"))
    second_expression_entry = tk.Entry(root, width=40, font=("Comic Sans MS", 12, "bold"), bg="#ffffff")
    
    selection_label = tk.Label(root, text="Choose an active expression:", bg="#ffffff", font=("Comic Sans MS", 12, "bold"))
    radio1 = tk.Radiobutton(root, text="Expression 1", variable=active_expression, value=1, bg="#ffffff", font=("Comic Sans MS", 12, "bold"))
    radio2 = tk.Radiobutton(root, text="Expression 2", variable=active_expression, value=2, bg="#ffffff", font=("Comic Sans MS", 12, "bold"))
    
    variable_label = tk.Label(root, text="Variable to decompose:", bg="#ffffff", font=("Comic Sans MS", 12, "bold"))
    variable_entry = tk.Entry(root, width=20, font=("Comic Sans MS", 12, "bold"), bg="#ffffff")
    
    result_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
    expression_result_display = tk.Label(result_frame, text="The result will be displayed here.", justify="left", wraplength=950, anchor="w", bg="#ffffff", font=("Comic Sans MS", 12, "bold"))
    expression_result_display.pack(fill="both", expand=True, padx=10, pady=10)
    
    canvas.create_window(50, 20, window=expression_label_1, anchor="nw")
    canvas.create_window(300, 20, window=first_expression_entry, anchor="nw")
    
    canvas.create_window(50, 60, window=expression_label_2, anchor="nw")
    canvas.create_window(300, 60, window=second_expression_entry, anchor="nw")
    
    canvas.create_window(50, 100, window=selection_label, anchor="nw")
    canvas.create_window(300, 100, window=radio1, anchor="nw")
    canvas.create_window(450, 100, window=radio2, anchor="nw")
    
    canvas.create_window(50, 140, window=variable_label, anchor="nw")
    canvas.create_window(300, 140, window=variable_entry, anchor="nw")
    
    BUTTON_START_X = 150    
    BUTTON_START_Y = 200
    BUTTON_SPACING_X = 225  
    BUTTON_SPACING_Y = 50
    BUTTONS_PER_ROW = 3
    
    buttons = [
        ("Simplification", simplify_expression),
        ("Zhegalkin polynomial", zhegalkin_polynomial),
        ("Property Check", check_properties),
        ("Minimize", minimize_expression),
        ("Factoring in a variable", decompose_expression),
        ("Generate a Karnaugh  map", generate_kmap),
        ("Visualization of AST", visualize_ast),
        ("Generate Circuit", generate_circuit),
        ("Equivalence check", check_equivalence),
    ]
    
    for index, (text, command) in enumerate(buttons):
        row = index // BUTTONS_PER_ROW
        col = index % BUTTONS_PER_ROW
        x = BUTTON_START_X + col * BUTTON_SPACING_X
        y = BUTTON_START_Y + row * BUTTON_SPACING_Y
        button = tk.Button(root, text=text, width=25, command=command, font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0")
        canvas.create_window(x, y, window=button, anchor="nw")
    
    save_button = tk.Button(root, text="Save to file", width=15, command=save_to_file, font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0")
    canvas.create_window(720, 20, window=save_button, anchor="nw")
    canvas.create_window(50, 360, window=result_frame, anchor="nw")

    help_button = tk.Button(root, text="Help", width=15, command=open_help_website, font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0")
    canvas.create_window(720, 60, window=help_button, anchor="nw")

    sets_button = tk.Button(root, text="Sets", width=15, command=open_sets_window, font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0")
    canvas.create_window(720, 100, window=sets_button, anchor="nw")
    
    if background_image:
        root.bg_photo = frames 
    
    function_set = BooleanFunctionSet()
    root.mainloop()
