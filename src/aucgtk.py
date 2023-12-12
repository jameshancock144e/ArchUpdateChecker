#! /usr/bin/python3

import threading
from gi.repository import GLib, Gtk, GObject
from aucpacman import getUpdates, runUpdates

class UpdateNotificationWindow(Gtk.Window): # Window for displaying message to user
    def __init__(self, text):
        Gtk.Window.__init__(self, title="AUC") # Create window
        grid = Gtk.Grid() # Create component grid
        self.add(grid)
        label = Gtk.Label() # Create and set label to input
        label.set_markup(text)
        grid.attach(label, 0, 0, 2, 1)
        updateButton = Gtk.Button("Update") # Add update button
        viewButton = Gtk.Button("View") # Add view updates button
        viewButton.connect("clicked", self.launchViewWindow)
        updateButton.connect("clicked", self.launchUpdateWindow)
        grid.attach(viewButton, 0, 1, 1, 1)
        grid.attach(updateButton, 1, 1, 1, 1)

    def launchViewWindow(self, button):
        window = UpdateViewWindow(getUpdates())
        window.show_all()

    def launchUpdateWindow(self, button):
        window = UpdateStatusWindow(self)
        window.show_all()

class UpdateViewWindow(Gtk.Window): # Window for viewing available updates
    def __init__(self, updates):
        Gtk.Window.__init__(self, title="AUC") # Create window
        listbox = Gtk.ListBox() # Create list of updates
        for update in updates: # Populate update list
            label = Gtk.Label(update.decode("utf-8"))
            row = Gtk.ListBoxRow()
            row.add(label)
            listbox.add(row)
        self.add(listbox)

class UpdateStatusWindow(Gtk.Window): # Window for showing update status
    def __init__(self, parent):
        Gtk.Window.__init__(self, title="AUC") # Create window
        self.set_default_size(800, 600) # Set window size
        scrolledwindow = Gtk.ScrolledWindow() # Create scrolled container
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.add(scrolledwindow)
        self.textview = Gtk.TextView() # Create text view
        self.textbuffer = self.textview.get_buffer()
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.textview.set_wrap_mode(2)
        scrolledwindow.add(self.textview)
        self.updatesthread = threading.Thread(target=self.doUpdates) # Start updates thread
        self.updatesthread.start()
        self.super = parent

    def updateProgress(self, progress):
        self.textbuffer.insert_at_cursor(progress) # Add progress to text view
        self.textview.scroll_to_mark(self.textbuffer.get_insert(), 0.0, True, 0.5, 0.5)

    def doUpdates(self):
        updates = runUpdates() # Run updates
        for line in updates.stdout: # Update text view
            GLib.idle_add(self.updateProgress, line.decode())
