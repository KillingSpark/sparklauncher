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
        self.icon = desk_entry.getIcon()

    def getName(self):
        return self.name

    def getIcon(self):
        return self.icon

    def start(self):
        exec_str = str.split(str(self.exe), " ")
        executable = exec_str[0]
        args = exec_str[1:]

        filtered_args = list([executable])

        for arg in args:
            if not arg.startswith('%'):
                filtered_args.append(arg)

        print(executable)
        subprocess.Popen(filtered_args)


class PathEntry:
    def __init__(self, path):
        self.name = path

    def getName(self):
        return self.name

    def getIcon(self):
        return "folder"

    def start(self):
        subprocess.call(["xdg-open", self.name])

class BrowserEntry:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def getName(self):
        return self.name

    def getIcon(self):
        return "chromium"

    def start(self):
        subprocess.call(["xdg-open", self.url])

class Launcher:
    def load_chrome_book_marks(self, subdict, bm_list):
        if subdict["type"] == "url":
            bm_list.append(BrowserEntry(subdict["name"], subdict["url"]))
        if subdict["type"] == "folder":
            for child in subdict["children"]:
                bm_list = self.load_chrome_book_marks(child, bm_list)

        return bm_list

    def load_counts(self):
        self.count_file_path = os.path.expanduser("~") + "/.config/sparklauncher/.sparklauncher"
        if os.path.exists(self.count_file_path):
            count_file = open(self.count_file_path, "r")
            self.count_dict = json.load(count_file)

    def load_bookmarks(self):
        self.book_marks_file_path = os.path.expanduser("~") + "/.config/chromium/Default/Bookmarks"
        if os.path.exists(self.book_marks_file_path):
            book_marks_file = open(self.book_marks_file_path, "r")
            chrome_book_marks_folders = json.load(book_marks_file)
            bm_list = list()
            for root in chrome_book_marks_folders["roots"]:
                  self.load_chrome_book_marks(chrome_book_marks_folders["roots"][root], bm_list)
            
            for bm in bm_list:
                self.chrome_book_marks[bm.getName()] = bm
        
        #load chrome bookmarks
        self.book_marks_file_path = os.path.expanduser("~") + "/.config/chrome/Default/Bookmarks"
        if os.path.exists(self.book_marks_file_path):
            book_marks_file = open(self.book_marks_file_path, "r")
            chrome_book_marks_folders = json.load(book_marks_file)
            bm_list = list()
            for root in chrome_book_marks_folders["roots"]:
                  self.load_chrome_book_marks(chrome_book_marks_folders["roots"][root], bm_list)
            
            for bm in bm_list:
                self.chrome_book_marks[bm.getName()] = bm


    def reload(self):
        #reset
        self.count_dict = {}
        self.chrome_book_marks = {}
        self.entries = {}
        self.ever_started = list()

        self.load_counts()
        self.load_bookmarks()
        loaded = desktopEntryLoader.EntryLoader().load()
        for entry in loaded:
            self.entries[entry] = AppEntry(loaded[entry])

        for entry in self.entries:
            try:
                # if this worked it got started at least once
                count = self.count_dict[entry]
                self.ever_started.append(self.entries[entry])
            except KeyError:
                pass
        



    def __init__(self):
        self.count_dict = {}
        self.chrome_book_marks = {}
        self.entries = {}
        self.ever_started = list()

        self.reload()

        self.filtered_entries = self.ever_started
        self.filtered_entries.sort(key=lambda x: x.getName())
        self.filtered_entries.sort(key=self.map_entry_count, reverse=True)

    def filter(self, tokens):
        if len(tokens) == 1 and tokens[0] == '':
            self.filtered_entries = self.ever_started
            return

        new_filtered = list()

        #only one mode at a time
        if tokens[0] == "~" or tokens[0] == "/":
            for path in self.find_matching_path(tokens[1:], os.path.expanduser(tokens[0])):
                new_filtered.append(PathEntry(path))
        elif tokens[0] == "#":
            tokens = tokens[1:]
            
            for name in self.chrome_book_marks:
                hit = True
                for token in tokens:
                    if not (token.upper() in self.chrome_book_marks[name].getName().upper() or token.upper() in self.chrome_book_marks[name].url.upper()):
                        hit = False
                if hit: 
                    new_filtered.append(self.chrome_book_marks[name])
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


        json.dump(self.count_dict, open(self.count_file_path, "w"))
        selected.start()
