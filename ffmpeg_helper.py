import pprint
import tkinter as tk
from tkinter import ttk
import sys
import os
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import re

NUM_ROWS=1
NUM_COLS=1
FFMPEG_EXE="c:\\varie\\ffmpeg\\bin\\ffmpeg.exe -hide_banner"
list_regex = {"codecs":"^ [^ ]{6} [^ ^=]+", "filters":"^ [^ ^=]{1,3} [^ ^=]+",
  "formats":" [DE]{1,2}[ ]+[^ ^=]+"}
class Application(tk.Frame):
	
	def __init__(self, master=None, w=800, h=600):
		self.opt = -1
		tk.Frame.__init__(self, master, width=w, height=h)
		pp = True
		if pp:
			self.pack(expand=True, fill=tk.BOTH)
		else:	
			for c in range(NUM_COLS):
				self.columnconfigure(c, weight=1)
			for r in range(NUM_ROWS):
				self.rowconfigure(r, weight=1)
			self.grid(sticky="NSEW")	
		self.update()
		pprint.pprint(self.winfo_geometry())
		#lc = self.get_ffmpeg_codecs()	
		lc = self.get_ffmpeg_list("codecs")
		self.createWidgets()
		self.list_cod['values'] = lc
		self.list_enc['values'] = lc
		lf = self.get_ffmpeg_list("filters")
		#pprint.pprint(lf)

	def onComboCod(self, event):
		txt = self.list_cod.get()
		#print(txt) # debug
		helpstr = os.popen(FFMPEG_EXE + " -h decoder=" + txt).read()
		#print(helpstr) # debug
		helpstr = helpstr.replace("\n", "     \n") # workaround perche' la scrollbar si sovrappone al testo !!!
		self.help_cod.delete('0.0', tk.END)
		self.help_cod.insert(tk.END, helpstr)
		self.help_cod.update()
		
	def onComboEnc(self, event):
		txt = self.list_enc.get()
		#print(txt) # debug
		helpstr = os.popen(FFMPEG_EXE + " -h encoder=" + txt).read()
		#print(helpstr) # debug
		helpstr = helpstr.replace("\n", "     \n")
		self.help_enc.delete('0.0', tk.END)
		self.help_enc.insert(tk.END, helpstr)
		self.help_enc.update()
			
	def createWidgets(self):
		#pprint.pprint(self.configure())
		#self.nb = ttk.Notebook(self)
		self.nb = ttk.Notebook(self, width=self.winfo_width(), height=self.winfo_height())
		pp = True
		if pp:
			self.nb.pack(expand=True, fill=tk.BOTH)
		else:	
			self.nb.rowconfigure(0, weight=1)
			self.nb.columnconfigure(0, weight=1)
			self.nb.grid(row=0, column=0, sticky="NSEW")
		######
		self.tab1 = tk.Frame(self.nb)
		self.tab2 = tk.Frame(self.nb)
		self.tab1.pack(expand=True, fill=tk.BOTH)
		self.tab2.pack(expand=True, fill=tk.BOTH)
		self.nb.add(self.tab1, text="Decoders")
		self.nb.add(self.tab2, text="Encoders")
		######
		self.list_cod = ttk.Combobox(self.tab1)
		self.help_cod = tk.Text(self.tab1, wrap="none")
		self.list_cod.grid(row=0, column=0)
		self.help_cod.grid(row=1, column=0, sticky="NSEW")
		self.list_cod.bind("<<ComboboxSelected>>", self.onComboCod)
		self.sb_cod_h=ttk.Scrollbar(self.help_cod, orient=tk.HORIZONTAL)
		self.sb_cod_v=ttk.Scrollbar(self.help_cod)
		self.help_cod.config(xscrollcommand=self.sb_cod_h.set, yscrollcommand=self.sb_cod_v.set)
		self.sb_cod_h.config( command = self.help_cod.xview )
		self.sb_cod_v.config( command = self.help_cod.yview )
		self.sb_cod_h.pack(side=tk.BOTTOM,fill=tk.X) # ??? usando la grid non si riesce a posizionare correttamente ...
		self.sb_cod_v.pack(side=tk.RIGHT,fill=tk.Y)
		##################
		self.list_enc = ttk.Combobox(self.tab2)
		self.help_enc = tk.Text(self.tab2, wrap="none")
		self.list_enc.grid(row=0, column=0)
		self.help_enc.grid(row=1, column=0, sticky="NSEW")
		self.list_enc.bind("<<ComboboxSelected>>", self.onComboEnc)
		self.sb_enc_h=ttk.Scrollbar(self.help_enc, orient=tk.HORIZONTAL)
		self.sb_enc_v=ttk.Scrollbar(self.help_enc)
		self.help_enc.config(xscrollcommand=self.sb_enc_h.set, yscrollcommand=self.sb_enc_v.set)
		self.sb_enc_h.config( command = self.help_enc.xview )
		self.sb_enc_v.config( command = self.help_enc.yview )
		self.sb_enc_h.pack(side=tk.BOTTOM,fill=tk.X)
		self.sb_enc_v.pack(side=tk.RIGHT,fill=tk.Y)
		##################
		# i 2 tab sono organizzati a griglia ...
		self.tab1.rowconfigure(0, weight=1)
		self.tab1.rowconfigure(1, weight=20)
		self.tab1.columnconfigure(0, weight=1)
		self.tab2.rowconfigure(0, weight=1)
		self.tab2.rowconfigure(1, weight=20)
		self.tab2.columnconfigure(0, weight=1)
		
	def get_ffmpeg_list(self, listtype="codecs"):
		global list_regex
		self.codecs =	os.popen(FFMPEG_EXE + " -"+listtype).read()
		cd = self.codecs.split("\n")
		list_out = []
		for x in cd:
			m = re.search(list_regex[listtype], x)
			if m:
				#y = m.group(0)[1:].split(" ")
				y = re.split("[ ]+", m.group(0)[1:])
				list_out.append( y[1] )
		return list_out
		
	def get_ffmpeg_codecs(self):
		self.codecs =	os.popen(FFMPEG_EXE + " -codecs").read()
		cd = self.codecs.split("\n")
		list_cod = []
		for x in cd:
			m = re.search("^ [^ ]{6} [^ ^=]+", x)
			if m:
				#print( m.group(0) ) # debug
				y = m.group(0)[1:].split(" ")
				#print(y[1]) # debug
				#list_cod.append( y[1] + "\n" )
				list_cod.append( y[1] )
		return list_cod
	
	
app = Application(w=640,h=480) #(w=1200,h=900)
app.master.title('FFMPEG helper')
app.mainloop()
