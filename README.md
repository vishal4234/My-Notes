# 📒 My Notes - Python GUI Note-Taking App

## 📌 Description

**My Notes** is a simple and visually appealing desktop note-taking application developed using Python's `customtkinter` for the GUI and `sqlite3` for persistent data storage. It allows users to create, view, edit, and delete colorful sticky notes that remain available even after closing the application.

---

## 🎯 Objectives

- Develop a user-friendly GUI-based note-taking application.
- Implement CRUD (Create, Read, Update, Delete) functionality for notes.
- Demonstrate the integration of GUI components with an SQLite database.

---

## 🚀 Key Features

- **Create Notes:** Add new notes using color-coded buttons (Red, Blue, Yellow, Green, Orange, Purple).
- **Edit Notes:** Notes are editable in-place; changes are auto-saved.
- **Delete Notes:** Easily remove notes via a delete (`✕`) button with confirmation prompt.
- **Data Persistence:** Notes are saved in a local SQLite database (`notes.db`).
- **Auto Layout:** Notes are arranged in a clean 4-column grid dynamically.
- **Scrollable View:** Easily navigate through all your notes with a scrollable frame.

---

## ⚙️ Function Breakdown

| Function | Description |
|----------|-------------|
| `center_window(app)` | Centers the application window on the screen. |
| `setup_database()` | Creates the `notes` table in the SQLite database if it doesn't exist. |
| `darken_color(color_code, factor)` | Returns a darker version of a color for hover effects. |
| `confirm_delete(note_frame, note_id, dialog)` | Deletes the note from UI and database after confirmation. |
| `delete_note(note_frame, note_id)` | Prompts a confirmation dialog before deleting a note. |
| `auto_arrange_notes(new_note=None)` | Arranges all notes in a 4-column grid layout. |
| `create_note_frame(note_id, color, content)` | Creates a GUI note frame with editable text and delete button. |
| `add_note(color, content)` | Inserts a new note into the database and displays it. |
| `load_notes()` | Loads and displays all notes from the database on startup. |
| `setup_close_handler()` | Ensures the database connection closes safely on exit. |
| `create_widgets()` | Sets up the GUI components (top bar, buttons, notes area). |

---

## 🖼️ Layout Design

### 🏠 Main Page

- Top Navigation Bar with App Name and Color Buttons.
- Scrollable area containing notes arranged in a grid layout.

### ❌ Confirmation Dialog

- Simple pop-up asking "Are you sure you want to delete this note?" with **OK** and **Cancel** options.

---

## 🧾 Code Overview

The app combines:
- `customtkinter`: for a modern and customizable GUI.
- `sqlite3`: for local persistent note storage.
- Python's built-in `tkinter` and `typing` for general GUI functionality and type safety.

> 💡 Real-time updates to the database ensure changes are saved automatically, and note deletions are confirmed with a dialog to avoid accidental loss.

---

## 🖥️ Output

- Responsive and colorful notes interface.
- Sticky notes with real-time editing and deletion.
- Clean layout and persistent notes across sessions.

---

## ✅ Conclusion

**"My Notes"** is a compact and efficient desktop application that demonstrates how to integrate GUI design with persistent storage using Python. With smooth user interactions, real-time editing, and a clean layout, it serves as a complete example for building modern desktop applications.

---

## 📁 Files

- `main.py` – Main application script
- `notes.db` – SQLite database (generated on first run)
- `icon.ico` – Optional app icon

---

## 🛠 Requirements

- Python 3.x
- Modules:
  - `customtkinter`
  - `sqlite3` (standard with Python)
  - `tkinter` (standard with Python)

Install `customtkinter` if needed:
```bash
pip install customtkinter
