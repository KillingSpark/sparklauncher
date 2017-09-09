from xdg import DesktopEntry

import entryLoader

import copy

import os

class Launcher:
    def __init__(self):
        self.entries = entryLoader.EntryLoader().load()
        self.filtered_entries = list(self.entries)

    def filter(self, tokens):
        if len(tokens) == 0:
            self.filtered_entries = self.entries
            return

        new_filtered = list()
        for entry in self.entries:
            if not self.entries[entry].getType() == "Application":
                continue

            contains = True
            for token in tokens: 
                contains = contains and (str(token).upper() in str(entry).upper())
                if not contains:
                    break
            if contains:
                new_filtered.append(entry)
        
        new_filtered.sort()
        self.filtered_entries = new_filtered

    def print_selection(self):
        for name in self.filtered_entries:
            print(name)

    def run_selected(self):
        exec_str = str.split(str(self.entries[self.filtered_entries[0]].getExec()), " ")
        executable = exec_str[0]
        args = exec_str[1:]

        filtered_args = list([""])

        for arg in args:
            if not arg.startswith('%'):
                filtered_args.append(arg)

        
        print(executable)
        print(filtered_args)

        os.execvp(executable, filtered_args)

