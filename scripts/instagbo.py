#!/usr/bin/env python3

"""
instant gb-offset

Calculates between ROM offsets (hex / dec) and Game Boy addresses
in real time.

Yeah, I missed Pointerberechner way too much. :yea:

2022-09-11
"""

import tkinter as tk
import re
import math

class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.textboxes = []
		self.pack()
		self.setup()
	
	def update_texts(self, index, event=None):
		def offset_from(string):
			b, a = re.match("([0-9a-fA-F]{2,}):([0-9a-fA-F]{4})", string).groups()
			base = int(b, 16) * 0x4000
			if int(b, 16) == 0:
				addr = int(a, 16)
			else:
				addr = int(a, 16) - 0x4000
			offs = hex(base + addr)
			return offs[2:]

		def pointer_from(string):
			if string == '':
				return ''
			offs = int(string, 16)
			bank = math.floor(offs / 0x4000)
			if bank != 0:
				addr = (offs - (bank * 0x4000)) + 0x4000
			else:
				addr = (offs - (bank * 0x4000))
			return "%02x:%04x" % (bank, addr)
	
		def upd_one_text(index, replace_with):
			self.textboxes[index].delete(0,'end')
			self.textboxes[index].insert('end', replace_with)
		
		last_txt = self.textboxes[index].get()
		
		# correct input
		if index == 0:
			is_not_hex = re.match(r'^[0-9a-fA-F]+$', last_txt) is None
			last_txt = re.sub(r'[^0-9a-fA-F]', '', last_txt)
			if is_not_hex:
				upd_one_text(index, last_txt)
		elif index == 1:
			is_not_hex = re.match(r'^[0-9]+$', last_txt) is None
			last_txt = re.sub(r'[^0-9]', '', last_txt)
			if is_not_hex:
				upd_one_text(index, last_txt)
		
		# update the rest of the tables
		if index == 0:
			if last_txt == '':
				upd_one_text(1, '')
			else:
				upd_one_text(1, str(int(last_txt, 16)))
			upd_one_text(2, pointer_from(last_txt))
		elif index == 1:
			if last_txt == '':
				upd_one_text(0, '')
				upd_one_text(2, '')
			else:
				i = hex(int(last_txt))[2:]
				upd_one_text(0, i)
				upd_one_text(2, pointer_from(i))
		elif index == 2:
			if re.match("([0-9a-fA-F]{2,}):([0-9a-fA-F]{4})", last_txt):
				i = offset_from(last_txt)
				upd_one_text(1, str(int(i, 16)))
				upd_one_text(0, i)
	
	def setup(self):
		# hex
		self.t1l = tk.Label(self, text='Hexadecimal offset', justify=tk.LEFT)
		self.t1l.pack()
		self.t1 = tk.Entry(self, width=12, font=('monospace', 32))
		self.textboxes.append(self.t1)
		self.t1.bind("<KeyRelease>", lambda ev: self.update_texts(0, ev))
		self.t1.pack()
		
		# dec
		self.t2l = tk.Label(self, text='Decimal offset', justify=tk.LEFT)
		self.t2l.pack()
		self.t2 = tk.Entry(self, width=12, font=('monospace', 32))
		self.textboxes.append(self.t2)
		self.t2.bind("<KeyRelease>", lambda ev: self.update_texts(1, ev))
		self.t2.pack()
		
		# ptr
		self.t3l = tk.Label(self, text='Pointer', justify=tk.LEFT)
		self.t3l.pack()
		self.t3 = tk.Entry(self, width=12, font=('monospace', 32))
		self.textboxes.append(self.t3)
		self.t3.bind("<KeyRelease>", lambda ev: self.update_texts(2, ev))
		self.t3.pack()
	
	def quit(self):
		self.master.destroy()

if __name__ == '__main__':
	i = tk.Tk()
	i.resizable(False,False)
	i.title('instant gb-offset')
	app = App(master=i)
	i.protocol('WM_DELETE_WINDOW', app.quit)
	app.mainloop()
