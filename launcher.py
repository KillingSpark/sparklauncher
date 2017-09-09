from xdg import DesktopEntry

import entryLoader

import copy

import os

import json

class Launcher:
    def __init__(self):
        self.count_dict = {}

        self.count_file_path = os.path.expanduser("~")+"/.sparklauncher"
        if os.path.exists(self.count_file_path):
            count_file = os.open(self.count_file_path, os.O_RDWR)
            json_count = os.read(count_file, 2048)
            self.count_dict = json.loads(json_count)

        self.entries = entryLoader.EntryLoader().load()

        self.filtered_entries = list(self.entries)

    def filter(self, tokens):
        if len(tokens) == 0:
            self.filtered_entries = self.entries
            return

        new_filtered = list()
        for name in self.entries:

            contains = True
            for token in tokens: 
                contains = contains and (str(token).upper() in str(name).upper())
                if not contains:
                    break
            if contains:
                new_filtered.append(self.entries[name])
        
        new_filtered.sort(key=lambda x: x.getName())

        new_filtered.sort(key=self.map_entry_count, reverse=True)
        self.filtered_entries = new_filtered

    def map_entry_count(self, entry):
            count = 0
            try:
                count = self.count_dict[entry.getName()]
            except KeyError:
                pass
            return count

    def print_selection(self):
        for name in self.filtered_entries:
            print(name)

    def run_selected(self, index):
        selected = self.filtered_entries[index]

        try:
            self.count_dict[selected.getName()] += 1
        except KeyError:
            self.count_dict[selected.getName()] = 1

        json_count = json.dumps(self.count_dict)
        count_file = os.open(self.count_file_path, os.O_RDWR)
        os.write(count_file, json_count)

        exec_str = str.split(str(selected.getExec()), " ")
        executable = exec_str[0]
        args = exec_str[1:]

        filtered_args = list([""])

        for arg in args:
            if not arg.startswith('%'):
                filtered_args.append(arg)

        
        print(executable)
        print(filtered_args)

        os.execvp(executable, filtered_args)

