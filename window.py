#! /usr/bin/python2

import locking
if locking.check_lock_file():
    exit()
locking.create_lock_file()

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GLib

import settings
import launcher

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)

win.set_decorated(False)

entryBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
win.add(entryBox)

entry = Gtk.Entry()
entryBox.add(entry)

labelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

entryBox.override_background_color(Gtk.StateType.NORMAL, settings.COL_BACKGROUND_ENTRYLIST)

select_provider = Gtk.CssProvider()
select_provider.load_from_data('#selected' + settings.SELECTED_STYLE)
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), select_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

entry_provider = Gtk.CssProvider()
entry_provider.load_from_data('.entry' + settings.SEARCHBAR_STYLE)
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), entry_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

search_provider = Gtk.CssProvider()
search_provider.load_from_data('#label' + settings.ENTRY_STYLE)
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), search_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

entryBox.add(labelBox)

l = launcher.Launcher()

SELECTED_INDEX = -1
def update_selection(entry_object):
    global SELECTED_INDEX
    SELECTED_INDEX = -1
    try:
        labelBox.get_children()[SELECTED_INDEX].set_name("label")
    except IndexError:
        pass

    l.filter(str.split(entry_object.get_text(), " "))
    
    for child in labelBox.get_children():
        labelBox.remove(child)

    for i in range(0,min(settings.MAX_ENTRIES,len(l.filtered_entries))):
        label = Gtk.Label()
        text = GLib.markup_escape_text(l.filtered_entries[i].getName())
        label.set_markup("<span font_desc=\"19.0\">" + text + "</span>")
        label.set_name("label")
        label.set_max_width_chars(15)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        labelBox.add(label)

    labelBox.show_all()

entry.connect("changed", update_selection)

def run_selected(_):
    locking.delete_lock_file()
    if SELECTED_INDEX < 0:
        l.run_selected(0)

    l.run_selected(SELECTED_INDEX)

entry.connect("activate", run_selected)

def handle_keys(widget, key_event):
    global SELECTED_INDEX


    #esc key value
    if key_event.keyval == 65307:
        locking.delete_lock_file()
        Gtk.main_quit()

    #down
    elif key_event.keyval == 65364:
        if SELECTED_INDEX < len(labelBox.get_children())-1:
            if SELECTED_INDEX >= 0:
                labelBox.get_children()[SELECTED_INDEX].set_name("label")

            SELECTED_INDEX += 1
            labelBox.get_children()[SELECTED_INDEX].set_name("selected")
            
    #up
    elif key_event.keyval == 65362:
        if SELECTED_INDEX > 0:
            labelBox.get_children()[SELECTED_INDEX].set_name("label")
            SELECTED_INDEX -= 1
            labelBox.get_children()[SELECTED_INDEX].set_name("selected")

win.connect("key-press-event",handle_keys)

win.show_all()


win.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
win.set_size_request(settings.WIN_WIDTH, settings.WIN_HEIGHT)
win.set_resizable(False)

update_selection(entry)

Gtk.main()