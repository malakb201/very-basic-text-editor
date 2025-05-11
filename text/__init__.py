from .core import CodeEditor
from .version import get_version
from .widgets import EditorNotebook, LineNumbers

__all__ = ['CodeEditor', 'get_version', 'EditorNotebook', 'LineNumbers']
__version__ = get_version()