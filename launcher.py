from xdg import DesktopEntry
import desktopEntryLoader
import copy
import os
import json
import subprocess

import settings

class AppEntry:
    def __init__(self, desk_entry):
        self.name = desk_entry.getName()
        self.exe = desk_entry.getExec()

    def getName(self):
        return self.name

    def start(self):
        exec_str = str.split(str(self.exe), " ")
        executable = exec_str[0]
        args = exec_str[1:]

        filtered_args = list([""])

        for arg in args:
            if not arg.startswith('%'):
                filtered_args.append(arg)

        print(executable)
        print(filtered_args)

        os.execvp(executable, filtered_args)


class PathEntry:
    def __init__(self, path):
        self.name = path

    def getName(self):
        small_path = self.name
        max_len = settings.MAX_NAME_CHARS
        if len(self.name) > max_len:
            small_path = "..." + self.name[-max_len:]
        return small_path

    def start(self):
        subprocess.call(["xdg-open", self.name])
        exit()


class Launcher:
    def __init__(self):
        self.count_dict = {}

        self.count_file_path = os.path.expanduser("~") + "/.sparklauncher"
        if os.path.exists(self.count_file_path):
            count_file = os.open(self.count_file_path, os.O_RDWR)
            json_count = os.read(count_file, 2048)
            self.count_dict = json.loads(json_count)

        loaded = desktopEntryLoader.EntryLoader().load()
        self.entries = {}

        for entry in loaded:
            self.entries[entry] = AppEntry(loaded[entry])

        self.ever_started = list()

        for entry in self.entries:
            try:
                # if this worked it got started at least once
                count = self.count_dict[entry]
                self.ever_started.append(self.entries[entry])
            except KeyError:
                pass

        self.filtered_entries = self.ever_started
        self.filtered_entries.sort(key=lambda x: x.getName())
        self.filtered_entries.sort(key=self.map_entry_count, reverse=True)

    def filter(self, tokens):
        if len(tokens) == 1 and tokens[0] == '':
            self.filtered_entries = self.ever_started
            return

        new_filtered = list()

        #either file mode or app mode
        if tokens[0] == "~" or tokens[0] == "/":
            for path in self.find_matching_path(tokens[1:], os.path.expanduser(tokens[0])):
                new_filtered.append(PathEntry(path))
        else:
            for name in self.entries:
                contains = True
                for token in tokens:
                    contains = contains and (
                        str(token).upper() in str(name).upper())
                    if not contains:
                        break
                if contains:
                    new_filtered.append(self.entries[name])

        new_filtered.sort(key=lambda x: x.getName())
        new_filtered.sort(key=self.map_entry_count, reverse=True)
        self.filtered_entries = new_filtered

    def find_matching_path(self, tokens, path):
        paths = list()
        for name in os.listdir(path):
            if not name.startswith("."):
                # if only one token is left, files are ok too
                if len(tokens) == 1 or os.path.isdir(os.path.join(path, name)):
                    if tokens[0].upper() in name.upper():
                        paths.append(path + "/" + name)

        if len(tokens) > 1:
            hits = list()
            for dir in paths:
                for hit in self.find_matching_path(tokens[1:], dir):
                    hits.append(hit)
            return hits
        else:
            return paths

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
        if not os.path.exists(self.count_file_path):
            count_file = os.open(self.count_file_path, os.O_CREAT)
        count_file = os.open(self.count_file_path, os.O_RDWR)
        os.write(count_file, json_count)

        selected.start()
