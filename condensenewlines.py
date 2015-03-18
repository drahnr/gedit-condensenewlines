#!/usr/bin/env python

"""Condense Newlines plugin for Gedit3

Copyright (C) 2015 Bernhard Schuster

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

__author__ = "Bernhard Schuster"
__email__ = "yummi@ratpoison.io"

from gi.repository import GObject, Gio, Gtk, Gedit, GLib, Gdk

import re
import os

class CondenseNewlinesApp(GObject.Object, Gedit.AppActivatable):
	app = GObject.property(type=Gedit.App)

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		self.app.add_accelerator("F4", "win.condensenewlines", None)

	def do_deactivate(self):
		self.app.remove_accelerator("win.condensenewlines")

class CondenseNewlinesWindow(GObject.Object, Gedit.WindowActivatable):
	window = GObject.property(type=Gedit.Window)
	action = None
	doc = None

	def __init__(self):
		GObject.Object.__init__(self)
		self.regexsourcefiles = re.compile('.*\.(?:cpp|c|h|hpp|go|rust)$', re.IGNORECASE)

	def condense_iters(self):
		"""
		Pull the buffer into a Python string and then use regex to kick out the superflous newlines
		"""

		text = self.doc.get_text(self.doc.get_start_iter(), self.doc.get_end_iter(), False)

		compiledpattern = re.compile('((?:[\t\s]*\n){3,})', flags=re.MULTILINE)

		start_iter = self.doc.get_start_iter()
		end_iter   = self.doc.get_start_iter()

		line_no		= 0 # Last matched line no
		last_match_pos = 0 # Last matched position in the string
		deletednewlines = 0

		for match in re.finditer(compiledpattern, text):
			# inc in lines

			line_inc = text.count('\n', last_match_pos, match.start())
			# count the newlines in our match
			newlines_in_match = text.count('\n', match.start(), match.end())

			line_no += line_inc + 1;
			start_iter.set_line(line_no)
			start_iter.set_line_offset(0)

			print ("del lines from {0}", line_no)

			line_no += newlines_in_match - 2
			end_iter.set_line(line_no)
			end_iter.set_line_offset(0)

			print ("del lines to {0}", line_no)
			self.doc.delete(start_iter, end_iter)

			line_no = end_iter.get_line()+1

			last_match_pos = match.end()

	def condense_newlines(self, action, data=None):
		print ("\n\n executing action\n\n")
		if self.doc is not None:
			self.doc.begin_user_action()
			self.condense_iters()
			self.doc.end_user_action()
		else:
			print("No active document...\n\n")

	def do_activate(self):
		"""Activate plugin"""
		print ("\n\n registering action\n\n")
		self.action = Gio.SimpleAction(name="condensenewlines")
		print ("\n\n GAction = {} \n\n".format(self.action.get_name()))
		self.action.connect('activate', lambda a, p: self.condense_newlines(self.action))
		self.window.add_action(self.action)

	def do_update_state(self):
		self.doc = self.window.get_active_document();
		if self.doc is None:
			print ("\n\n no active document, disabling action\n\n")
		else:
			print ("\n\n enabling action\n\n")
#		if self.regexsourcefiles.match(self.doc.get_short_name_for_display()) is not None:
		self.window.lookup_action("condensenewlines").set_enabled(self.doc is not None)
#		else:
#			self.window.lookup_action("condensenewlines").set_enabled(False)

	def do_deactivate(self):
		print ("\n\n deregistering action\n\n")
		self.window.remove_action("condensenewlines")
