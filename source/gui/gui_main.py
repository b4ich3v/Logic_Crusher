import ctypes
import os
import platform
import sys
import tkinter as tk
from tkinter import messagebox
import markdown2
from tkinterweb import HtmlFrame
from PIL import Image, ImageSequence, ImageTk, ImageDraw, ImageFont

from gui import constants as cn
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

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def open_help_window():
    help_window = tk.Toplevel()
    help_window.title(cn.HELP_WINDOW_TITLE)
    help_window.geometry(f"{cn.HELP_WINDOW_WIDTH}x{cn.HELP_WINDOW_HEIGHT}")

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

def create_text_image(
        width, height, text, alpha, font_path=None, 
        font_size=cn.UPDATE_BACKGROUND_INTERVAL
    ):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if font_path and os.path.exists(font_path):
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.truetype(cn.FALLBACK_FONT_PATH, font_size)

    x_offset = cn.TEXT_X_OFFSET
    y_offset = cn.TEXT_Y_OFFSET
    x = x_offset
    y = y_offset

    text_color = (0, 0, 0, alpha)
    draw.text((x, y), text, font=font, fill=text_color)
    return img

def fade_text_in_out(
        canvas, text_content, duration=cn.FADE_DURATION, 
        interval=cn.FADE_INTERVAL, font_path=None
    ):
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()

    text_image_id = canvas.create_image(0, 0, anchor="nw")
    images_cache = [None]

    def do_step(step):
        if step <= duration:
            alpha = int((step / duration) * 255)
        else:
            alpha = max(0, 255 - int(((step - duration) / duration) * 255))

        img = create_text_image(width, height, text_content, alpha=alpha,
                                font_path=font_path, font_size=cn.DEFAULT_FONT_SIZE)
        photo = ImageTk.PhotoImage(img)
        images_cache[0] = photo
        canvas.itemconfig(text_image_id, image=photo)

        if step < 2 * duration:
            canvas.after(interval, lambda: do_step(step + 1))

    do_step(0)

def show_splash():
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)

    width, height = cn.SPLASH_WIDTH, cn.SPLASH_HEIGHT
    screen_w = splash_root.winfo_screenwidth()
    screen_h = splash_root.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    splash_root.geometry(f"{width}x{height}+{x}+{y}")

    bg_path = resource_path(cn.SPLASH_BG_IMAGE)
    bg_image = Image.open(bg_path)
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(splash_root, width=width, height=height,
                       bd=0, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_photo)

    text_content = cn.SPLASH_QUOTE
    mysterious_font_path = cn.MYSTERIOUS_FONT_PATH

    fade_text_in_out(
        canvas,
        text_content,
        duration=cn.FADE_DURATION,
        interval=cn.FADE_INTERVAL,
        font_path=mysterious_font_path
    )

    splash_root.after(cn.SPLASH_TIMEOUT, lambda: start_main_window(splash_root))
    splash_root.mainloop()

def start_main_window(splash_root):
    splash_root.destroy()
    run()

