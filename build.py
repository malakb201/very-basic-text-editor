from text.version import get_version
import PyInstaller.__main__

def build():
    version = get_version().replace(".", "_")
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--windowed',
        f'--name=ZeeText_v{version}',
        '--icon=zeetext.ico',
        '--add-data=text;text',
        '--noconfirm',
        '--clean'
    ])

if __name__ == "__main__":
    build()