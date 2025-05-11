import tkinter as tk
import ctypes
import platform
from text.core import CodeEditor

def main():
    root = tk.Tk()
    root.title("ZeeText")
    
    if platform.system() == "Windows":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ZeeText.1.0")
        except:
            pass
    
    editor = CodeEditor(root)
    root.protocol("WM_DELETE_WINDOW", editor.exit_editor)
    root.mainloop()

if __name__ == "__main__":
    main()