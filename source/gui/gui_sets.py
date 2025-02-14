import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles
from PIL import Image, ImageTk

from gui import constants as cn
from . import gui_main

def open_sets_window():
    """Open a new window for performing set operations and visualizations."""
    sets_window = tk.Toplevel(gui_main.root)
    sets_window.title(cn.SECONDARY_TITTLE)
    sets_window.geometry(f"{cn.SET_WINDOW_WIDTH}x{cn.SET_WINDOW_HEIGHT}")
    sets_window.resizable(False, False)
    
    try:
        background_image = Image.open(gui_main.resource_path(cn.SECONDARY_BG_IMAGE))
        background_image = background_image.resize(
            (cn.BACKGROUND_IM_WIDTH, cn.BACKGROUND_IM_HEIGHT), Image.LANCZOS
        )  
        background_photo = ImageTk.PhotoImage(background_image)
    except Exception as e:
        messagebox.showerror("Error", f"The background image was not loaded: {str(e)}")
        background_photo = None
    
    canvas = tk.Canvas(
        sets_window, 
        width=cn.SET_WINDOW_WIDTH, 
        height=cn.SET_WINDOW_HEIGHT, 
        highlightthickness=0
    )

    canvas.pack(fill="both", expand=True)
    
    if background_photo:
        canvas.create_image(0, 0, anchor="nw", image=background_photo)
        sets_window.bg_photo = background_photo 
    else:
        canvas.configure(bg="lightgray")

    result_label_sets = tk.Label(
        sets_window, 
        text=cn.RESULT_PLACEHOLDER,
        wraplength=cn.RESULT_LABEL_WRAP, 
        justify="left",
        font=cn.LABEL_FONT, 
        bg=cn.LABEL_BG_COLOR,
        bd=cn.RESULT_LABEL_BORDER_WIDTH, 
        relief="groove"
    )

    canvas.create_window(
        cn.RESULT_LABEL_X, 
        cn.RESULT_LABEL_Y, 
        anchor="nw",
        window=result_label_sets
    )

    set1_label = tk.Label(
        sets_window, 
        text="Set A (separate with commas):",
        font=cn.LABEL_FONT, 
        bg=cn.LABEL_BG_COLOR
    )

    canvas.create_window(
        cn.SET1_LABEL_X, 
        cn.SET1_LABEL_Y, 
        anchor="nw", 
        window=set1_label
    )

    set1_entry = tk.Entry(
        sets_window, 
        width=cn.SET_ENTRY_WIDTH,
        font=cn.ENTRY_FONT,
        bg=cn.ENTRY_BG_COLOR
    )
    
    canvas.create_window(
        cn.SET1_ENTRY_X, 
        cn.SET1_ENTRY_Y, 
        anchor="nw", 
        window=set1_entry
    )

    set2_label = tk.Label(
        sets_window, 
        text="Set B (separate with commas):",
        font=cn.LABEL_FONT, 
        bg=cn.LABEL_BG_COLOR
    )

    canvas.create_window(
        cn.SET2_LABEL_X, 
        cn.SET2_LABEL_Y, 
        anchor="nw", 
        window=set2_label
    )

    set2_entry = tk.Entry(
        sets_window, 
        width=cn.SET_ENTRY_WIDTH,
        font=cn.ENTRY_FONT,
        bg=cn.ENTRY_BG_COLOR
    )

    canvas.create_window(
        cn.SET2_ENTRY_X, 
        cn.SET2_ENTRY_Y, 
        anchor="nw", 
        window=set2_entry
    )

    def sets_to_bitmasks(set1, set2):
        """Convert two sets into their bitmask representations 
        and return both bitmasks along with the sorted list of all unique elements."""
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
        """Convert a bitmask back into a set of elements using the provided list of all elements."""
        result = set()

        for i, current in enumerate(all_elements):
            if bitmask & (1 << i):
                result.add(current)
        return result

    def parse_set(entry):
        """Parse the text from an Entry widget into a set of strings."""
        text = entry.get().strip()

        if not text:
            return set()
        return set(map(str.strip, text.split(',')))

    def perform_set_operation(entry1, entry2, operation):
        """Perform a set operation (union, intersection, difference, or symmetric difference) on two sets."""
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
        """Check and display various relational properties 
        between set A and set B, such as subset, proper subset, equality, and superset."""
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
            lines.append(
                "A is a proper subset of B." 
                if proper_subset_a_b 
                else "A is not a proper subset of B."
            )
            lines.append(
                "B is a proper subset of A." 
                if proper_subset_b_a 
                else "B is not a proper subset of A."
            )
            lines.append("A and B are equal." if is_equal else "A and B are not equal.")
            lines.append("A is a subset of B." if subset_a_b else "A is not a subset of B.")
            lines.append("B is a subset of A." if subset_b_a else "B is not a subset of A.")
            lines.append("A is a superset of B." if superset_a_b else "A is not a superset of B.")
            lines.append("B is a superset of A." if superset_b_a else "B is not a superset of A.")
            
            result_label_sets.config(text="\n".join(lines))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def perform_set_relation(entry1, entry2, relation):
        """Check a specific relation between two sets (currently supports checking if they are disjoint)."""
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
        """Calculate and display the power sets of both set A and set B."""
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
            
            power_set_str_a = ", ".join(
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
        """Generate and display a Venn diagram for sets A and B."""
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
            messagebox.showerror(
                "Error", f"An error occurred while rendering the Venn diagram: {str(e)}"
            )

    def cartesian_product(entry1, entry2):
        """Calculate the Cartesian product of the two sets from the given Entry widgets."""
        try:
            set1 = parse_set(entry1)
            set2 = parse_set(entry2)

            list_1 = sorted(set1)
            list_2 = sorted(set2)

            product = [(a, b) for a in list_1 for b in list_2]

            if product:
                product_str = ', '.join(f"({p[0]}, {p[1]})" for p in product)
            else:
                product_str = "Empty product."

            result_label_sets.config(text=f"Cartesian product (A × B): {product_str}")

        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while calculating the Cartesian product: {str(e)}"
            )

    def cardinality(entry1, entry2):
        """Calculate and display the cardinality (number of elements) of set A and set B."""
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
            messagebox.showerror(
                "Error", f"An error occurred while calculating the cardinality: {str(e)}"
            )

    btn_union = tk.Button(
        sets_window, 
        text="Union (A ∪ B)",
        width=cn.BUTTON_WIDTH_LARGE, 
        font=cn.BUTTON_FONT,
        bg=cn.BUTTON_BG_COLOR, 
        command=lambda: perform_set_operation(set1_entry, set2_entry, "union")
    )

    canvas.create_window(
        cn.BUTTON_X_FOR_SETS, 
        cn.BTN_UNION_Y, 
        anchor="nw", 
        window=btn_union
    )

    btn_intersect = tk.Button(
        sets_window, 
        text="Intersection (A ∩ B)",
        width=cn.BUTTON_WIDTH_LARGE, 
        font=cn.BUTTON_FONT,
        bg=cn.BUTTON_BG_COLOR, 
        command=lambda: perform_set_operation(set1_entry, set2_entry, "intersection")
    )

    canvas.create_window(
        cn.BUTTON_X_FOR_SETS, 
        cn.BTN_INTERSECT_Y, 
        anchor="nw", 
        window=btn_intersect
    )

    btn_diff = tk.Button(
        sets_window, 
        text="Difference (A - B)",
        width=cn.BUTTON_WIDTH_LARGE, 
        font=cn.BUTTON_FONT,
        bg=cn.BUTTON_BG_COLOR, 
        command=lambda: perform_set_operation(set1_entry, set2_entry, "difference")
    )

    canvas.create_window(
        cn.BUTTON_X_FOR_SETS, 
        cn.BTN_DIFF_Y, 
        anchor="nw", 
        window=btn_diff
    )

    btn_symdiff = tk.Button(
        sets_window, 
        text="Symmetric difference (A Δ B)",
        width=cn.BUTTON_WIDTH_LARGE, 
        font=cn.BUTTON_FONT,
        bg=cn.BUTTON_BG_COLOR,
        command=lambda: perform_set_operation(set1_entry, set2_entry, "symmetric_difference")
    )

    canvas.create_window(
        cn.BUTTON_X_FOR_SETS, 
        cn.BTN_SYMDIFF_Y, 
        anchor="nw", 
        window=btn_symdiff
    )

    venn_button = tk.Button(
        sets_window, 
        text="Venn diagram",
        width=cn.BUTTON_WIDTH_LARGE, 
        font=cn.BUTTON_FONT,
        bg=cn.BUTTON_BG_COLOR, 
        command=plot_venn
    )

    canvas.create_window(
        cn.BUTTON_X_FOR_SETS, 
        cn.BTN_VENN_Y, 
        anchor="nw", 
        window=venn_button
    )

    btn_disjoint = tk.Button(
        sets_window, 
        text="Discretion check",
        width=cn.BUTTON_WIDTH_LARGE, 
        font=cn.BUTTON_FONT,
        bg=cn.BUTTON_BG_COLOR, 
        command=lambda: perform_set_relation(set1_entry, set2_entry, "disjoint")
    )
    
    canvas.create_window(
        cn.BUTTON_X_FOR_SETS, 
        cn.BTN_DISJOINT_Y, 
        anchor="nw", 
        window=btn_disjoint
    )

    btn_cartprod = tk.Button(
        sets_window, 
        text="Cartesian product (A × B)",
        width=cn.BUTTON_WIDTH_LARGE, 
        font=cn.BUTTON_FONT,
        bg=cn.BUTTON_BG_COLOR, 
        command=lambda: cartesian_product(set1_entry, set2_entry)
    )
    
    canvas.create_window(
        cn.BUTTON_X_FOR_SETS, 
        cn.BTN_CARTPROD_Y, 
        anchor="nw", 
        window=btn_cartprod
    )

    btn_cardinality = tk.Button(
        sets_window, 
        text="Cardinality",
        width=cn.BUTTON_WIDTH_LARGE, 
        font=cn.BUTTON_FONT,
        bg=cn.BUTTON_BG_COLOR, 
        command=lambda: cardinality(set1_entry, set2_entry)
    )
    
    canvas.create_window(
        cn.BUTTON_X_FOR_SETS, 
        cn.BTN_CARDINALITY_Y, 
        anchor="nw", 
        window=btn_cardinality
    )

    btn_power = tk.Button(
        sets_window, 
        text="Power Set of A and B",
        width=cn.BUTTON_WIDTH_LARGE, 
        font=cn.BUTTON_FONT,
        bg=cn.BUTTON_BG_COLOR, 
        command=power_set_both
    )

    canvas.create_window(
        cn.BUTTON_X_FOR_SETS, 
        cn.BTN_POWER_Y, 
        anchor="nw", 
        window=btn_power
    )

    btn_relations = tk.Button(
        sets_window, 
        text="Relations between A and B",
        width=cn.BUTTON_WIDTH_LARGE, 
        font=cn.BUTTON_FONT,
        bg=cn.BUTTON_BG_COLOR, 
        command=check_all_relations
    )

    canvas.create_window(
        cn.BUTTON_X_FOR_SETS, 
        cn.BTN_RELATIONS_Y, 
        anchor="nw", 
        window=btn_relations
    )
