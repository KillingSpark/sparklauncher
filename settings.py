import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk

MAX_ENTRIES = 9
MAX_ENTRY_CHARS = 39
WIN_WIDTH = 600
WIN_HEIGHT = 400

#border and color stlyes for some reason dont get passed down from the window to the cildren, font-size does tho
SEARCHBAR_STYLE =   b'{ background: #000000;    color: white;       border-width: 1px; border-radius: 0px;}'
ENTRY_STYLE =       b'{ background: #696969;    color: lightgrey;   border-width: 0px; border-radius: 0px;}'
SELECTED_STYLE =    b'{ background: #434343;    color: #5294E2;     border-width: 0px; border-radius: 0px;}'
WINDOW_STYLE =      b'{ background: #696969;    color: lightgrey;   font-size: 19px;}'

JUSTIFY_ENTRY = "CENTER" #LEFT/RIGHT/CENTER
