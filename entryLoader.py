from xdg.DesktopEntry import DesktopEntry
import xdg

import os

class EntryLoader:
    def __init__(self):
        self.GLOBAL_DIR_PATH = "/usr/share/applications"
        self.USER_DIR_PATH = os.path.expanduser("~") + "/.local/share/applications"

        self.DESKTOP_ENTRIES = {}

    def load_dir(self, dir_path):
        for subdir, dirs, files in os.walk(dir_path):
            for desktop_file in files:
                desktop_file = subdir+"/"+desktop_file
                if desktop_file[-8:] == ".desktop":
                    entry = DesktopEntry(desktop_file)
                    try:
                        entry.validate()
                        self.DESKTOP_ENTRIES[entry.getName()] = entry
                    except xdg.Exceptions.ValidationError, e:
                        continue

    def load(self):                    
        self.load_dir(self.GLOBAL_DIR_PATH)
        self.load_dir(self.USER_DIR_PATH)
        return self.DESKTOP_ENTRIES