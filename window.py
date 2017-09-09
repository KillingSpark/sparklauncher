import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

import launcher

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)

def quit_on_esc(widget, key_event):
    #esc key value
    if key_event.keyval == 65307:
        Gtk.main_quit()

win.connect("key-press-event",quit_on_esc)
win.set_decorated(False)

entryBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
win.add(entryBox)

entry = Gtk.Entry()
entryBox.add(entry)

labelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

win.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))

provider = Gtk.CssProvider()
provider.load_from_data('.entry { background: black; color: white; border-radius: 0px}')
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

entryBox.add(labelBox)

l = launcher.Launcher()

max_apps = 10
width = 600
height = 400

def update_selection(entry_object):
    l.filter(str.split(entry_object.get_text(), " "))
    
    for child in labelBox.get_children():
        labelBox.remove(child)

    for i in range(0,min(max_apps,len(l.filtered_entries))):
        label = Gtk.Label()
        label.set_markup("<span foreground=\"gray\" font_desc=\"19.0\">" + l.filtered_entries[i] + "</span>")
        labelBox.add(label)
    
    labelBox.add(Gtk.Label("  "))

    labelBox.show_all()
    labelCount = len(labelBox.get_children())+1
    lablHeight = (labelBox.get_children()[0].get_allocation().height)

entry.connect("changed", update_selection)

def run_selected(_):
    l.run_selected()
entry.connect("activate", run_selected)

win.show_all()


win.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
win.set_size_request(width, height)
win.set_resizable(False)

Gtk.main()