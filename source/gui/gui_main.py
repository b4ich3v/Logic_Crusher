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

MAIN_WINDOW_WIDTH = 1000
MAIN_WINDOW_HEIGHT = 600

HELP_WINDOW_WIDTH = 800
HELP_WINDOW_HEIGHT = 600

BACKGROUND_WIDTH = 1000
BACKGROUND_HEIGHT = 600

BUTTON_WIDTH_1 = 25
BUTTON_WIDTH_2 = 15
BUTTON_BG_COLOR = "#f0f0f0"
BUTTON_FONT = ("Comic Sans MS", 10, "bold")

ENTRY_WIDTH_1 = 40
ENTRY_WIDTH_2 = 20
ENTRY_FONT = ("Comic Sans MS", 12, "bold")
ENTRY_BG_COLOR = "#ffffff"

LABEL_BG_COLOR = "#ffffff"
LABEL_FONT = ("Comic Sans MS", 12, "bold")

RADIO_BUTTON_FONT = ("Comic Sans MS", 12, "bold")
RADIO_BUTTON_BG_COLOR = "#ffffff"

SAVE_BUTTON_X = 720
SAVE_BUTTON_Y = 20

HELP_BUTTON_X = 720
HELP_BUTTON_Y = 60

SETS_BUTTON_X = 720
SETS_BUTTON_Y = 100

EXPR_LABEL_X = 50
EXPR_LABEL_Y_1 = 20
EXPR_LABEL_Y_2 = 60
SELECTION_LABEL_Y = 100
VARIABLE_LABEL_Y = 140

