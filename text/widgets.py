import tkinter as tk
from tkinter import ttk, scrolledtext
from .version import get_version

class LineNumbers(tk.Canvas):
    def __init__(self, parent, text_widget, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.text_widget = text_widget
        self.configure(width=60, bg="#252525", highlightthickness=0, bd=0)
        self.text_widget.bind("<Configure>", self.on_configure)
        self.text_widget.bind("<KeyRelease>", self.on_key_release)
    
    def on_configure(self, event=None):
        self.redraw()
    
    def on_key_release(self, event=None):
        self.redraw()
    
    def redraw(self):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(40, y, anchor="ne", text=linenum, fill="#707070", font=("Consolas", 12))
            i = self.text_widget.index(f"{i}+1line")

class EditorNotebook(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_theme()
        self.create_status_bar()
        self.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def setup_theme(self):
        self.bg_color = "#333333"
        self.fg_color = "#FFFFFF"
        self.insert_bg = "#FFFFFF"
        self.select_bg = "#555555"
        self.select_fg = "#FFFFFF"
    
    def create_status_bar(self):
        self.status_bar = ttk.Frame(self.parent)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.cursor_pos = ttk.Label(self.status_bar, text="Ln 1, Col 1")
        self.cursor_pos.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(self.status_bar, text=f"v{get_version()}").pack(side=tk.RIGHT, padx=5)
    
    def add_new_tab(self, content="", title=None):
        frame = ttk.Frame(self)
        container = ttk.Frame(frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        text_area = scrolledtext.ScrolledText(
            container,
            wrap=tk.WORD,
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.insert_bg,
            selectbackground=self.select_bg,
            selectforeground=self.select_fg,
            font=("Consolas", 12),
            relief=tk.FLAT
        )
        
        line_numbers = LineNumbers(container, text_area)
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        def on_scroll(*args):
            text_area.yview(*args)
            line_numbers.yview(*args)
        
        text_area.config(yscrollcommand=on_scroll)
        line_numbers.config(yscrollcommand=on_scroll)
        
        if content:
            text_area.insert(tk.END, content)
        
        tab_title = title if title else f"Untitled {len(self.tabs())+1}"
        self.add(frame, text=tab_title)
        self.select(frame)
        text_area.focus_set()
        
        text_area.bind("<Key>", lambda e: line_numbers.redraw())
        text_area.bind("<MouseWheel>", lambda e: line_numbers.redraw())
        text_area.bind("<KeyRelease>", self.update_cursor_pos)
        
        return text_area
    
    def update_line_numbers(self):
        current_tab = self.select()
        if current_tab:
            tab = self.nametowidget(current_tab)
            for child in tab.winfo_children():
                if isinstance(child, LineNumbers):
                    child.redraw()
    
    def update_cursor_pos(self, event=None):
        text_widget = self.get_current_text_widget()
        if text_widget:
            cursor_pos = text_widget.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            self.cursor_pos.config(text=f"Ln {line}, Col {col}")
    
    def on_tab_change(self, event):
        self.parent.master.update_title()
        self.update_line_numbers()
        self.update_cursor_pos()
    
    def get_current_text_widget(self):
        current_tab = self.select()
        if not current_tab:
            return None
        
        tab = self.nametowidget(current_tab)
        for child in tab.winfo_children():
            if isinstance(child, tk.scrolledtext.ScrolledText):
                return child
            for grandchild in child.winfo_children():
                if isinstance(grandchild, tk.scrolledtext.ScrolledText):
                    return grandchild
        return None