def run():
    global root, first_expression_entry, second_expression_entry
    global active_expression, expression_result_display, variable_entry
    global function_set

    root = tk.Tk()
    root.title(cn.APP_TITLE)
    root.geometry(f"{cn.MAIN_WINDOW_WIDTH}x{cn.MAIN_WINDOW_HEIGHT}")

    root.resizable(False, False)
    
    if platform.system() == "Windows":
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
        style &= ~0x10000  
        ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
    
    canvas = tk.Canvas(
        root, 
        width=cn.MAIN_WINDOW_WIDTH, 
        height=cn.MAIN_WINDOW_HEIGHT
    )
    canvas.pack(fill="both", expand=True)
    
    try:
        background_image = Image.open(resource_path(cn.MAIN_BG_GIFF))
    except (FileNotFoundError, IOError) as e:
        messagebox.showerror("Error", f"Failed to load background image: {e}")
        background_image = None

    if background_image:
        frames = [
            ImageTk.PhotoImage(frame.copy().resize(
                (cn.BACKGROUND_GIF_WIDTH, cn.BACKGROUND_GIF_HEIGHT), Image.LANCZOS)
                ) 
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
        text=cn.LABEL_EXPR_1_TEXT, 
        bg=cn.LABEL_BG_COLOR, 
        font=cn.LABEL_FONT
    )

    first_expression_entry = tk.Entry(
        root, 
        width=cn.ENTRY_WIDTH_1,
        font=cn.ENTRY_FONT,
        bg=cn.ENTRY_BG_COLOR
    )
    
    expression_label_2 = tk.Label(
        root, 
        text=cn.LABEL_EXPR_2_TEXT, 
        bg=cn.LABEL_BG_COLOR, 
        font=cn.LABEL_FONT
    )
    
    second_expression_entry = tk.Entry(
        root, 
        width=cn.ENTRY_WIDTH_1, 
        font=cn.ENTRY_FONT, 
        bg=cn.ENTRY_BG_COLOR
    )
    
    selection_label = tk.Label(
        root, 
        text=cn.LABEL_SELECT_ACTIVE, 
        bg=cn.LABEL_BG_COLOR, 
        font=cn.LABEL_FONT
    )
    
    radio1 = tk.Radiobutton(
        root, 
        text="Expression 1", 
        variable=active_expression, 
        value=1, 
        bg=cn.RADIO_BUTTON_BG_COLOR, 
        font=cn.RADIO_BUTTON_FONT
    )
    
    radio2 = tk.Radiobutton(
        root, 
        text="Expression 2", 
        variable=active_expression, 
        value=2, 
        bg=cn.RADIO_BUTTON_BG_COLOR, 
        font=cn.RADIO_BUTTON_FONT
    )
    
    variable_label = tk.Label(
        root, 
        text=cn.LABEL_DECOMPOSE_VAR, 
        bg=cn.LABEL_BG_COLOR, 
        font=cn.LABEL_FONT
    )

    variable_entry = tk.Entry(
        root, 
        width=cn.ENTRY_WIDTH_2, 
        font=cn.ENTRY_FONT, 
        bg=cn.ENTRY_BG_COLOR
    )
    
    result_frame = tk.Frame(
        root, 
        bg=cn.ENTRY_BG_COLOR, 
        bd=2, 
        relief="groove"
    )

    expression_result_display = tk.Label(
        result_frame, 
        text=cn.RESULT_PLACEHOLDER, 
        justify="left", 
        wraplength=950, 
        anchor="w", 
        bg=cn.LABEL_BG_COLOR, 
        font=cn.LABEL_FONT
    )

    expression_result_display.pack(
        fill="both", 
        expand=True, 
        padx=cn.RESULT_DISPLAY_PADX, 
        pady=cn.RESULT_DISPLAY_PADY
    )
    
    canvas.create_window(
        cn.EXPR_LABEL_X, cn.EXPR_LABEL_Y_1, 
        window=expression_label_1, anchor="nw"
        )
    canvas.create_window(
        cn.EXPR_ENTRY_X, cn.EXPR_ENTRY_Y_1, 
        window=first_expression_entry, anchor="nw"
        )
    
    canvas.create_window(
        cn.EXPR_LABEL_X, cn.EXPR_LABEL_Y_2, 
        window=expression_label_2, anchor="nw"
        )
    canvas.create_window(
        cn.EXPR_ENTRY_X, cn.EXPR_ENTRY_Y_2, 
        window=second_expression_entry, anchor="nw"
        )
    
    canvas.create_window(
        cn.EXPR_LABEL_X, cn.SELECTION_LABEL_Y, 
        window=selection_label, anchor="nw"
        )
    canvas.create_window(
        cn.RADIO_BUTTON_X_1, cn.RADIO_BUTTON_Y, 
        window=radio1, anchor="nw"
        )
    canvas.create_window(
        cn.RADIO_BUTTON_X_2, cn.RADIO_BUTTON_Y, 
        window=radio2, anchor="nw"
        )
    
    canvas.create_window(
        cn.EXPR_LABEL_X, cn.VARIABLE_LABEL_Y, 
        window=variable_label, anchor="nw"
        )
    canvas.create_window(
        cn.EXPR_ENTRY_X, cn.VARIABLE_ENTRY_Y, 
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
        row = index // cn.BUTTONS_PER_ROW
        col = index % cn.BUTTONS_PER_ROW
        x = cn.BUTTON_START_X + col * cn.BUTTON_SPACING_X
        y = cn.BUTTON_START_Y + row * cn.BUTTON_SPACING_Y

        button = tk.Button(
            root, 
            text=text, 
            width=cn.BUTTON_WIDTH_1, 
            command=command, 
            font=cn.BUTTON_FONT, 
            bg=cn.BUTTON_BG_COLOR
        )

        canvas.create_window(
            x, 
            y, 
            window=button, 
            anchor="nw"
        )
    
    save_button = tk.Button(
        root, 
        text=cn.SAVE_TO_FILE_BUTTON_TEXT, 
        width=cn.BUTTON_WIDTH_2, 
        command=gui_actions.save_to_file, 
        font=cn.BUTTON_FONT, 
        bg=cn.BUTTON_BG_COLOR
    )

    canvas.create_window(
        cn.SAVE_BUTTON_X, 
        cn.SAVE_BUTTON_Y, 
        window=save_button, 
        anchor="nw"
    )

    canvas.create_window(
        cn.RESULT_FRAME_X, 
        cn.RESULT_FRAME_Y, 
        window=result_frame, 
        anchor="nw"
    )

    help_button = tk.Button(
        root, 
        text=cn.HELP_BUTTON_TEXT, 
        width=15, 
        command=open_help_window, 
        font=cn.BUTTON_FONT, 
        bg=cn.BUTTON_BG_COLOR
    )
    
    canvas.create_window(
        cn.HELP_BUTTON_X, 
        cn.HELP_BUTTON_Y, 
        window=help_button, 
        anchor="nw"
    )

    sets_button = tk.Button(
        root, 
        text=cn.SETS_BUTTON_TEXT, 
        width=cn.BUTTON_WIDTH_2, 
        command=gui_sets.open_sets_window, 
        font=cn.BUTTON_FONT, 
        bg=cn.BUTTON_BG_COLOR
    )

    canvas.create_window(
        cn.SETS_BUTTON_X, 
        cn.SETS_BUTTON_Y, 
        window=sets_button, 
        anchor="nw"
    )
    
    if background_image:
        root.bg_photo = frames 
    
    function_set = BooleanFunctionSet()
    root.mainloop()
