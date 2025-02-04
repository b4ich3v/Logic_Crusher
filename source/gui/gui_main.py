import ctypes
import os
import platform
import sys
import tkinter as tk
from tkinter import messagebox
import markdown2
from tkinterweb import HtmlFrame
from PIL import Image, ImageSequence, ImageTk

from boolean_logic.boolean_functions import BooleanFunctionSet
from . import gui_actions
from . import gui_sets

function_set = BooleanFunctionSet()

root = None
first_expression_entry = None
second_expression_entry = None
active_expression = None
expression_result_display = None
variable_entry = None

BUTTON_START_X = 150    
BUTTON_START_Y = 200
BUTTON_SPACING_X = 225  
BUTTON_SPACING_Y = 50
BUTTONS_PER_ROW = 3

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def open_help_window():
    help_window = tk.Toplevel()
    help_window.title("Help window")
    help_window.geometry("800x600")

    html_frame = HtmlFrame(help_window, horizontal_scrollbar="auto")
    html_frame.pack(fill="both", expand=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    local_readme_path = os.path.join(
        current_dir, '..', '..', 
        'instructions', 'README.md'
    )

    try:
        with open(local_readme_path, "r", encoding="utf-8") as f:
            markdown_text = f.read()
        html_text = markdown2.markdown(markdown_text)
        html_frame.add_html(html_text)

    except Exception as e:
        html_frame.add_html(
            f"<h2 style='color:red'>Error while reading the file</h2><p>{e}</p>"
        )

def run():
    global root, first_expression_entry, second_expression_entry
    global active_expression, expression_result_display, variable_entry
    global function_set

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
        frames = [
            ImageTk.PhotoImage(frame.copy().resize((1000, 600), Image.LANCZOS)) 
            for frame in ImageSequence.Iterator(background_image)
        ]
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
    
    expression_label_1 = tk.Label(
        root, text="Enter boolean expression 1:", 
        bg="#ffffff", font=("Comic Sans MS", 12, "bold")
    )

    first_expression_entry = tk.Entry(
        root, width=40, 
        font=("Comic Sans MS", 12, "bold"), bg="#ffffff"
    )
    
    expression_label_2 = tk.Label(
        root, text="Enter boolean expression 2:", 
        bg="#ffffff", font=("Comic Sans MS", 12, "bold")
    )
    
    second_expression_entry = tk.Entry(
        root, width=40, 
        font=("Comic Sans MS", 12, "bold"), bg="#ffffff"
    )
    
    selection_label = tk.Label(
        root, text="Choose an active expression:", 
        bg="#ffffff", font=("Comic Sans MS", 12, "bold")
    )
    
    radio1 = tk.Radiobutton(
        root, text="Expression 1", 
        variable=active_expression, value=1, bg="#ffffff", 
        font=("Comic Sans MS", 12, "bold")
    )
    
    radio2 = tk.Radiobutton(
        root, text="Expression 2", 
        variable=active_expression, value=2, 
        bg="#ffffff", font=("Comic Sans MS", 12, "bold")
    )
    
    variable_label = tk.Label(
        root, text="Variable to decompose:", 
        bg="#ffffff", font=("Comic Sans MS", 12, "bold")
    )

    variable_entry = tk.Entry(
        root, width=20, 
        font=("Comic Sans MS", 12, "bold"), 
        bg="#ffffff"
    )
    
    result_frame = tk.Frame(
        root, bg="#ffffff", 
        bd=2, relief="groove"
    )

    expression_result_display = tk.Label(
        result_frame, text="The result will be displayed here.", 
        justify="left", wraplength=950, 
        anchor="w", bg="#ffffff", 
        font=("Comic Sans MS", 12, "bold")
    )

    expression_result_display.pack(
        fill="both", expand=True, 
        padx=10, pady=10
    )
    
    canvas.create_window(50, 20, window=expression_label_1, anchor="nw")
    canvas.create_window(300, 20, window=first_expression_entry, anchor="nw")
    
    canvas.create_window(50, 60, window=expression_label_2, anchor="nw")
    canvas.create_window(300, 60, window=second_expression_entry, anchor="nw")
    
    canvas.create_window(50, 100, window=selection_label, anchor="nw")
    canvas.create_window(300, 100, window=radio1, anchor="nw")
    canvas.create_window(450, 100, window=radio2, anchor="nw")
    
    canvas.create_window(50, 140, window=variable_label, anchor="nw")
    canvas.create_window(300, 140, window=variable_entry, anchor="nw")
    
    buttons = [
        ("Simplification", gui_actions.simplify_expression),
        ("Zhegalkin polynomial", gui_actions.zhegalkin_polynomial),
        ("Property check", gui_actions.check_properties),
        ("Minimize", gui_actions.minimize_expression),
        ("Factoring in a variable", gui_actions.decompose_expression),
        ("Generate a Karnaugh  map", gui_actions.generate_kmap),
        ("Visualization of AST", gui_actions.visualize_ast),
        ("Generate Circuit", gui_actions.generate_circuit),
        ("Equivalence check", gui_actions.check_equivalence),
    ]
    
    for index, (text, command) in enumerate(buttons):
        row = index // BUTTONS_PER_ROW
        col = index % BUTTONS_PER_ROW
        x = BUTTON_START_X + col * BUTTON_SPACING_X
        y = BUTTON_START_Y + row * BUTTON_SPACING_Y

        button = tk.Button(
            root, text=text, 
            width=25, command=command, 
            font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0"
        )

        canvas.create_window(
            x, y, 
            window=button, 
            anchor="nw"
        )
    
    save_button = tk.Button(
        root, text="Save to file", 
        width=15, command=gui_actions.save_to_file, 
        font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0"
    )

    canvas.create_window(
        720, 20, 
        window=save_button, 
        anchor="nw"
    )

    canvas.create_window(
        50, 360, 
        window=result_frame, 
        anchor="nw"
    )

    help_button = tk.Button(
        root, text="Help", 
        width=15, command=open_help_window, 
        font=("Comic Sans MS", 10, "bold"), 
        bg="#f0f0f0"
    )
    
    canvas.create_window(
        720, 60, 
        window=help_button, 
        anchor="nw"
    )

    sets_button = tk.Button(
        root, text="Sets", 
        width=15, command=gui_sets.open_sets_window, 
        font=("Comic Sans MS", 10, "bold"), 
        bg="#f0f0f0"
    )

    canvas.create_window(
        720, 100, 
        window=sets_button, 
        anchor="nw"
    )
    
    if background_image:
        root.bg_photo = frames 
    
    function_set = BooleanFunctionSet()
    root.mainloop()
