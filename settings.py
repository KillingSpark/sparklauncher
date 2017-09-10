import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk

MAX_ENTRIES = 10
WIN_WIDTH = 600
WIN_HEIGHT = 400

#COL_BACKGROUND_ENTRYLIST = Gdk.RGBA(0,0,0,1)
COL_BACKGROUND_ENTRYLIST = Gdk.RGBA()
COL_BACKGROUND_ENTRYLIST.parse('#696969')

SEARCHBAR_STYLE = '{ background: black; color: white; border-radius: 0px; font-size: 19px;}'
ENTRY_STYLE = '{ background: #696969; color: lightgrey; font-size: 19px;}'
SELECTED_STYLE = '{ background: #434343; color: white}'
