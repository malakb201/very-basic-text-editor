import tkinter as tk
from tkinter import ttk
import os
from .menus import MenuBuilder
from .file_io import FileManager
from .widgets import EditorNotebook
from .version import get_version

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.version = get_version()
        self.root.title(f"ZeeText v{self.version}")
        self.root.geometry("1200x800")
        self.setup_theme()
        
        self.current_font = ("Consolas", 12)
        self.zoom_level = 0
        self.untitled_count = 0
        self.file_paths = {}
        
        self.notebook = EditorNotebook(self.root)
        self.file_manager = FileManager(self)
        self.menus = MenuBuilder(self)
        
        self.setup_ui()
        self.new_file()
    
    def setup_theme(self):
        self.root.configure(bg="#2d2d2d")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background="#2d2d2d", foreground="white")
        self.style.configure('TFrame', background="#2d2d2d")
        self.style.configure('TLabel', background="#2d2d2d", foreground="white")
        self.style.configure('TButton', background="#3d3d3d", foreground="white")
        self.style.map('TButton',
                      background=[('active', '#4d4d4d')],
                      foreground=[('active', 'white')])
    
    def setup_ui(self):
        self.menus.build_menu()
        self.notebook.pack(fill=tk.BOTH, expand=True)
    
    def new_file(self):
        self.untitled_count += 1
        tab_title = f"Untitled-{self.untitled_count}"
        self.notebook.add_new_tab(title=tab_title)
        self.file_paths[tab_title] = None
        self.update_title()
    
    def update_title(self):
        current_tab = self.notebook.select()
        if current_tab:
            tab_text = self.notebook.tab(current_tab, "text")
            file_path = self.file_paths.get(tab_text, "")
            if file_path:
                self.root.title(f"{os.path.basename(file_path)} - ZeeText v{self.version}")
            else:
                self.root.title(f"{tab_text} - ZeeText v{self.version}")
    
    def status(self, message):
        self.notebook.status_label.config(text=message)
        self.root.after(3000, lambda: self.notebook.status_label.config(text="Ready"))
    
    def show_about(self):
        about = tk.Toplevel(self.root)
        about.title(f"About ZeeText v{self.version}")
        about.configure(bg="#2d2d2d")
        
        tk.Label(
            about,
            text=f"ZeeText v{self.version}\nOpen Source Text Editor\nCopyright © Zeetext",
            bg="#2d2d2d",
            fg="white",
            font=("Arial", 11)
        ).pack(padx=20, pady=20)
        
        ttk.Button(about, text="OK", command=about.destroy).pack(pady=10)
    
    def exit_editor(self):
        self.root.quit()