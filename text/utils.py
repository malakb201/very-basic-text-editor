def get_platform():
    import platform
    return platform.system()

def is_windows():
    return get_platform() == "Windows"

def setup_dark_title_bar(window):
    if is_windows():
        try:
            from ctypes import windll
            HWND = window.winfo_id()
            windll.dwmapi.DwmSetWindowAttribute(
                HWND,
                20,  # DWMWA_USE_IMMERSIVE_DARK_MODE
                True,
                4
            )
        except:
            pass