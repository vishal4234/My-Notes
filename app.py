import tkinter as tk
from customtkinter import *
import sqlite3
from typing import Optional

# Initialize database connection and cursor
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

def center_window(app):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = 800
    window_height = 600
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

def setup_database():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        color TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def darken_color(color_code: str, factor=0.9) -> str:
    """Return a slightly darker version of the color"""
    if len(color_code) != 7 or not color_code.startswith("#"):
        return color_code
        
    try:
        r = int(color_code[1:3], 16)
        g = int(color_code[3:5], 16)
        b = int(color_code[5:7], 16)
        return f"#{int(r*factor):02x}{int(g*factor):02x}{int(b*factor):02x}"
    except:
        return color_code

def confirm_delete(note_frame, note_id, dialog):
    note_frame.destroy()
    dialog.destroy()
    try:
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        auto_arrange_notes()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def delete_note(note_frame, note_id):
    confirm_dialog = CTkToplevel(app)
    confirm_dialog.title("Confirmation")
    
    # Center relative to main window
    x = app.winfo_x() + (app.winfo_width() // 2) - 115
    y = app.winfo_y() + (app.winfo_height() // 2) - 60
    confirm_dialog.geometry(f"230x120+{x}+{y}")
    
    confirm_text = CTkLabel(
        confirm_dialog, 
        text="Are you sure you want\nto delete this note?", 
        text_color="white", font=("Arial", 20)
    )
    confirm_text.pack(pady=10)

    button_frame = CTkFrame(confirm_dialog, fg_color="transparent")
    button_frame.pack(pady=5)

    CTkButton(
        button_frame, text="OK", width=80, height=30,
        font=("Arial", 12), fg_color="#E23838", text_color="white",
        hover_color="#CE3333", command=lambda: confirm_delete(note_frame, note_id, confirm_dialog)
    ).grid(row=0, column=0, padx=5)

    CTkButton(
        button_frame, text="Cancel", width=80, height=30,
        font=("Arial", 12), fg_color="#a4a4a4", text_color="white",
        hover_color="#a9a9a9", command=confirm_dialog.destroy
    ).grid(row=0, column=1, padx=5)

def auto_arrange_notes(new_note=None):
    children = bottom.winfo_children()
    if new_note:
        children = [new_note] + children[:-1]  # Bring new note to front
        
    for index, child in enumerate(children):
        row = index // 4
        col = index % 4
        child.grid(row=row, column=col, pady=10, padx=10)

def create_note_frame(note_id: int, color: str, content: str):
    note = CTkFrame(bottom, width=170, height=150, 
                   corner_radius=10, fg_color=color)
    
    # Delete button in top-right corner
    delete_btn = CTkButton(
        note, text="✕", width=20, height=20,
        font=("Arial", 12), corner_radius=100,
        fg_color="transparent", text_color="white" if color != "#f3f3f3" else "black",
        hover_color=darken_color(color, 0.8),
        command=lambda: delete_note(note, note_id)
    )
    delete_btn.place(relx=0.9, rely=0.05, anchor="center")

    # Text area
    text_color = "black" if color == "#f3f3f3" else "white"
    text_box = CTkTextbox(
        note, width=160, height=130, corner_radius=8,
        fg_color="transparent", text_color=text_color,
        border_width=0, font=("Arial", 14), wrap="word"
    )
    text_box.insert("0.0", content)
    text_box.place(relx=0.5, rely=0.55, anchor="center")

    # Update database on content change
    def update_content(event=None):
        new_content = text_box.get("0.0", "end-1c")
        try:
            cursor.execute(
                "UPDATE notes SET content = ? WHERE id = ?",
                (new_content, note_id)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    text_box.bind("<KeyRelease>", update_content)

    auto_arrange_notes(note)

def add_note(color: Optional[str] = None, content: str = ""):
    try:
        cursor.execute(
            "INSERT INTO notes (content, color) VALUES (?, ?)", (content, color)
        )
        conn.commit()
        note_id = cursor.lastrowid
        create_note_frame(note_id, color, content)
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def load_notes():
    try:
        cursor.execute("SELECT id, content, color FROM notes ORDER BY created_at DESC")
        for note_id, content, color in cursor.fetchall():
            create_note_frame(note_id, color, content)
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def setup_close_handler():
    def on_close():
        try:
            conn.close()
        except:
            pass
        app.destroy()
        
    app.protocol("WM_DELETE_WINDOW", on_close)

def create_widgets():
    # Top Navigation Bar
    top_nav = CTkFrame(app, width=800, height=100, corner_radius=0, fg_color="#f3f3f3")
    top_nav.grid(row=0, column=0, sticky="ew")

    # Bottom Content Area
    global bottom
    bottom = CTkScrollableFrame(app, width=800, height=500, corner_radius=0, fg_color="#ffffff")
    bottom.grid(row=1, column=0, sticky="nsew")

    # Logo
    logo = CTkLabel(top_nav, text="MY NOTES", text_color="black", font=("Arial", 20, "bold"), fg_color="transparent")
    logo.grid(row=0, column=0, padx=20, pady=10)

    # Color buttons for new notes
    colors = [
        ("#E23838", "red"), 
        ("#009CDF", "blue"),
        ("#FFB900", "yellow"),
        ("#5EBD3E", "green"),
        ("#FF5E3A", "orange"),
        ("#A94DFF", "purple"),
    ]
    
    for i, (color_code, _) in enumerate(colors, start=1):
        btn = CTkButton(
            top_nav, text="+", width=20, height=30,
            font=("Arial", 20), corner_radius=100,
            fg_color=color_code, text_color="white",
            cursor="hand2", hover_color=darken_color(color_code),
            border_width=0, command=lambda c=color_code: add_note(c)
        )
        btn.grid(row=0, column=i, padx=10, pady=10)

# Main application setup
app = CTk(fg_color="white")
app.geometry("970x600")
app.resizable(False, False)
app.title("My Notes")
try:
    app.iconbitmap("icon.ico")
except:
    pass  # Handle missing icon gracefully

set_appearance_mode("dark")
center_window(app)
setup_database()
create_widgets()
load_notes()
setup_close_handler()

app.mainloop()