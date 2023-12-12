import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from aucpacman import getUpdates, syncDB

class MessageDialogWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="AUC")
        box = Gtk.Box(spacing=6)
        self.add(box)
        label = Gtk.Label()
        label.set_markup("<big>" + str(getUpdates()) + " updates are available</big>")
        box.add(label)

syncDB()
win = MessageDialogWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
