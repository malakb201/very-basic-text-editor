import os
import tkinter as tk
from tkinter import filedialog, messagebox
from .version import get_version

class FileManager:
    def __init__(self, editor):
        self.editor = editor
        self.recent_files = []
    
    def save_file(self, event=None):
        try:
            text_widget = self.editor.notebook.get_current_text_widget()
            if text_widget is None:
                messagebox.showerror("Error", "No text widget found")
                return False

            current_tab = self.editor.notebook.select()
            if not current_tab:
                messagebox.showerror("Error", "No active tab found")
                return False

            tab_title = self.editor.notebook.tab(current_tab, "text")
            file_path = self.editor.file_paths.get(tab_title)

            if file_path is None or tab_title.startswith("Untitled"):
                return self.save_as()

            content = text_widget.get("1.0", tk.END)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.editor.status(f"Saved: {file_path}")
            return True

        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")
            return False
    
    def save_as(self, event=None):
        text_widget = self.editor.notebook.get_current_text_widget()
        if text_widget is None:
            messagebox.showerror("Error", "No active document to save")
            return False
        
        filetypes = [
            ("Text files", "*.txt"),
            ("Python files", "*.py"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=filetypes,
            title=f"Save As - ZeeText v{get_version()}"
        )
        
        if not file_path:
            return False
        
        try:
            content = text_widget.get("1.0", tk.END)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            current_tab = self.editor.notebook.select()
            if current_tab:
                base_name = os.path.basename(file_path)
                self.editor.notebook.tab(current_tab, text=base_name)
                self.add_to_recent_files(file_path)
                self.editor.file_paths[base_name] = file_path
                self.editor.update_title()
                self.editor.status(f"Saved: {file_path}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
            return False
    
    def open_file(self, event=None):
        filetypes = [
            ("Text files", "*.txt"),
            ("Python files", "*.py"), 
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if not file_path:
            return
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            base_name = os.path.basename(file_path)
            
            # Check if file is already open
            for tab_id in self.editor.notebook.tabs():
                tab_text = self.editor.notebook.tab(tab_id, "text")
                if tab_text == base_name:
                    self.editor.notebook.select(tab_id)
                    return
            
            # Add new tab with file content
            self.editor.notebook.add_new_tab(content=content, title=base_name)
            self.editor.file_paths[base_name] = file_path
            self.add_to_recent_files(file_path)
            self.editor.status(f"Opened: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
    
    def add_to_recent_files(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:10]