EXPR_ENTRY_X = 300
EXPR_ENTRY_Y_1 = 20
EXPR_ENTRY_Y_2 = 60
RADIO_BUTTON_X_1 = 300
RADIO_BUTTON_X_2 = 450
RADIO_BUTTON_Y = 100
VARIABLE_ENTRY_Y = 140

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def open_help_window():
    help_window = tk.Toplevel()
    help_window.title("Help window")
    help_window.geometry(f"{HELP_WINDOW_WIDTH}x{HELP_WINDOW_HEIGHT}")

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
    root.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}")

    root.resizable(False, False)
    
    if platform.system() == "Windows":
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
        style &= ~0x10000  
        ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
    
    canvas = tk.Canvas(root, width=MAIN_WINDOW_WIDTH, height=MAIN_WINDOW_HEIGHT)
    canvas.pack(fill="both", expand=True)
    
    try:
        background_image = Image.open(resource_path("main_background.gif"))
    except (FileNotFoundError, IOError) as e:
        messagebox.showerror("Error", f"Failed to load background image: {e}")
        background_image = None

    if background_image:
        frames = [
            ImageTk.PhotoImage(frame.copy().resize((BACKGROUND_WIDTH, BACKGROUND_HEIGHT), Image.LANCZOS)) 
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
        root, 
        text="Enter boolean expression 1:", 
        bg=LABEL_BG_COLOR, 
        font=LABEL_FONT
    )

    first_expression_entry = tk.Entry(
        root, 
        width=ENTRY_WIDTH_1,
        font=ENTRY_FONT,
        bg=ENTRY_BG_COLOR
    )
    
    expression_label_2 = tk.Label(
        root, 
        text="Enter boolean expression 2:", 
        bg=LABEL_BG_COLOR, 
        font=LABEL_FONT
    )
    
    second_expression_entry = tk.Entry(
        root, 
        width=ENTRY_WIDTH_1, 
        font=ENTRY_FONT, 
        bg=ENTRY_BG_COLOR
    )
    
    selection_label = tk.Label(
        root, 
        text="Choose an active expression:", 
        bg=LABEL_BG_COLOR, 
        font=LABEL_FONT
    )
    
    radio1 = tk.Radiobutton(
        root, 
        text="Expression 1", 
        variable=active_expression, 
        value=1, 
        bg=RADIO_BUTTON_BG_COLOR, 
        font=RADIO_BUTTON_FONT
    )
    
    radio2 = tk.Radiobutton(
        root, 
        text="Expression 2", 
        variable=active_expression, 
        value=2, 
        bg=RADIO_BUTTON_BG_COLOR, 
        font=RADIO_BUTTON_FONT
    )
    
    variable_label = tk.Label(
        root, 
        text="Variable to decompose:", 
        bg=LABEL_BG_COLOR, 
        font=LABEL_FONT
    )

    variable_entry = tk.Entry(
        root, 
        width=ENTRY_WIDTH_2, 
        font=ENTRY_FONT, 
        bg=ENTRY_BG_COLOR
    )
    
    result_frame = tk.Frame(
        root, 
        bg=ENTRY_BG_COLOR, 
        bd=2, 
        relief="groove"
    )

    expression_result_display = tk.Label(
        result_frame, 
        text="The result will be displayed here.", 
        justify="left", 
        wraplength=950, 
        anchor="w", 
        bg=LABEL_BG_COLOR, 
        font=LABEL_FONT
    )

    expression_result_display.pack(
        fill="both", 
        expand=True, 
        padx=10, 
        pady=10
    )
    
    canvas.create_window(
        EXPR_LABEL_X, EXPR_LABEL_Y_1, 
        window=expression_label_1, anchor="nw"
        )
    canvas.create_window(
        EXPR_ENTRY_X, EXPR_ENTRY_Y_1, 
        window=first_expression_entry, anchor="nw"
        )
    
    canvas.create_window(
        EXPR_LABEL_X, EXPR_LABEL_Y_2, 
        window=expression_label_2, anchor="nw"
        )
    canvas.create_window(
        EXPR_ENTRY_X, EXPR_ENTRY_Y_2, 
        window=second_expression_entry, anchor="nw"
        )
    
    canvas.create_window(
        EXPR_LABEL_X, SELECTION_LABEL_Y, 
        window=selection_label, anchor="nw"
        )
    canvas.create_window(
        RADIO_BUTTON_X_1, RADIO_BUTTON_Y, 
        window=radio1, anchor="nw"
        )
    canvas.create_window(
        RADIO_BUTTON_X_2, RADIO_BUTTON_Y, 
        window=radio2, anchor="nw"
        )
    
    canvas.create_window(
        EXPR_LABEL_X, VARIABLE_LABEL_Y, 
        window=variable_label, anchor="nw"
        )
    canvas.create_window(
        EXPR_ENTRY_X, VARIABLE_ENTRY_Y, 
        window=variable_entry, anchor="nw"
        )
    
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
            root, 
            text=text, 
            width=BUTTON_WIDTH_1, 
            command=command, 
            font=BUTTON_FONT, 
            bg=BUTTON_BG_COLOR
        )

        canvas.create_window(
            x, 
            y, 
            window=button, 
            anchor="nw"
        )
    
    save_button = tk.Button(
        root, 
        text="Save to file", 
        width=BUTTON_WIDTH_2, 
        command=gui_actions.save_to_file, 
        font=BUTTON_FONT, 
        bg=BUTTON_BG_COLOR
    )

    canvas.create_window(
        720, 
        20, 
        window=save_button, 
        anchor="nw"
    )

    canvas.create_window(
        50, 
        360, 
        window=result_frame, 
        anchor="nw"
    )

    help_button = tk.Button(
        root, 
        text="Help", 
        width=15, 
        command=open_help_window, 
        font=BUTTON_FONT, 
        bg=BUTTON_BG_COLOR
    )
    
    canvas.create_window(
        720, 
        60, 
        window=help_button, 
        anchor="nw"
    )

    sets_button = tk.Button(
        root, 
        text="Sets", 
        width=BUTTON_WIDTH_2, 
        command=gui_sets.open_sets_window, 
        font=BUTTON_FONT, 
        bg=BUTTON_BG_COLOR
    )

    canvas.create_window(
        720, 
        100, 
        window=sets_button, 
        anchor="nw"
    )
    
    if background_image:
        root.bg_photo = frames 
    
    function_set = BooleanFunctionSet()
    root.mainloop()
