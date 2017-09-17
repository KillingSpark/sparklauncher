#! /usr/bin/python2

# import gtk stuff
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GObject

#import settings
import settings
import launcher
import os
import threading

GObject.threads_init()

TRIGGER_FIFO = "/tmp/sparklauncher.fifo"

# check for running instance
import locking
if locking.check_lock_file():
    print("already running")
    fd = os.open(TRIGGER_FIFO, os.O_WRONLY)
    os.write(fd, "open")
    os.close(fd)
    exit()

# globals
ENTRY_LAUNCHER = launcher.Launcher()
SELECTED_INDEX = -1

# gui globals
MAIN_WINDOW = Gtk.Window()
SEARCH_BOX = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
RESULT_BOX = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
SEARCH_ENTRY = Gtk.Entry()


def clicked_label(label_with_entry, button_event):
    label_with_entry.entry.start()

# the handlers for signals


def update_selection(entry_object):
    global SELECTED_INDEX
    SELECTED_INDEX = -1
    try:
        RESULT_BOX.get_children()[SELECTED_INDEX].set_name("label")
    except IndexError:
        pass

    ENTRY_LAUNCHER.filter(str.split(entry_object.get_text(), " "))

    for child in RESULT_BOX.get_children():
        RESULT_BOX.remove(child)

    for i in range(0, min(settings.MAX_ENTRIES, len(ENTRY_LAUNCHER.filtered_entries))):
        text = ENTRY_LAUNCHER.filtered_entries[i].getName()
        if len(text) > settings.MAX_ENTRY_CHARS:
            text = "..." + text[len(text) - settings.MAX_ENTRY_CHARS - 3:]

        button = Gtk.Button(label=text)
        button.entry = ENTRY_LAUNCHER.filtered_entries[i]
        button.connect("button-press-event", clicked_label)
        button.set_name("label")

        if settings.JUSTIFY_ENTRY == "LEFT":
            box = Gtk.HBox(0)
            box.pack_start(button, False, False, 0)
        if settings.JUSTIFY_ENTRY == "RIGHT":
            box = Gtk.HBox(0)
            box.pack_end(button, False, False, 0)
        if settings.JUSTIFY_ENTRY == "CENTER":
            box = Gtk.VBox(0)
            box.pack_start(button, False, False, 0)

        box.set_name("label")
        RESULT_BOX.add(box)

    RESULT_BOX.show_all()


def run_selected(_):
    MAIN_WINDOW.hide()
    if SELECTED_INDEX < 0:
        ENTRY_LAUNCHER.run_selected(0)

    ENTRY_LAUNCHER.run_selected(SELECTED_INDEX)


def handle_keys(widget, key_event):
    global SELECTED_INDEX

    # enter if the text lost focus
    if key_event.keyval == 65293:
        run_selected(widget)

    # esc key value
    if key_event.keyval == 65307:
        MAIN_WINDOW.hide()

    # down
    elif key_event.keyval == 65364:
        if SELECTED_INDEX < len(RESULT_BOX.get_children()) - 1:
            if SELECTED_INDEX >= 0:
                RESULT_BOX.get_children()[SELECTED_INDEX].get_children()[0].set_name("label")

            SELECTED_INDEX += 1
            RESULT_BOX.get_children()[SELECTED_INDEX].get_children()[0].set_name("selected")
        return True

    # up
    elif key_event.keyval == 65362:
        if SELECTED_INDEX > 0:
            RESULT_BOX.get_children()[SELECTED_INDEX].get_children()[0].set_name("label")
            SELECTED_INDEX -= 1
            RESULT_BOX.get_children()[SELECTED_INDEX].get_children()[0].set_name("selected")
        return True

    return False


def hide_on_focus_lost(*_):
    MAIN_WINDOW.hide()


# funcs for better readability


def setup_window():
    MAIN_WINDOW.set_name("window")
    MAIN_WINDOW.set_skip_taskbar_hint(True)
    MAIN_WINDOW.set_decorated(False)
    MAIN_WINDOW.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
    MAIN_WINDOW.set_size_request(settings.WIN_WIDTH, settings.WIN_HEIGHT)
    MAIN_WINDOW.set_resizable(False)

    SEARCH_ENTRY.set_name("search")

    MAIN_WINDOW.add(SEARCH_BOX)
    SEARCH_BOX.add(SEARCH_ENTRY)
    SEARCH_BOX.add(RESULT_BOX)


def connect_signals():
    MAIN_WINDOW.connect("delete-event", MAIN_WINDOW.hide)
    MAIN_WINDOW.connect("key-press-event", handle_keys)
    MAIN_WINDOW.connect("focus-out-event", hide_on_focus_lost)
    SEARCH_ENTRY.connect("activate", run_selected)
    SEARCH_ENTRY.connect("changed", update_selection)


def load_style_settings():
    select_provider = Gtk.CssProvider()
    select_provider.load_from_data(b'#selected' + settings.SELECTED_STYLE)
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(
    ), select_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    window_provider = Gtk.CssProvider()
    window_provider.load_from_data(b'#window' + settings.WINDOW_STYLE)
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(
    ), window_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    entry_provider = Gtk.CssProvider()
    entry_provider.load_from_data(b'#label' + settings.ENTRY_STYLE)
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(
    ), entry_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    search_provider = Gtk.CssProvider()
    search_provider.load_from_data(b'#search' + settings.SEARCHBAR_STYLE)
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(
    ), search_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    hover_provider = Gtk.CssProvider()
    hover_provider.load_from_data(b'#label:hover' + settings.SELECTED_STYLE)
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(
    ), hover_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# startup the whole system
load_style_settings()
setup_window()
connect_signals()
update_selection(SEARCH_ENTRY)
MAIN_WINDOW.show_all()

def wait_on_fifo():
    if not os.path.exists(TRIGGER_FIFO):
        os.mkfifo(TRIGGER_FIFO)
    while True:
        fd = os.open(TRIGGER_FIFO, os.O_RDONLY)
        while os.read(fd, 1000):
            pass
        os.close(fd)
        GObject.idle_add(MAIN_WINDOW.show_all)
    os.remove(TRIGGER_FIFO)



t = threading.Thread(target=wait_on_fifo)
t.daemon = True
t.start()

Gtk.main()
