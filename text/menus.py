import tkinter as tk
from tkinter import ttk
from .version import get_version

class MenuBuilder:
    def __init__(self, editor):
        self.editor = editor
        self.root = editor.root
    
    def build_menu(self):
        menubar = tk.Menu(self.root, bg="#333333", fg="white")
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="white")
        file_menu.add_command(label="New", command=self.editor.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.editor.file_manager.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.editor.file_manager.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.editor.file_manager.save_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.editor.exit_editor)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="white")
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.root.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.root.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.root.event_generate("<<Paste>>"))
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="white")
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_command(label="Reset Zoom", command=self.reset_zoom, accelerator="Ctrl+0")
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="white")
        help_menu.add_command(label=f"About ZeeText v{get_version()}", command=self.editor.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        self.root.bind("<Control-s>", self.editor.file_manager.save_file)
        self.root.bind("<Control-Shift-S>", self.editor.file_manager.save_as)
        self.root.bind("<Control-o>", self.editor.file_manager.open_file)
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind("<Control-0>", lambda e: self.reset_zoom())
    
    def undo(self):
        if text_widget := self.editor.notebook.get_current_text_widget():
            text_widget.edit_undo()
            self.editor.notebook.update_line_numbers()
    
    def redo(self):
        if text_widget := self.editor.notebook.get_current_text_widget():
            text_widget.edit_redo()
            self.editor.notebook.update_line_numbers()
    
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