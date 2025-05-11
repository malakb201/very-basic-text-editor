import tkinter as tk
from tkinter import messagebox

class EditorActions:
    def __init__(self, editor):
        self.editor = editor
    
    def undo(self):
        if text_widget := self.editor.notebook.get_current_text_widget():
            text_widget.edit_undo()
            self.editor.notebook.update_line_numbers()
    
    def redo(self):
        if text_widget := self.editor.notebook.get_current_text_widget():
            text_widget.edit_redo()
            self.editor.notebook.update_line_numbers()
    
    def select_all(self):
        if text_widget := self.editor.notebook.get_current_text_widget():
            text_widget.tag_add(tk.SEL, "1.0", tk.END)
            text_widget.mark_set(tk.INSERT, "1.0")
    
    def show_find_dialog(self):
        FindDialog(self.editor)
    
    def zoom_in(self):
        self.editor.zoom_level += 1
        self.update_font_size()
    
    def zoom_out(self):
        self.editor.zoom_level -= 1
        self.update_font_size()
    
    def reset_zoom(self):
        self.editor.zoom_level = 0
        self.update_font_size()
    
    def update_font_size(self):
        new_size = max(8, min(72, 12 + self.editor.zoom_level))
        self.editor.current_font = ("Consolas", new_size)
        for tab_id in self.editor.notebook.tabs():
            tab = self.editor.notebook.nametowidget(tab_id)
            for child in tab.winfo_children():
                if isinstance(child, tk.scrolledtext.ScrolledText):
                    child.config(font=self.editor.current_font)
        self.editor.notebook.update_line_numbers()