import os

def get_desktop_path():
    home = os.path.expanduser("~")
    desktop = os.path.join(home, "Desktop")
    return desktop

