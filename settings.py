import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk

MAX_ENTRIES = 10
WIN_WIDTH = 600
WIN_HEIGHT = 400

SEARCHBAR_STYLE = b'{ background: black; color: white; border-radius: 0px; font-size: 19px;}'
ENTRY_STYLE = b'{ background: #696969; color: lightgrey; font-size: 19px;}'
ICON_STYLE = b'{ background: #696969 ;color: lightgrey; font-size: 19px; border: 0px; border-radius: 0px}'
SELECTED_STYLE = b'{ background: #434343; color: white; font-size: 19px;}'
WINDOW_STYLE = b'{ background: #696969; color: lightgrey;}'
